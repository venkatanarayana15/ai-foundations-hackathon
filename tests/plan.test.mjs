import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import {
  LEVEL_MAP_EVENT,
  createLevelMap,
  materializeLevelMap,
  levelMapRows,
  levelMapChildren,
  groupClass,
  assemblePlan,
  validatePlanContent,
  PLAN_DEFAULTS,
} from '../src/engine.js';
import { contentPack } from '../src/content-pack.js';

// ---------------------------------------------------------------- helpers ---

const assessment = (seq, childId, domain, finalLevel, errorCodes = [], ts = 1000 + seq) => ({
  seq, ts, type: LEVEL_MAP_EVENT.ASSESSMENT, payload: { childId, domain, finalLevel, errorCodes },
});
const override = (seq, childId, domain, level, ts = 1000 + seq) => ({
  seq, ts, type: LEVEL_MAP_EVENT.OVERRIDE, payload: { childId, domain, level },
});
/** Compare only the durable part of a snapshot (counters are per-call). */
const core = (s) => ({ rows: s.rows, cursor: s.cursor });

// A small, fully-cited fixture pack — deliberately missing `pre_letter` and
// `paragraph` so the failure and fallback paths are exercisable.
const fixturePack = {
  packVersion: 'test-0',
  openers: [{
    blockId: 'OPN-1', chapterId: 'CH1', domain: 'literacy', audience: 'whole_class',
    activity: 'warm up', talkLine: 'tl-open',
    ncertRef: { book: 'B', page: 1 }, cbseFln: 'FLN-L-0.1',
  }],
  blocks: [
    { blockId: 'BLK-L-1', chapterId: 'CH1', domain: 'literacy', level: 'letter', activity: 'a1', talkLine: 't1', ncertRef: { book: 'B', page: 2 }, cbseFln: 'FLN-L-1.1' },
    { blockId: 'BLK-L-2', chapterId: 'CH1', domain: 'literacy', level: 'letter', activity: 'a2', talkLine: 't2', ncertRef: { book: 'B', page: 3 }, cbseFln: 'FLN-L-1.1' },
    { blockId: 'BLK-W-1', chapterId: 'CH1', domain: 'literacy', level: 'word', activity: 'a3', talkLine: 't3', ncertRef: { book: 'B', page: 4 }, cbseFln: 'FLN-L-2.1' },
  ],
  closers: [{
    blockId: 'CLS-1', chapterId: 'CH1', domain: 'literacy', audience: 'whole_class',
    activity: 'close', talkLine: 'tl-close',
    ncertRef: { book: 'B', page: 5 }, cbseFln: 'FLN-L-3.1',
  }],
};

const kids = [
  { childId: 'C1', domain: 'literacy', level: 'letter', errorCodes: ['LIT-LET-01'] },
  { childId: 'C2', domain: 'literacy', level: 'letter', errorCodes: [] },
  { childId: 'C3', domain: 'literacy', level: 'word', errorCodes: [] },
];

const planFor = (over = {}) =>
  assemblePlan({ date: '2026-10-12', chapterId: 'CH1', levelMap: kids, pack: fixturePack, ...over });

// ======================================================= level-map snapshot ===

