// Samanantar core engine — pure, deterministic, offline.
// Mirrors plam.md v2 §3.0: ladder (K5→Story, C→R→A), stop rules, error taxonomy,
// TaRL grouping, remediation lookup, dashboard, append-only event store.

// ---------- Levels ----------
export const LITERACY_LADDER = ['pre_letter', 'letter', 'word', 'paragraph', 'story'];
export const NUMERACY_LADDER = ['num_concrete', 'num_representation', 'num_abstract'];
export const LADDER_BY_DOMAIN = { literacy: LITERACY_LADDER, numeracy: NUMERACY_LADDER };

// ---------- ASR matching (Devanagari-tolerant) ----------
// Strips matras/vowel signs & nukta so "किताब" vs "किताब्" vs matra slips still
// match the target; CER is computed on the raw string for honest reporting.
const DEVANAGARI_SIGN = /[\u093E-\u094D\u0901-\u0903\u093C]/g;

export function normalizeDevanagari(s) {
  return String(s ?? '').replace(DEVANAGARI_SIGN, '').replace(/\s+/g, '').trim();
}

// Levenshtein distance on raw strings (used for CER-style scoring).
export function levenshtein(a, b) {
  a = String(a ?? ''); b = String(b ?? '');
  if (a === b) return 0;
  const m = a.length, n = b.length;
  if (!m) return n;
  if (!n) return m;
  let prev = Array.from({ length: n + 1 }, (_, i) => i);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    prev = cur;
  }
  return prev[n];
}

// A response matches if: exact, or ASR-confidence-weighted fuzzy match on the
// normalized form (simulates teacher's 1-tap correction upstream of this).
export function responseMatches(item, transcript, asrConfidence = 1.0) {
  if (transcript == null || transcript === '') return false;
  const target = String(item.prompt);
  if (item.kind === 'read_aloud') {
    if (transcript === target) return true;
    const normT = normalizeDevanagari(transcript);
    const normP = normalizeDevanagari(target);
    // Matra-only slip counts as a read — but only when ASR is confident.
    // At low confidence, a consonant-skeleton match is not enough evidence.
    if (normT === normP && asrConfidence >= 0.6) return true;
    // CER on RAW strings (honest metric; matras count as chars).
    const dist = levenshtein(transcript, target);
    const maxLen = Math.max(transcript.length, target.length) || 1;
    const cer = dist / maxLen;
    // Threshold tightens as ASR confidence drops — never accept garbage.
    const tolerance = 0.25 * asrConfidence + 0.05;
    if (cer <= tolerance) return true;
    // Keyword-spotting fallback (plam.md v2 §4 Phase 2): for short items,
    // accept when the target's consonant skeleton is contained in what was
    // heard — robust to noise-induced char drops on letters/words. Gated on
    // confidence and disabled for single akshars (too weak as evidence).
    if (asrConfidence >= 0.5 && normP.length >= 2 && normT.includes(normP)) return true;
    return false;
  }
  if (item.kind === 'audio_choice') {
    const normT = normalizeDevanagari(transcript);
    return (item.accepts ?? []).some((a) => {
      if (a === transcript) return true;
      const normA = normalizeDevanagari(a);
      // Single akshars must match exactly — a different akshar is a real error.
      if (normT.length <= 2 && normA.length <= 2) return normT === normA;
      return normT.length === normA.length && levenshtein(normT, normA) <= 1 && asrConfidence >= 0.6;
    });
  }
  return false;
}

// Consonant skeleton (normalized Devanagari) — the KWS signature.
export function asrSkeleton(s) {
  return normalizeDevanagari(s);
}

// ---------- Adaptive ladder (stop rules per plam.md v2 §4 Phase 2) ----------
export const PASS_THRESHOLD = 0.6;      // ≥60% correct → level passed
export const MAX_TIME_PER_CHILD_MS = 5 * 60 * 1000; // hard cap 5 min

export function startAssessment(domain = 'literacy') {
  const ladder = LADDER_BY_DOMAIN[domain];
  return {
    domain,
    ladder,
    idx: 0,
    results: [],
    startedAt: Date.now(),
    finished: false,
    finalLevel: null,
    scored: { correct: 0, total: 0 },
    timedOut: false,
  };
}

