# 🏛️ Samanantar — Technical Documentation v4 (24 Sep 2026)

**Challenge 02 - Learning-Level Visibility.** Per-child diagnostic visibility: *the teacher cannot see where each child actually stands.*

> The assessment ladder is the **sensor**, the frontier model is the **diagnosis**, and the NCERT page is the **plan**.

---

## 1. What the system does

| Stage | Job | How |
|---|---|---|
| **Sense** | Where is each child, really? | 3-min voice check → on-device Indic ASR → transcript + confidence |
| **Diagnose** | Which band, which misconception? | Deterministic matcher + error classifier (ASER thresholds) |
| **Group** | Who works together? | TaRL bands, max 8, regroup weekly |
| **Plan** | What does the teacher do for 40 minutes? | Claude + NCERT retrieval (online) or deterministic PlanAssembler (offline) |
| **Run** | Station cards, timer, talk-lines, "help first" | Teacher UI |
| **Log** | What actually happened? | Append-only event log; weekly regroup |

---

## 2. Architecture

Diagram: [`docs/data-flow.svg`](docs/data-flow.svg) (source: [`docs/data-flow.mmd`](docs/data-flow.mmd)) · Detail: [`ARCHITECTURE_OFFLINE.md`](ARCHITECTURE_OFFLINE.md)

```
Teacher UI (Hindi-first, 3 taps to a plan)
  └── Orchestrator (pure, deterministic)
        ├── LevelMap     — materialised view over the event log
        ├── Grouping     — TaRL bands, max 8
        └── PlanAssembler— Tier A: composes pre-validated blocks
  └── Sensor:    VAD → Indic ASR (INT8, on-device) → transcript + confidence
  └── Planner:   Claude + NCERT retrieval → schema-validated rotation  [online only]
                 → VALIDATOR (citation + time budget) → Plan Cache
  └── Storage:   append-only event log (SQLCipher) · level-map snapshot
                 · signed content pack · plan cache
  └── Sync:      optional, opt-in, upload-only, cursor + gzip, batch 500
```

**Two AI touchpoints and only two:** ASR on the device, Claude in the cloud. Everything between them — matching, diagnosis, the level-map fold, offline plan assembly — is deterministic, pure and unit-tested. Diagnosis is deliberately **not** an LLM, so the auditable part stays auditable.

---

## 3. The two modules that carry the design (`src/engine.js`)

### 3.1 Level-map — a pure fold over events

The event log is the source of truth; the level-map is a **disposable, rebuildable view**. Corrupt snapshot → delete and replay. Because events are immutable and ordered by `seq`, replay is idempotent and sync never needs merge logic.

```js
createLevelMap()                                  // { rows, cursor: -1, applied, ignored }
materializeLevelMap(events, { base })             // pure; pass base to fold only the tail
levelMapRows(snapshot)                            // deterministic order (childId, domain)
levelMapChildren(snapshot)                        // adapter for groupClass / classHeatmap
```

*Policy:* **last event wins.** `overridden` means the level in force came from a teacher correction. A teacher override outranks the model; a *later* assessment is fresh evidence and supersedes it. An assessment with no recorded level never silently clears an override.

### 3.2 PlanAssembler — deterministic offline planning

```js
assemblePlan({ date, chapterId, levelMap, pack, constraints, history })
  → { ok: true, plan } | { ok: false, reasons }     // never a half-plan
```

1. Resolve bands from the level-map (`groupClass`, max 8), **weakest band first**
2. Pick a whole-class opener and closer for the chapter
3. Per band, pick an activity at the exact level — else the nearest **lower** level, flagged `isFallback` — preferring the least recently used block (anti-repetition)
4. Time plan is structural: `opening + rotations × minutesPerRotation + closing ≤ totalMinutes`
5. Teacher attention rotates weakest-band-first; `helpFirst` names the 2–3 children whose error pattern is most urgent
6. **Citation gate:** every activity must carry `ncertRef{book,page}` + `cbseFln`, or the whole plan fails