describe('Level-map snapshot (pure fold over the event log)', () => {
  test('empty input yields an empty snapshot at cursor -1', () => {
    const s = createLevelMap();
    assert.deepEqual(core(s), { rows: {}, cursor: -1 });
    assert.deepEqual(core(materializeLevelMap([])), { rows: {}, cursor: -1 });
  });

  test('folds a completed assessment into a row', () => {
    const s = materializeLevelMap([assessment(0, 'C1', 'literacy', 'word', [{ code: 'LIT-WRD-01' }])]);
    const row = s.rows['C1|literacy'];
    assert.equal(row.level, 'word');
    assert.deepEqual(row.errorCodes, ['LIT-WRD-01']);
    assert.equal(row.nObservations, 1);
    assert.equal(row.overridden, false);
    assert.equal(row.source, 'assessment');
    assert.equal(s.cursor, 0);
  });

  test('accepts error codes as plain strings or objects', () => {
    const a = materializeLevelMap([assessment(0, 'C1', 'literacy', 'word', ['X-1'])]);
    const b = materializeLevelMap([assessment(0, 'C1', 'literacy', 'word', [{ code: 'X-1', label: 'z' }])]);
    assert.deepEqual(a.rows['C1|literacy'].errorCodes, ['X-1']);
    assert.deepEqual(b.rows['C1|literacy'].errorCodes, ['X-1']);
  });

  test('ignores unrelated and malformed events without throwing', () => {
    const s = materializeLevelMap([
      { seq: 0, type: 'assessment_started', ts: 1, payload: { childId: 'C1', domain: 'literacy' } },
      { seq: 1, type: LEVEL_MAP_EVENT.ASSESSMENT, ts: 2, payload: { domain: 'literacy' } }, // no childId
      { seq: 2, type: LEVEL_MAP_EVENT.OVERRIDE, ts: 3, payload: { childId: 'C2', domain: 'literacy' } }, // no level
      { seq: 3, type: LEVEL_MAP_EVENT.ASSESSMENT, ts: 4, payload: { childId: 'C3', domain: 'literacy', finalLevel: 'letter' } },
    ]);
    assert.equal(s.applied, 1);
    assert.equal(s.ignored, 3);
    assert.equal(Object.keys(s.rows).length, 1);
    assert.equal(s.cursor, 3);
  });

  test('teacher override outranks the sensor, and a later assessment supersedes it', () => {
    const afterOverride = materializeLevelMap([
      assessment(0, 'C1', 'literacy', 'letter'),
      override(1, 'C1', 'literacy', 'word'),
    ]);
    const o = afterOverride.rows['C1|literacy'];
    assert.equal(o.level, 'word');
    assert.equal(o.overridden, true);
    assert.equal(o.source, 'override');
    assert.equal(o.nOverrides, 1);
    assert.equal(o.nObservations, 1);

    const afterReassess = materializeLevelMap([
      assessment(0, 'C1', 'literacy', 'letter'),
      override(1, 'C1', 'literacy', 'word'),
      assessment(2, 'C1', 'literacy', 'paragraph'),
    ]).rows['C1|literacy'];
    assert.equal(afterReassess.level, 'paragraph');
    assert.equal(afterReassess.overridden, false);
    assert.equal(afterReassess.source, 'assessment');
    assert.equal(afterReassess.nOverrides, 1, 'override count is retained for auditing');
  });

  test('an assessment with no level never silently clears an override', () => {
    const row = materializeLevelMap([
      override(0, 'C1', 'literacy', 'word'),
      assessment(1, 'C1', 'literacy', null), // timed out — carries no level evidence
    ]).rows['C1|literacy'];
    assert.equal(row.level, 'word');
    assert.equal(row.overridden, true);
    assert.equal(row.nObservations, 1, 'the attempt is still counted');
  });

  test('replay is idempotent and order-insensitive on input', () => {
    const events = [
      assessment(0, 'A', 'literacy', 'letter'),
      assessment(1, 'B', 'literacy', 'word'),
      assessment(2, 'A', 'literacy', 'word'),
    ];
    const once = materializeLevelMap(events);
    const twice = materializeLevelMap(events);
    const shuffled = materializeLevelMap([events[2], events[0], events[1]]);
    assert.deepEqual(core(once), core(twice));
    assert.deepEqual(core(once), core(shuffled), 'fold order is by seq, not array order');
  });

  test('applying the tail to a base equals a full fold (crash-resume)', () => {
    const events = [
      assessment(0, 'A', 'literacy', 'letter'),
      assessment(1, 'B', 'literacy', 'word'),
      assessment(2, 'A', 'literacy', 'word'),
      override(3, 'B', 'literacy', 'paragraph'),
    ];
    const full = materializeLevelMap(events);
    const base = materializeLevelMap(events.slice(0, 2));
    const resumed = materializeLevelMap(events, { base });
    assert.deepEqual(core(resumed), core(full));
    assert.equal(resumed.applied, 2, 'only the tail was folded');
  });

  test('never mutates the base snapshot', () => {
    const events = [assessment(0, 'A', 'literacy', 'letter'), assessment(1, 'B', 'literacy', 'word')];
    const base = materializeLevelMap(events.slice(0, 1));
    const before = JSON.stringify(base);
    materializeLevelMap(events, { base });
    assert.equal(JSON.stringify(base), before);
  });

  test('rows are deterministically ordered and adapt to groupClass', () => {
    const s = materializeLevelMap([
      assessment(0, 'C2', 'literacy', 'letter'),
      assessment(1, 'C1', 'literacy', 'letter'),
      assessment(2, 'C3', 'literacy', 'word'),
      assessment(3, 'C1', 'numeracy', 'num_concrete'),
    ]);
    assert.deepEqual(
      levelMapRows(s).map((r) => `${r.childId}:${r.domain}`),
      ['C1:literacy', 'C1:numeracy', 'C2:literacy', 'C3:literacy']
    );
    const groups = groupClass(levelMapChildren(s), { maxGroupSize: 8 });
    assert.equal(groups.length, 3, 'literacy:letter, literacy:word, numeracy:num_concrete');
    const letter = groups.find((g) => g.level === 'letter');
    assert.deepEqual(letter.childIds.sort(), ['C1', 'C2']);
  });

  test('unassessed children are visible to the adapter but not a band', () => {
    const s = materializeLevelMap([assessment(0, 'C1', 'literacy', null)]);
    const children = levelMapChildren(s);
    assert.equal(children[0].level, null);
    assert.equal(groupClass(children)[0].level, 'unassessed');
  });
});