export function nextItem(state, pack) {
  if (state.finished) return null;
  const items = pack.items.filter(
    (it) => it.domain === state.domain && it.level === state.ladder[state.idx]
  );
  const alreadyUsed = new Set(state.results.map((r) => r.itemId));
  return items.find((it) => !alreadyUsed.has(it.itemId)) ?? items[0] ?? null;
}

export function recordResponse(state, item, { correct, timeMs, transcript = null, asrConfidence = 1.0, teacherOverride = false, chosenAnswer = null } = {}, pack = null) {
  if (state.finished) return state;
  state.results.push({
    itemId: item.itemId, level: item.level, correct, timeMs,
    transcript, asrConfidence, teacherOverride, chosenAnswer,
  });
  state.scored.correct += correct ? 1 : 0;
  state.scored.total += 1;

  // Cumulative simulated clock (wall-clock independent → deterministic tests).
  state.elapsedMs = (state.elapsedMs ?? 0) + timeMs;
  if (state.elapsedMs > MAX_TIME_PER_CHILD_MS) {
    state.finished = true;
    state.timedOut = true;
    state.finalLevel = state.ladder[Math.max(0, state.idx - 1)] ?? state.ladder[0];
    return state;
  }

  const levelResults = state.results.filter((r) => r.level === item.level);
  const passed = levelResults.filter((r) => r.correct).length;
  const n = levelResults.length;

  // Decide once we have 3 observations OR the level's items are exhausted
  // (short levels like `story` must still terminate).
  const unusedAtLevel = pack
    ? pack.items.filter(
        (it) =>
          it.domain === state.domain &&
          it.level === item.level &&
          !state.results.some((r) => r.itemId === it.itemId)
      ).length
    : Number.MAX_SAFE_INTEGER;
  const decided = n >= 3 || unusedAtLevel === 0;
  if (!decided) return state;

  if (passed / n >= PASS_THRESHOLD) {
    // Advance; if top of ladder, finish.
    if (state.idx === state.ladder.length - 1) {
      state.finished = true;
      state.finalLevel = state.ladder[state.idx];
    } else {
      state.idx += 1;
    }
  } else {
    // Fail level → final level is the highest *passed* one; floor = ladder[0]
    // (ASER semantics: a child who cannot read letters IS at 'pre_letter').
    state.finished = true;
    state.finalLevel = state.ladder[Math.max(0, state.idx - 1)];
  }
  return state;
}

export function finishAssessment(state) {
  if (!state.finished) {
    state.finished = true;
    state.finalLevel = state.idx > 0 ? state.ladder[state.idx - 1] : null;
  }
  return state;
}

// ---------- Error taxonomy ----------
export function classifyErrors(state, pack) {
  const codes = [];
  for (const r of state.results) {
    if (r.correct) continue;
    const item = pack.items.find((it) => it.itemId === r.itemId);
    if (!item) continue;
    if (r.level === 'num_abstract' && item.borrowRequired) {
      const wrong = String(r.chosenAnswer ?? '');
      const stem = String(item.prompt);
      // Heuristic "avoided borrowing" detector: |wrong| < |correct| and no carry marker.
      const correct = item.choices[item.correctIndex];
      const nums = stem.match(/\d+/g) ?? [];
      const a = Number(nums[0]), b = Number(nums[1]);
      const isSubtraction = stem.includes('−') || stem.includes('-');
      if (isSubtraction && wrong && Number(wrong) < Number(correct)) {
        codes.push({ code: 'NUM-ABS-02', label: 'Avoids borrowing', itemId: item.itemId });
        continue;
      }
      if (isSubtraction && a && b && a - b !== Number(correct) && Number(wrong) === Math.abs(a - b)) {
        codes.push({ code: 'NUM-ABS-01', label: 'Forgets borrowing', itemId: item.itemId });
        continue;
      }
      codes.push({ code: 'NUM-ABS-01', label: 'Forgets borrowing', itemId: item.itemId });
      continue;
    }
    const ec = pack.errorCodes.find((e) =>
      e.detect.signal.kind === 'exact_miss' && e.detect.signal.value === item.itemId
    ) ?? pack.errorCodes.find((e) =>
      e.detect.domain === item.domain && e.detect.level === item.level
    );
    if (ec) codes.push({ code: ec.code, label: ec.label, itemId: item.itemId });
  }
  return codes;
}