**Safety invariant:** offline, this can only emit pre-validated blocks. There is no generative step, so there is no hallucination surface. The same citation rule guards Claude's output, so both tiers meet one standard.

---

## 4. Offline tiers

Connectivity is needed **only** to generate a plan that has never been generated before.

| Tier | Condition | Assessment | Plan |
|---|---|---|---|
| 3 | Online | full ASR | Claude generates; cached |
| 2 | Offline, model present | full ASR | PlanAssembler from validated blocks |
| 1 | Offline, model missing | tap-only | PlanAssembler, coarser bands |
| 0 | Nothing installed | paper export | printable template |

Model budgets, storage maths, failure-mode tests and the device matrix: [`ARCHITECTURE_OFFLINE.md`](ARCHITECTURE_OFFLINE.md) §4, §6, §9.

---

## 5. Content pack contract

`src/content-pack.js` · Python mirror `content_pack.json` v1.3.0

- **Items** — 8+ assessment items across Pre-Letter→Story and Concrete→Abstract, each with `target`, `ncertRef{book,page}`, `cbseFln`, `acceptsTapFallback`, `cra`
- **Error codes** — misconception, NCERT fix, TaRL grouping, C→R→A hint
- **Plan blocks** — `openers` / `blocks` / `closers`, each with `chapterId`, `level`, `activity`, a Hindi `talkLine`, `ncertRef` and `cbseFln`
- **CI rule:** `validatePlanContent()` and the Python pack check fail the build if any entry is uncited. *Enforced by test, not by trust.*

---

## 6. Testing — 74 passing tests

| Suite | Covers |
|---|---|
| `tests/unit.test.mjs` | ASR matching, adaptive ladder and stop rules, error taxonomy, TaRL grouping, dashboard, event store, pilot statistics (MDES, κ, TOST), CSV export |
| `tests/plan.test.mjs` | Level-map fold: idempotence, crash-resume, override precedence, adapters. PlanAssembler: determinism, time budget, anti-repetition, level fallback, teacher focus, help-first, and every explicit failure path. Pack CI rule. End-to-end events → level-map → plan |
| `tests/simulator.mjs` | Synthetic 45-child classroom: right-skewed ability, bursty 40–60 dB ASR channel, 12% silence, teacher override, interruption, kill-and-resume |

```bash
npm test      # 74 tests
npm run sim   # classroom simulation
```

Note the honesty boundary: the simulator models the ASR **channel statistically**. It is not a real ASR model and must not be presented as one.

---

## 7. Privacy & safeguarding

Pseudonymous child IDs (`SCH01-CL2-017`) — **the app never accepts a child's name**; no photos; **audio discarded after inference**; SQLCipher at rest with a per-install key in the Android Keystore; assess in the teacher's view, never alone; written parental consent (hi + en, `consent_template.txt`); opt-in sync, upload-only, switchable off with **zero feature loss**.

---

## 8. Status — what exists and what does not

**Exists and is tested:** the pure engine (ladder, grouping, error taxonomy, level-map fold, PlanAssembler), the content pack with CI-enforced citations, the simulator, the Streamlit prototype, the pilot pre-registration and the frozen analysis script.

**Does not exist yet (the critical path):**
- the **real Claude call site and its validator** — the LLM layer is the highest-weighted technical gap
- **real on-device Indic ASR** — model variant, INT8 export path and licence still to be confirmed and benchmarked on a 1–2 GB device
- the offline Android/PWA client — the Python prototype is a design reference

**Not claimed:** no learning-gain results. Three weeks cannot produce them; this repository contains no measurement that would justify the claim.

---

## 9. Run

```bash
npm test                                   # engine + plan tests
npm run sim                                # classroom simulation

pip install -r requirements.txt
streamlit run app.py                       # prototype: load demo class → room map → block
```