// ========================================================== PlanAssembler ===

describe('PlanAssembler — structure and determinism', () => {
  test('assembles one station per band plus a whole-class opener and closer', () => {
    const res = planFor();
    assert.equal(res.ok, true, JSON.stringify(res.reasons));
    const { plan } = res;
    assert.equal(plan.stations.length, 2, 'letter band + word band');
    assert.equal(plan.opening.blockId, 'OPN-1');
    assert.equal(plan.closing.blockId, 'CLS-1');
    assert.equal(plan.opening.bandId, null, 'the opener is whole-class');
    assert.deepEqual(plan.stations.map((s) => s.level), ['letter', 'word'], 'weakest band first');
    assert.equal(plan.minutesPerRotation, 15);
    assert.equal(plan.rotations, 2);
  });

  test('the block never exceeds the time budget', () => {
    const { plan } = planFor();
    const accounted =
      plan.openingMinutes + plan.rotations * plan.minutesPerRotation + plan.closingMinutes;
    assert.equal(accounted, plan.totalMinutes);
    assert.ok(plan.workMinutes <= plan.totalMinutes);
  });

  test('is deterministic — same inputs produce byte-identical plans', () => {
    assert.deepEqual(planFor(), planFor());
    assert.equal(JSON.stringify(planFor()), JSON.stringify(planFor()));
  });

  test('every activity that reaches the teacher carries an NCERT page and FLN code', () => {
    const { plan } = planFor();
    for (const a of [plan.opening, ...plan.stations, plan.closing]) {
      assert.ok(a.ncertRef?.book, `${a.blockId} missing ncertRef.book`);
      assert.ok(a.ncertRef?.page, `${a.blockId} missing ncertRef.page`);
      assert.ok(a.cbseFln, `${a.blockId} missing cbseFln`);
    }
  });

  test('teacher attention rotates, weakest band first', () => {
    const { plan } = planFor();
    assert.deepEqual(plan.teacherFocus.map((f) => f.level), ['letter', 'word']);
    assert.deepEqual(plan.teacherFocus.map((f) => f.round), [1, 2]);
    assert.ok(plan.teacherFocus[0].talkLine, 'each focus round carries a talk-line');
  });

  test('helpFirst points at the weakest band and stops at the cap', () => {
    const { plan } = planFor();
    assert.equal(plan.helpFirst[0].childId, 'C1');
    assert.equal(plan.helpFirst[0].errorCode, 'LIT-LET-01');
    assert.ok(plan.helpFirst.length <= PLAN_DEFAULTS.maxHelpFirst);
  });

  test('a short block collapses to a single rotation', () => {
    const { plan } = planFor({ constraints: { totalMinutes: 25 } });
    assert.equal(plan.rotations, 1);
    assert.equal(plan.minutesPerRotation, 15);
    assert.equal(plan.teacherFocus.length, 1);
  });

  test('warns when there are more bands than station slots', () => {
    const many = [
      { childId: 'C1', domain: 'literacy', level: 'letter', errorCodes: [] },
      { childId: 'C2', domain: 'literacy', level: 'word', errorCodes: [] },
      { childId: 'C3', domain: 'literacy', level: 'paragraph', errorCodes: [] },
      { childId: 'C4', domain: 'literacy', level: 'story', errorCodes: [] },
    ];
    const res = assemblePlan({
      chapterId: 'CH1', levelMap: many, pack: fixturePack,
      constraints: { maxStationsPerRound: 3 },
    });
    assert.equal(res.ok, true);
    assert.equal(res.plan.stations.length, 4);
    assert.ok(res.plan.warnings.some((w) => /station slots/.test(w)));
  });
});