// ---------- Remediation ----------
export function remediationFor(errorCode, pack, { craStage = 'concrete' } = {}) {
  const ec = pack.errorCodes.find((e) => e.code === errorCode);
  if (!ec) return null;
  return (
    ec.remediations.find((r) => r.craStage === craStage) ??
    ec.remediations[0] ??
    null
  );
}

// ---------- TaRL grouping (bands, not grades; max 8) ----------
export function groupClass(children, { maxGroupSize = 8 } = {}) {
  const bands = new Map();
  for (const c of children) {
    const key = `${c.domain}:${c.level ?? 'unassessed'}`;
    if (!bands.has(key)) bands.set(key, []);
    bands.get(key).push(c);
  }
  const groups = [];
  for (const [key, members] of [...bands.entries()].sort()) {
    for (let i = 0; i < members.length; i += maxGroupSize) {
      groups.push({
        id: `G-${key}-${groups.length + 1}`,
        domain: key.split(':')[0],
        level: key.split(':')[1],
        childIds: members.slice(i, i + maxGroupSize).map((c) => c.childId),
      });
    }
  }
  return groups;
}

// ---------- Dashboard aggregation ----------
export function classHeatmap(children) {
  const dist = {};
  for (const c of children) {
    const key = `${c.domain}:${c.level ?? 'unassessed'}`;
    dist[key] = (dist[key] ?? 0) + 1;
  }
  return dist;
}

export function nextBestAction(children, groups, pack) {
  return groups.map((g) => {
    const sampleChild = children.find((c) => c.childId === g.childIds[0]);
    const errs = sampleChild?.errorCodes ?? [];
    const primary = errs[0]?.code;
    const rem = primary ? remediationFor(primary, pack) : null;
    return {
      groupId: g.id,
      level: g.level,
      nChildren: g.childIds.length,
      activity: rem?.activity ?? 'Review level items',
      ncertRef: rem?.ncertRef ?? '—',
    };
  });
}

// ---------- Append-only event store (plam.md v2 §3.0/§3.2) ----------
export function createEventStore(deviceId = 'DEV-001') {
  const events = [];
  let seq = 0;
  return {
    get events() { return events; },
    get cursor() { return seq; },
    append(type, payload, ts = Date.now()) {
      const ev = { seq: seq++, deviceId, type, payload, ts };
      events.push(ev);
      return ev;
    },
    // Deterministic replay: state is a pure fold over events.
    replay() {
      return events;
    },
    // Sync contract: gzip+batch is the transport's job; here we emit batches & ack cursors.
    since(cursor) {
      return events.filter((e) => e.seq > cursor);
    },
    ack(upTo) { seq = Math.max(seq, upTo); },
    // Cursor = number of events already uploaded. Slice-based → cursor-safe.
    exportBatch(cursor, batchSize = 500) {
      const pending = events.slice(cursor);
      const batch = pending.slice(0, batchSize);
      return { batch, nextCursor: cursor + batch.length };
    },
  };
}

// ---------- Pilot: stratified randomization (plam.md v2 §4) ----------
// treatFrac = fraction of EACH stratum assigned to treatment (balance within strata).
export function stratifiedAssign(children, strataFn, treatFrac = 0.5, rand = Math.random) {
  const strata = new Map();
  for (const c of children) {
    const k = strataFn(c);
    if (!strata.has(k)) strata.set(k, []);
    strata.get(k).push(c);
  }
  const assignment = new Map();
  for (const [, members] of strata) {
    const shuffled = [...members].sort(() => rand() - 0.5);
    const nTreat = Math.round(shuffled.length * treatFrac);
    shuffled.forEach((c, i) => assignment.set(c.childId, i < nTreat ? 'treatment' : 'control'));
  }
  return assignment;
}

// ---------- Power analysis (cluster RCT, honest MDES) ----------
export function mdesCluster({ nClustersPerArm, clusterSize, icc = 0.15, alpha = 0.05, power = 0.8 }) {
  const zAlpha = 1.959963985;
  const zPower = 1.281551566; // 80% (one-sided convention for MDES tables)
  const df = 2 * nClustersPerArm - 2;
  if (df <= 0) return null;
  const tCrit = approxTCrit(df, 1 - alpha / 2);
  const designEffect = 1 + (clusterSize - 1) * icc;
  const nPerArm = nClustersPerArm * clusterSize;
  const mdes = (tCrit + zPower) * Math.sqrt((2 * designEffect) / nPerArm);
  return { mdes, designEffect, nPerArm, df };
}