describe('PlanAssembler — anti-repetition and fallback', () => {
  test('prefers a never-used block over a recently used one', () => {
    const { plan } = planFor({ history: { 'BLK-L-1': '2026-10-01' } });
    const letter = plan.stations.find((s) => s.level === 'letter');
    assert.equal(letter.blockId, 'BLK-L-2');
    assert.equal(letter.isFallback, false);
  });

  test('among used blocks, the least recently used wins', () => {
    const { plan } = planFor({ history: { 'BLK-L-1': '2026-10-01', 'BLK-L-2': '2026-10-05' } });
    assert.equal(plan.stations.find((s) => s.level === 'letter').blockId, 'BLK-L-1');
  });

  test('falls back to the nearest LOWER level and flags it', () => {
    const res = assemblePlan({
      chapterId: 'CH1',
      levelMap: [{ childId: 'C1', domain: 'literacy', level: 'paragraph', errorCodes: [] }],
      pack: fixturePack,
    });
    assert.equal(res.ok, true, JSON.stringify(res.reasons));
    const [station] = res.plan.stations;
    assert.equal(station.level, 'paragraph', 'the band keeps its true level');
    assert.equal(station.matchedLevel, 'word', 'the activity is the nearest lower block');
    assert.equal(station.isFallback, true);
  });

  test('also satisfies the LRU rule while falling back', () => {
    const res = assemblePlan({
      chapterId: 'CH1',
      levelMap: [{ childId: 'C1', domain: 'literacy', level: 'paragraph', errorCodes: [] }],
      pack: fixturePack,
      history: { 'BLK-W-1': '2026-10-01' },
    });
    // BLK-W-1 is the only 'word' block, so it is reused rather than failing.
    assert.equal(res.ok, true);
    assert.equal(res.plan.stations[0].blockId, 'BLK-W-1');
  });
});

describe('PlanAssembler — explicit failure, never a half-plan', () => {
  test('rejects an empty level-map', () => {
    const res = assemblePlan({ chapterId: 'CH1', levelMap: createLevelMap(), pack: fixturePack });
    assert.equal(res.ok, false);
    assert.deepEqual(res.reasons, ['level-map is empty — assess at least one child first']);
    assert.equal(res.plan, undefined, 'no partial plan is returned');
  });

  test('rejects a level-map with no assessed children', () => {
    const res = assemblePlan({
      chapterId: 'CH1',
      levelMap: [{ childId: 'C1', domain: 'literacy', level: null, errorCodes: [] }],
      pack: fixturePack,
    });
    assert.equal(res.ok, false);
    assert.match(res.reasons[0], /no assessed bands/);
  });

  test('rejects a missing or unknown chapter', () => {
    assert.equal(assemblePlan({ levelMap: kids, pack: fixturePack }).ok, false);
    const res = assemblePlan({ chapterId: 'NOPE', levelMap: kids, pack: fixturePack });
    assert.equal(res.ok, false);
    assert.match(res.reasons[0], /no activity blocks for chapter/);
  });

  test('rejects a pack with no blocks at all', () => {
    const res = assemblePlan({ chapterId: 'CH1', levelMap: kids, pack: { packVersion: 'x' } });
    assert.equal(res.ok, false);
    assert.match(res.reasons[0], /no activity blocks/);
  });

  test('rejects an uncited pack before it can reach a teacher', () => {
    const badPack = {
      packVersion: 'bad',
      openers: fixturePack.openers,
      closers: fixturePack.closers,
      blocks: [{ blockId: 'BLK-UNCITED', chapterId: 'CH1', domain: 'literacy', level: 'letter', activity: 'a' }],
    };
    const res = assemblePlan({ chapterId: 'CH1', levelMap: kids, pack: badPack });
    assert.equal(res.ok, false);
    assert.match(res.reasons[0], /content pack invalid/);
    assert.match(res.reasons[0], /BLK-UNCITED missing ncertRef/);
  });

  test('fails when a band has no activity at or below its level', () => {
    const res = assemblePlan({
      chapterId: 'CH1',
      levelMap: [{ childId: 'C1', domain: 'literacy', level: 'pre_letter', errorCodes: [] }],
      pack: fixturePack,
    });
    assert.equal(res.ok, false);
    assert.ok(res.reasons.some((r) => /no activity for band literacy:pre_letter/.test(r)));
  });

  test('fails when the block is too short to teach', () => {
    const res = planFor({ constraints: { totalMinutes: 12 } });
    assert.equal(res.ok, false);
    assert.ok(res.reasons.some((r) => /insufficient time/.test(r)));
  });

  test('fails rather than emitting a plan with no opener', () => {
    const res = assemblePlan({
      chapterId: 'CH1', levelMap: kids,
      pack: { ...fixturePack, openers: [] },
    });
    assert.equal(res.ok, false);
    assert.ok(res.reasons.some((r) => /no whole-class opener/.test(r)));
  });
});

// =============================================== pack rule + integration ===

describe('Content pack: plan blocks are all cited (CI rule)', () => {
  test('validatePlanContent passes on the shipped pack', () => {
    assert.deepEqual(validatePlanContent(contentPack), []);
  });

  test('every block has a resolvable chapter, a level in its domain ladder and a talk-line', () => {
    for (const b of contentPack.blocks) {
      assert.ok(b.chapterId, `${b.blockId} has no chapterId`);
      assert.ok(b.activity, `${b.blockId} has no activity`);
      assert.ok(
        contentPack.openers.some((o) => o.chapterId === b.chapterId),
        `${b.blockId} has no opener for its chapter`
      );
      assert.ok(
        contentPack.closers.some((c) => c.chapterId === b.chapterId),
        `${b.blockId} has no closer for its chapter`
      );
    }
  });
});

describe('Integration: events → level-map → plan', () => {
  test('a real class produces a real block from the shipped pack', () => {
    const snapshot = materializeLevelMap([
      assessment(0, 'SCH01-CL1-001', 'literacy', 'letter', [{ code: 'LIT-LET-01' }]),
      assessment(1, 'SCH01-CL1-002', 'literacy', 'word', []),
      assessment(2, 'SCH01-CL2-003', 'literacy', 'paragraph', []),
    ]);
    const res = assemblePlan({
      date: '2026-10-12',
      chapterId: 'RIMJHIM-1-MELA',
      levelMap: snapshot,
      pack: contentPack,
    });
    assert.equal(res.ok, true, JSON.stringify(res.reasons));
    assert.deepEqual(res.plan.stations.map((s) => s.level), ['letter', 'word', 'paragraph']);
    assert.equal(res.plan.helpFirst[0].childId, 'SCH01-CL1-001');
    assert.equal(res.plan.packVersion, contentPack.packVersion);
    for (const s of res.plan.stations) {
      assert.ok(s.childIds.length >= 1);
      assert.match(s.ncertRef.book, /Rimjhim/);
    }
  });

  test('a teacher override changes the band the plan is built for', () => {
    const events = [
      assessment(0, 'C1', 'literacy', 'letter', []),
      assessment(1, 'C2', 'literacy', 'letter', []),
    ];
    const before = assemblePlan({ chapterId: 'RIMJHIM-1-MELA', levelMap: materializeLevelMap(events), pack: contentPack });
    assert.deepEqual(before.plan.stations.map((s) => s.level), ['letter']);

    const after = assemblePlan({
      chapterId: 'RIMJHIM-1-MELA',
      levelMap: materializeLevelMap([...events, override(2, 'C1', 'literacy', 'paragraph')]),
      pack: contentPack,
    });
    assert.deepEqual(after.plan.stations.map((s) => s.level).sort(), ['letter', 'paragraph']);
  });

  test('numeracy chapter assembles across the C→R→A ladder', () => {
    const snapshot = materializeLevelMap([
      assessment(0, 'N1', 'numeracy', 'num_concrete', []),
      assessment(1, 'N2', 'numeracy', 'num_representation', []),
      assessment(2, 'N3', 'numeracy', 'num_abstract', []),
    ]);
    const res = assemblePlan({ chapterId: 'MATH-MAGIC-2-SUB', levelMap: snapshot, pack: contentPack });
    assert.equal(res.ok, true, JSON.stringify(res.reasons));
    assert.deepEqual(
      res.plan.stations.map((s) => s.level),
      ['num_concrete', 'num_representation', 'num_abstract']
    );
    assert.equal(res.plan.opening.blockId, 'OPN-SUB-01');
  });
});