function approxTCrit(df, q) {
  // Normal approximation with a small-t correction (adequate for planning tables).
  const z = q === 0.975 ? 1.959963985 : 1.281551566;
  const a1 = (z ** 3 + z) / (4 * df);
  const a2 = (5 * z ** 5 + 16 * z ** 3 + 3 * z) / (96 * df ** 2);
  return z + a1 + a2;
}

// ---------- Quadratic-weighted kappa (agreement metric) ----------
export function quadraticWeightedKappa(raterA, raterB, categories) {
  const n = raterA.length;
  if (n === 0) return 1;
  const k = categories.length;
  const idx = new Map(categories.map((c, i) => [c, i]));
  const O = Array.from({ length: k }, () => Array(k).fill(0));
  for (let i = 0; i < n; i++) {
    const a = idx.get(raterA[i]); const b = idx.get(raterB[i]);
    if (a == null || b == null) continue;
    O[a][b] += 1;
  }
  const rowSums = O.map((r) => r.reduce((s, x) => s + x, 0));
  const colSums = Array.from({ length: k }, (_, j) => O.reduce((s, row) => s + row[j], 0));
  const total = rowSums.reduce((s, x) => s + x, 0) || 1;
  const E = Array.from({ length: k }, (_, i) =>
    Array.from({ length: k }, (_, j) => (rowSums[i] * colSums[j]) / total)
  );
  const w = Array.from({ length: k }, (_, i) =>
    Array.from({ length: k }, (_, j) => ((i - j) ** 2) / ((k - 1) ** 2 || 1))
  );
  let num = 0, den = 0;
  for (let i = 0; i < k; i++) for (let j = 0; j < k; j++) {
    num += w[i][j] * O[i][j];
    den += w[i][j] * E[i][j];
  }
  if (den === 0) return 1;
  return 1 - num / den;
}

// ---------- TOST equivalence (two one-sided tests, paired-ish approx) ----------
export function tostEquivalent(dDiff, se, margin = 0.2, alpha = 0.05) {
  const z = 1.644853627; // one-sided 5%
  const lower = (dDiff + margin) / se;
  const upper = (margin - dDiff) / se;
  return { pass: lower > z && upper > z, lowerT: lower, upperT: upper, margin };
}

// ---------- CSV export ----------
export function toCsv(rows) {
  if (!rows.length) return '';
  const cols = Object.keys(rows[0]);
  const esc = (v) => {
    const s = String(v ?? '');
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [cols.join(','), ...rows.map((r) => cols.map((c) => esc(r[c])).join(','))].join('\n');
}

// ============================================================================
// Level-map snapshot — a pure fold over the append-only event log.
// ARCHITECTURE_OFFLINE.md §6: the event log is the source of truth; the
// snapshot is a disposable, rebuildable view. Corrupt snapshot → delete and
// replay. Because events are immutable and ordered by `seq`, replay is
// idempotent and sync never needs merge logic.
// ============================================================================

export const LEVEL_MAP_EVENT = {
  ASSESSMENT: 'assessment_completed',
  OVERRIDE: 'teacher_override',
};

const rowKey = (childId, domain) => `${childId}|${domain}`;

/** An empty snapshot. `cursor` is the highest applied event `seq` (-1 = none). */
export function createLevelMap() {
  return { rows: {}, cursor: -1, applied: 0, ignored: 0 };
}

function cloneRows(rows) {
  const out = {};
  for (const [k, r] of Object.entries(rows ?? {})) {
    out[k] = { ...r, errorCodes: [...(r.errorCodes ?? [])] };
  }
  return out;
}

// Policy: **last event wins**, by fold order. `overridden` therefore means
// "the level currently in force came from a teacher correction, not the sensor."
// A teacher override outranks the model; a *later* assessment is fresh evidence
// and supersedes it. An assessment with no recorded level never clears an
// override (it carries no new information about the level).
function foldEvent(snapshot, ev) {
  const type = ev?.type;
  const p = ev?.payload ?? {};
  const { childId, domain } = p;
  const known =
    type === LEVEL_MAP_EVENT.ASSESSMENT || type === LEVEL_MAP_EVENT.OVERRIDE;
  if (!known || !childId || !domain) {
    snapshot.ignored += 1;
    return;
  }

  const key = rowKey(childId, domain);
  const prev = snapshot.rows[key] ?? {
    childId, domain, level: null, errorCodes: [], lastSeen: null,
    nObservations: 0, nOverrides: 0, overridden: false, source: null,
  };
  const row = { ...prev, errorCodes: [...prev.errorCodes] };

  if (type === LEVEL_MAP_EVENT.ASSESSMENT) {
    if (p.finalLevel) {
      row.level = p.finalLevel;
      row.overridden = false;
      row.source = 'assessment';
    }
    if (Array.isArray(p.errorCodes)) {
      row.errorCodes = p.errorCodes
        .map((e) => (typeof e === 'string' ? e : e?.code))
        .filter(Boolean);
    }
    row.nObservations += 1;
  } else {
    if (!p.level) {
      snapshot.ignored += 1;
      return;
    }
    row.level = p.level;
    row.overridden = true;
    row.source = 'override';
    row.nOverrides += 1;
  }

  if (ev.ts != null) row.lastSeen = ev.ts;
  snapshot.rows[key] = row;
  snapshot.applied += 1;
}

/**
 * Fold events into a snapshot. Pure: never mutates `events` or `base`.
 * Pass `base` to apply only the tail (events with `seq > base.cursor`) —
 * a crash mid-write leaves the cursor unadvanced, so replay simply redoes it.
 * Events must carry a numeric `seq` (as `createEventStore().append` assigns).
 */
export function materializeLevelMap(events = [], { base = null } = {}) {
  const snapshot = base
    ? { rows: cloneRows(base.rows), cursor: base.cursor ?? -1, applied: 0, ignored: 0 }
    : createLevelMap();
  const startCursor = snapshot.cursor;

  const ordered = [...events].sort((a, b) => (a?.seq ?? 0) - (b?.seq ?? 0));
  for (const ev of ordered) {
    const seq = ev?.seq ?? 0;
    if (seq <= startCursor) continue; // already folded into `base`
    foldEvent(snapshot, ev);
    if (seq > snapshot.cursor) snapshot.cursor = seq;
  }
  return snapshot;
}

/** Deterministically ordered rows (childId, then domain) — safe to diff and export. */
export function levelMapRows(snapshot) {
  return Object.values(snapshot?.rows ?? {})
    .map((r) => ({ ...r, errorCodes: [...(r.errorCodes ?? [])] }))
    .sort(
      (a, b) =>
        String(a.childId).localeCompare(String(b.childId)) ||
        String(a.domain).localeCompare(String(b.domain))
    );
}

/** Adapter: snapshot → the child shape `groupClass`/`classHeatmap` expect. */
export function levelMapChildren(snapshot) {
  return levelMapRows(snapshot).map(({ childId, domain, level, errorCodes }) => ({
    childId, domain, level, errorCodes,
  }));
}

// ============================================================================
// PlanAssembler — deterministic offline plan generation.
// ARCHITECTURE_OFFLINE.md §7. Pure: no clock, no randomness, no network.
//
// The safety invariant: with no network this can only ever emit *pre-validated*
// blocks from the signed content pack. There is no generative step, so there is
// no hallucination surface. The same citation rule guards Claude's online
// output, which is why both tiers meet one standard.
//
// Returns { ok: true, plan } or { ok: false, reasons } — never a half-plan.
// ============================================================================

export const PLAN_DEFAULTS = {
  totalMinutes: 40,
  openingMinutes: 5,
  closingMinutes: 5,
  minRotationMinutes: 8,
  rotations: 2,
  maxStationsPerRound: 3,
  maxGroupSize: 8,
  maxHelpFirst: 3,
};

const ladderIndex = (domain, level) => (LADDER_BY_DOMAIN[domain] ?? []).indexOf(level);

const isCited = (a) =>
  !!(a && a.ncertRef && a.ncertRef.book && a.ncertRef.page && a.cbseFln);

/**
 * CI gate: every opener, block and closer must cite an NCERT page + CBSE FLN
 * code. Enforced by test, not by trust — same rule as `validate_content_pack`.
 */
export function validatePlanContent(pack) {
  const errs = [];
  const sections = [
    ['opener', pack?.openers ?? []],
    ['block', pack?.blocks ?? []],
    ['closer', pack?.closers ?? []],
  ];
  for (const [kind, arr] of sections) {
    if (!Array.isArray(arr)) {
      errs.push(`${kind}s is not an array`);
      continue;
    }
    for (const b of arr) {
      const id = b?.blockId ?? `${kind}?`;
      if (!b?.chapterId) errs.push(`${id} missing chapterId`);
      if (!b?.activity) errs.push(`${id} missing activity`);
      if (!b?.ncertRef || !b.ncertRef.book || !b.ncertRef.page) errs.push(`${id} missing ncertRef`);
      if (!b?.cbseFln) errs.push(`${id} missing cbseFln`);
    }
  }
  return errs;
}

/** Least-recently-used first, then blockId ascending — fully deterministic. */
function pickLeastRecentlyUsed(pool, history = {}) {
  return (
    [...pool].sort((a, b) => {
      const la = history[a.blockId] ?? ''; // never used sorts first
      const lb = history[b.blockId] ?? '';
      if (la !== lb) return la < lb ? -1 : 1;
      return String(a.blockId).localeCompare(String(b.blockId));
    })[0] ?? null
  );
}

/** Exact level, else the nearest *lower* level (never above the child's band). */
function pickStationBlock(blocks, band, history) {
  const ladder = LADDER_BY_DOMAIN[band.domain] ?? [];
  const at = ladder.indexOf(band.level);
  for (let i = at; i >= 0; i--) {
    const pool = blocks.filter((b) => b.domain === band.domain && b.level === ladder[i]);
    if (pool.length) {
      return {
        block: pickLeastRecentlyUsed(pool, history),
        isFallback: i !== at,
        matchedLevel: ladder[i],
      };
    }
  }
  return null;
}

/**
 * Assemble one differentiated block from a level-map and a chapter.
 *
 * @param {object}   o
 * @param {string}   o.chapterId  chapter to build the block around
 * @param {object|Array} o.levelMap  snapshot from `materializeLevelMap`, or children[]
 * @param {object}   o.pack       content pack with openers/blocks/closers
 * @param {string}   [o.date]     ISO date — passed in, never read from the clock
 * @param {object}   [o.history]  { [blockId]: lastUsedISODate } for anti-repetition
 * @param {object}   [o.constraints]
 */
export function assemblePlan({
  date = null,
  chapterId,
  levelMap,
  pack,
  constraints = {},
  history = {},
} = {}) {
  const c = { ...PLAN_DEFAULTS, ...constraints };
  const fail = (reasons) => ({ ok: false, reasons, chapterId: chapterId ?? null });

  if (!chapterId) return fail(['chapterId is required']);
  if (!pack) return fail(['content pack is required']);
  if (!Array.isArray(pack.blocks)) return fail(['content pack has no activity blocks']);

  // The pack is the safety surface — reject it wholesale if any block is uncited.
  const packErrors = validatePlanContent(pack);
  if (packErrors.length) return fail([`content pack invalid: ${packErrors.join('; ')}`]);

  const blocks = pack.blocks.filter((b) => b.chapterId === chapterId);
  if (!blocks.length) return fail([`no activity blocks for chapter "${chapterId}"`]);

  const children = Array.isArray(levelMap)
    ? levelMap
    : levelMapChildren(levelMap ?? createLevelMap());
  if (!children.length) return fail(['level-map is empty — assess at least one child first']);

  const bands = groupClass(children, { maxGroupSize: c.maxGroupSize })
    .filter((g) => g.level != null && g.level !== 'unassessed')
    .sort(
      (a, b) =>
        ladderIndex(a.domain, a.level) - ladderIndex(b.domain, b.level) ||
        String(a.id).localeCompare(String(b.id))
    );
  if (!bands.length) return fail(['no assessed bands — every child is still unassessed']);

  const reasons = [];
  const warnings = [];

  // ---- whole-class opener and closer -------------------------------------
  const opening = pickLeastRecentlyUsed(
    (pack.openers ?? []).filter((o) => o.chapterId === chapterId),
    history
  );
  const closing = pickLeastRecentlyUsed(
    (pack.closers ?? []).filter((o) => o.chapterId === chapterId),
    history
  );
  if (!opening) reasons.push(`no whole-class opener for chapter "${chapterId}"`);
  if (!closing) reasons.push(`no closer for chapter "${chapterId}"`);

  // ---- one differentiated station per band -------------------------------
  const stations = [];
  for (const band of bands) {
    const picked = pickStationBlock(blocks, band, history);
    if (!picked) {
      reasons.push(`no activity for band ${band.domain}:${band.level}`);
      continue;
    }
    stations.push({
      blockId: picked.block.blockId,
      bandId: band.id,
      domain: band.domain,
      level: band.level,
      matchedLevel: picked.matchedLevel,
      isFallback: picked.isFallback,
      childIds: [...band.childIds],
      n: band.childIds.length,
      activity: picked.block.activity,
      talkLine: picked.block.talkLine ?? null,
      ncertRef: picked.block.ncertRef,
      cbseFln: picked.block.cbseFln,
      minutes: null, // set once the time plan is known
    });
  }
  if (stations.length > c.maxStationsPerRound) {
    warnings.push(
      `${stations.length} bands to ${c.maxStationsPerRound} station slots — the teacher can give direct time to only ${c.rotations} band(s) this block`
    );
  }

  // ---- time plan (structural: always sums to <= totalMinutes) -------------
  const workMinutes = c.totalMinutes - c.openingMinutes - c.closingMinutes;
  let rotations = Math.max(1, c.rotations);
  let minutesPerRotation = Math.floor(workMinutes / rotations);
  if (minutesPerRotation < c.minRotationMinutes && rotations > 1) {
    rotations = 1;
    minutesPerRotation = workMinutes;
  }
  if (workMinutes < c.minRotationMinutes) {
    reasons.push(
      `insufficient time: ${c.totalMinutes} min leaves ${workMinutes} min of work after the opener and close`
    );
  } else if (minutesPerRotation < c.minRotationMinutes) {
    reasons.push(
      `insufficient time: ${minutesPerRotation} min per rotation (minimum ${c.minRotationMinutes})`
    );
  }
  const scheduledMinutes = Math.max(0, rotations * minutesPerRotation);
  for (const s of stations) s.minutes = scheduledMinutes;

  // Teacher attention rotates weakest-band-first (the bands array is already
  // ordered lowest level first), so the children with the largest gap get the
  // adult; the remaining bands work independently.
  const teacherFocus = [];
  for (let r = 0; r < rotations && stations.length; r++) {
    const station = stations[r % stations.length];
    teacherFocus.push({
      round: r + 1,
      minutes: minutesPerRotation,
      bandId: station.bandId,
      domain: station.domain,
      level: station.level,
      talkLine: station.talkLine,
    });
  }

  // ---- who to help first -------------------------------------------------
  const helpFirst = [];
  for (const s of stations) {
    for (const childId of s.childIds) {
      if (helpFirst.length >= c.maxHelpFirst) break;
      const child = children.find((ch) => ch.childId === childId);
      const err = (child?.errorCodes ?? [])[0];
      if (!err) continue;
      helpFirst.push({
        childId,
        bandId: s.bandId,
        level: s.level,
        errorCode: typeof err === 'string' ? err : err?.code ?? null,
      });
    }
    if (helpFirst.length >= c.maxHelpFirst) break;
  }

  // ---- citation gate: nothing uncited reaches the teacher -----------------
  for (const a of [...stations, opening, closing].filter(Boolean)) {
    if (!isCited(a)) reasons.push(`activity ${a.blockId} is not cited (ncertRef + cbseFln required)`);
  }

  if (reasons.length) return fail(reasons);

  return {
    ok: true,
    reasons: [],
    plan: {
      date,
      chapterId,
      packVersion: pack.packVersion ?? null,
      totalMinutes: c.totalMinutes,
      openingMinutes: c.openingMinutes,
      closingMinutes: c.closingMinutes,
      workMinutes: scheduledMinutes,
      rotations,
      minutesPerRotation,
      bands: bands.map((b) => ({
        bandId: b.id,
        domain: b.domain,
        level: b.level,
        n: b.childIds.length,
        childIds: [...b.childIds],
      })),
      opening: { ...opening, minutes: c.openingMinutes, bandId: null },
      stations,
      teacherFocus,
      closing: { ...closing, minutes: c.closingMinutes, bandId: null },
      helpFirst,
      warnings,
    },
  };
}
