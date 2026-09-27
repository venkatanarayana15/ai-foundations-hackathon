# 🏆 Full Hackathon Winning Plan: Samanantar — v2

> ## ⚠️ SUPERSEDED FOR SUBMISSION — read this first (24 Sep 2026)
>
> This document was written for the **Learning-Level Visibility** framing. The team has since
> locked **Challenge 02 - Learning-Level Visibility** (child-level diagnostic visibility). Track choice is frozen
> after the Ideate stage (Guidelines §3.5), so where this file disagrees with the following,
> these win:
>
> * [`TRACK_DECISION.md`](TRACK_DECISION.md) — rubric-weighted track decision and evidence
> * [`IDEATE_DECK.md`](IDEATE_DECK.md) — the 9-slide submitted proposal
> * [`ARCHITECTURE_OFFLINE.md`](ARCHITECTURE_OFFLINE.md) — the on-device design
> * [`README.md`](README.md) — the public framing
>
> **What still carries over from this document:** the diagnostic ladder, TaRL grouping,
> the NCERT/CBSE citation rule, the evidence plan (cluster-randomised, honestly powered),
> the ethics and consent position, the fidelity instrument, and the risk register.
>
> **What does not:** the track, the pitch narrative, and the assessment-led framing.
> `plam.md` is retained as the reasoning archive, not as the submission.

> **What changed in v2** (deep audit, 2026-09-21):
> 1. ❌→✅ Duplicate "Section 6" removed; merged into one action list with owners.
> 2. ❌→✅ **K5 reading gap** (ASER's floor: can't read letters, can't recognize own name) added to ladder.
> 3. ❌→✅ **10-second name/letter screener** (ASER-style entry gate) added — biggest time saver.
> 4. ❌→✅ **Stats fixed**: 75 kids is underpowered for individual randomization → **cluster (classroom-level) randomization** + power table; pre-registration with power calc; two one-sided TOST equivalence for "no loss of info" claim; quadratic-weighted kappa (agreement, not just accuracy); stop rule ≥1.0 pp/min.
> 5. ❌→✅ **Control contamination protocol** added (control-class testing done on paper only, experimenters briefed, control classrooms excluded from app visibility).
> 6. ❌→✅ **IRB/consent** section added: written parental consent, encrypted-at-rest DB (SQLCipher), no child photos/PII, safeguarding (assess in view of teacher, never alone).
> 7. ❌→✅ **Offline architecture defined** (Section 3.0): append-only event store + content pack + queues; **448-Batch AES-GCM** row encryption.
> 8. ❌→✅ **Numeracy C-P-A sequence corrected** (Concrete → Representational → Abstract); place-value & composing/decomposing added (biggest G2 gap in ASER 2024 numeracy).
> 9. ❌→✅ **Fidelity instrument** defined (5-item implementation log) — dashboards can't invent data nobody recorded.
> 10. ❌→✅ **Pilot schedule fixed** (phase conflict): RCT runs Weeks 6–8, Dashboards ship Week 8 (after data), Sub mission prep Week 9, buffer Week 9–10.
> 11. ❌→✅ **Sync contract** specified (below) — "optional sync" was too vague to implement.
> 12. ❌→✅ **Language scope narrowed** to Hindi + one more (Marathi/Telugu) for pilot; others out of scope for judges' honesty.
> 13. ❌→✅ **Impact claims tempered** (J-PAL/TaRL evidence shows remediation works; claiming 35% vs 15% without a pilot = fabrication risk).
> 14. ❌→✅ **Whisper variant corrected**: IndicWhisper/IndicConformer; IndicASR is the project umbrella.
> 15. ❌→✅ **Testing = mandatory**: judge-run **classroom simulator** (Phase 2) with synthetic class of 45 kids & noise profiles; all module boundaries unit-tested; E2E on 2 low-end devices (Android 8, 1–2 GB RAM).

---

## 0. One-Page Executive Summary (for judges)

**Problem.** ASER 2024: >50% of Grade 5 students can't read Grade 2 text; foundational gap is invisible to the teacher mid-year. Existing tools (paper ASER, PadhAI) give a level but no "what to do tomorrow at the child's level."
**Solution.** Samanantar: offline-first Android app. Teacher runs a 3–5 min diagnostic (voice + tap), gets ASER level, error code, and a tomorrow-morning activity mapped to NCERT pages + CBSE FLN skills.
**Evidence plan.** Cluster-randomized pilot in 2 schools (4 classrooms, N≈90–120): Samanantar vs. status-quo paper. Pre-registered endpoints: reading-level gain, teacher minutes/child, fidelity (usage, override, completion).
**Key design bet.** The app is a **TaRL layer on existing NCERT/CBSE content** — not new content. ₹0 marginal cost/child; works offline; syncs when connectivity exists.

---

## 1. The Winning Strategy
To win, we must prove **causal impact** within 10 weeks using only **brief-provided resources**.
*   **Track:** **Challenge 02 - Learning-Level Visibility** (child-level diagnostic visibility; the three named needs are quoted on slide 1).
*   **Solution:** Samanantar — offline-first, voice-first orchestration of the daily differentiated block. Assessment is the **sensor**; the AI core is the **plan**.
*   **Winning Criteria:**
    1.  **Teacher-Centricity:** Saves time (≤5 mins/child vs. 10–15 mins paper) — measured with a stopwatch in-pilot, not assumed.
    2.  **Feasibility:** Works offline on low-end phones in noisy classrooms — verified in the classroom simulator + 2 low-end devices.
    3.  **Evidence:** Pilot data showing learning gains (cluster-randomized, pre-registered, cleaned dataset released).
    4.  **Alignment:** Uses NCERT/CBSE/ASER/AI4Bharat only. Every remediation maps to a textbook page + FLN skill.

## 2. Resource Checklist (Strict Adherence)
| Asset | Usage | Proof in Pitch |
| :--- | :--- | :--- |
| **NCERT** | Source of remediation activities (e.g., Rimjhim Book 1; Math-Magic 1–3) | Screenshots of app mapping errors to specific NCERT pages |
| **CBSE FLN** | Assessment framework & question banks | Alignment diagram showing how app items map to CBSE standards (Jadui Pitara for G1) |
| **ASER** | Metrics & benchmarks — **full ladder incl. Pre-letter/K5** | Pre/Post charts using ASER-aligned levels (Pre-letter → Letter → Word → Paragraph → Story) |
| **AI4Bharat** | ASR models — **IndicWhisper / IndicConformer** (IndicASR is the project umbrella) | Technical 1-pager citing exact variant + WER/CER numbers from our noise tests |
| **J-PAL/TaRL** | Pedagogical logic + **cluster-randomized design precedent** | Slide explaining "Teaching at the Right Level" implementation + pre-registration doc |

## 3. Architecture (NEW — was missing)

### 3.0 Offline-First Architecture
```
┌──────────────────────────────────────────────────────────┐
│  Android App (Kotlin) — works 100% offline               │
│                                                          │
│  UI (Compose)                                            │
│    └── ViewModel ──► Core Engine (pure Kotlin, testable) │
│                        ├── Ladder (K5→Story, Num C→A)    │
│                        ├── AsrOrchestrator (voice+tap,   │
│                        │   keyword fallback, 1-tap fix)  │
│                        ├── Grouping (TaRL bands)         │
│                        └── Remediation (pack lookup)     │
│                                                          │
│  Content Pack (versioned JSON+assets, signed, bundled)   │
│    NCERT activity pages · item banks · audio prompts     │
│                                                          │
│  Storage (encrypted, SQLCipher)                          │
│    └── Append-only Event Store:                          │
│        [childId, ts, eventType, payload, deviceId]       │
│        No PII. childId = pseudonymous.                   │
│                                                          │
│  Sync (optional, resumable, idempotent):                 │
│    upload: events since last cursor (gzip, batch 500)    │
│    download: content-pack manifest delta only            │
│    Conflict rule: events are immutable & append-only     │
│    → no merge needed; server is a mirror.                │
└──────────────────────────────────────────────────────────┘
```
**Key decision:** every interaction is an **event**, never a mutable row. A crashed battery mid-assessment resumes cleanly; analytics can be replayed; debugging is deterministic.

### 3.1 Content Pack Contract (Week 2 deliverable, before code)
`content-pack.schema.json`:
```json
{
  "packVersion": "1.2.0",
  "language": ["hi", "mr"],
  "items": [{
    "itemId": "LIT-W-003",
    "domain": "literacy",
    "level": "word",
    "target": "किताब",
    "expectedPhonemes": ["ki","taab"],
    "ncertRef": {"book":"Rimjhim-1","page":24},
    "cbseFln": "FLN-L-2.1 Blending akshars into words",
    "audioPrompt": "audio/hi/LIT-W-003.mp3",
    "acceptsTapFallback": true
  }],
  "errorCodes": [{
    "code": "MATH-01",
    "label": "forgets borrowing",
    "remediations": [{"ncertRef":"Math-Magic-2 p.45","craStage":"concrete"}],
    "taRL": "small-group, manipulatives first"
  }]
}
```
**Rule:** every item must have non-null `ncertRef` and `cbseFln` — enforced by a CI check, not by trust.

### 3.2 Sync Contract (was "sync is optional" — too vague)
*   **Upload only** (no content writes from server → teacher device).
*   Cursor-based, gzip, batch of 500 events; server ACKs cursor; resume safe.
*   Child IDs are pseudonymous (e.g., `SCH01-CL2-017`), no names ever leave device.
*   Opt-in per school in writing; can be disabled entirely with zero feature loss.

## 4. Execution Schedule — Aligned to Official Hackathon (27 Sept Ideate / 10 Oct–1 Nov Build)

> **Official timeline (hack2skill):** Ideate 7 Sept → **27 Sept deadline (idea proposal)** → Top 30 **10 Oct** → **Build 10 Oct–1 Nov (3 weeks)** → Top 10 **10 Nov** → Finale **18 Nov**. This plan is now compressed to that window. Earlier 10-week plan is archived.

### Phase 0: Foundation — Ideate Sprint (Now → 27 Sept) ⚡ *5 days*
*   **Team:** 2–4 members (Indian citizens, 18+), hybrid, register on hack2skill.
*   **Deliverable 27 Sept:** Idea deck (10 slides) + 2-min video + public GitHub (this repo) + Built With: `Claude 3.5 Sonnet, IndicWhisper/IndicConformer, Streamlit`.
*   **Deck must include:** Problem (ASER 7/10), User (Mrs Sharma 45 kids), Solution loop (3–5 min assess → NCERT p.XX), AI (hybrid + CER/WER), Resources (NCERT/CBSE/ASER/AI4Bharat), Evidence plan (cluster RCT + kappa/TOST), Feasibility (offline event-store).
*   **Ethics:** Consent templates (hi+en) ready by 26 Sept — see `consent_template.txt`.
*   **Device:** Borrow 1 low-end Android 8 1–2GB for video.

### Phase 1: Build Sprint — Weeks 1–3 (10 Oct–1 Nov) — *Only if Top 30*
*Goal: Ship working prototype + simulator + pilot prep. All code lands here.*

### Phase 1: Build — Assessment + Simulator (10–18 Oct, Week 1 of Build)
*   **Day 1–3:** Content pack v1.3.0 (already shipped: 8 items + 6 error codes, NCERT/CBSE per item, hi/mr) + ASR sandbox @40/50/60 dB (CER/WER separate, latency on low-end device).
*   **Day 4–7:** Literacy ladder Pre-Letter→Story + Numeracy C→R→A + hybrid voice+tap + 5-min cap + event store (offline, append-only) + classroom simulator (45 kids, 60dB, battery throttle, interruptions). Pass ≥90% stable ≤5 min, 0 crashes, resume after kill.

### Phase 2: Build — Intelligence + Dashboard (19–27 Oct, Week 2)
*   Error taxonomy 6→20 codes (4 layers: tech→NCERT→TaRL→CBSE) + teacher blind validation ≥85%.
*   Remediation C-R-A + grouping max 8/week + Dashboard (bench map + desk map + stickies + TOST/forest + streaks + absentee calendar + κ gauge) + Fidelity 5-item log.

### Phase 3: Build — Validation + Pitch (28 Oct–1 Nov, Week 3)
*   Cluster RCT pre-registration (OSF) with MDES 0.40 SD, primary: % ≥1 level + minutes/child, secondary: confidence + override + completion, TOST ±0.2 SD, κ≥0.75.
*   Assets: 2-min video (before/after + split-screen + pilot/sim data), 11-slide deck, 2-pager tech doc + simulator report. Rehearse 3× on low-end device, airplane-mode fallback.

### Phase 4: Finale (10–18 Nov) — if Top 10
*   Refine with mentor feedback (CSF/Anthropic), add Telugu pack if requested, polish offline APK, scale slide SCERT → 1,000 schools.

## 5. Risk Mitigation
| Risk | Probability | Mitigation Strategy |
| :--- | :--- | :--- |
| **ASR fails in noise** | High | Hybrid input (Touch + Voice) + Teacher override (1-tap). Test at 40/50/60 dB with real classroom audio. Report CER honestly. |
| **Schools cancel** | Medium | 2 backup schools; teacher certificates/stipends for time. |
| **Pilot underpowered / null** | **High (revised)** | Pre-register; report effect size + CI honestly; lead with teacher-time & TOST equivalence win. |
| **Control contamination** | Medium | Cluster randomization; no device in control rooms; deviation log. |
| **Content mismatch** | Medium | CI check: every item has NCERT page + FLN skill; teacher validation ≥85%. |
| **App crashes on low-end device** | Medium | Test on Android 8 / 1–2 GB RAM from Week 3, not Week 9; simulator pass criterion. |
| **Team member out sick** | Medium | Named backup per role; weekly doc sync. |
| **Consent/ethics gap** | Low | Consent forms ready by Week 2; IRB waiver letter; no PII ever stored. |

## 6. Pitch Narrative (claims tempered — see §A.2)
**Hook (Teacher Story - Before/After):**
> *"Before Samanantar, I taught Grades 1–3 together. I had 45 children but no way to know if Meera (Grade 2) could read letters or words. I guessed, taught to the middle. ASER says 7 in 10 children like Meera fall behind. Now, I open the app, assess Meera in 5 minutes, and see: 'Level: Word. Gap: Suffix blending. Next: Sound Matching (Rimjhim p.24).' I group her with 6 other 'Word level' children. In 2 weeks, Meera reads paragraphs."*

**Body (Evidence):**
> *"In our cluster-randomized pilot, teachers using Samanantar saved **X% time per child** (measured, not estimated). The app's reading-level judgments matched an independent blinded assessor at **κ = Y**. Teachers used the app **Z×/week**, completing **W% of recommended activities**. Where learning gains were positive, they were **[effect size] (95% CI [a,b])**."*
> *(Fill X, Y, Z, W from the pilot — never invent numbers.)*

**Close (Scale - Pedagogical Alignment):**
> *"This isn't a new system. It's a TaRL layer on top of NCERT and CBSE that works offline. Every activity maps to a specific textbook page and CBSE FLN skill. ₹0 marginal cost per child. Ready for SCERT rollout."*

## 7. Immediate Next Actions (merged — duplicate section removed)
| # | When | Action | Owner |
|---|------|--------|-------|
| 1 | Week 1 | School partnerships: 2 LOIs + 2 backups | Researcher |
| 2 | Week 1 | ASR noise test: IndicWhisper/IndicConformer, 30 samples, 40/50/60 dB, CER+WER | ML Engineer |
| 3 | Week 1 | Teacher interviews ×5 (30 min) + stopwatch baseline of paper assessment time | Researcher |
| 4 | Week 2 | Content-pack schema + 20 items/level × 2 languages with NCERT page refs | ML + Researcher |
| 5 | Week 2 | Error taxonomy spreadsheet v0 | Researcher |
| 6 | Week 2 | Figma mockup (heatmap + next best action) tested with 2 teachers | Mobile Dev |
| 7 | Week 2 | Consent forms + IRB waiver submitted | Researcher |
| 8 | Week 3 | Classroom simulator built; app runs against it nightly | Mobile Dev |
| 9 | Week 5 | Pre-registration doc drafted (endpoints, power table, analysis script) | Researcher |
| 10 | Week 6 | Pre-test + randomization executed (cluster-level, by an external coin-flip) | Researcher |

## Appendix A: Audit Log (what v1 got wrong)
1. **Duplicate §6** — two "Immediate Next Actions" sections with different lists. Merged.
2. **Overclaiming stats** — "35% vs 15%" was asserted before running a pilot. Fabrication risk if judges probe. Replaced with placeholders + a real power analysis (MDES ≈ 0.40 SD at this sample size with ICC 0.15).
3. **Contamination** — individual randomization inside one classroom is broken by design (kids share app). Switched to cluster randomization.
4. **Missing K5** — ASER floor is "can't read letters"; v1 ladder started at Letter. Added Pre-letter/name recognition.
5. **Phase conflict** — Dashboards (Wk 6–7) needed fidelity data that only the pilot (Wk 8–9) would generate. Interleaved now.
6. **"Sync optional"** — was un-implementable. Now a concrete event-store + cursor contract (§3.2).
7. **"LLM only rephrases"** — rephrasing can still distort meaning. Added teacher blind-validation of every mapping (≥85% agreement).
8. **No testing plan** — added simulator (45 synthetic kids + noise + battery throttle), unit tests on module boundaries, 2 low-end device checks, airplane-mode demo.
9. **Whisper variant** — "IndicASR" is a project name, not a model. Corrected to IndicWhisper/IndicConformer.
10. **"Offline-first" undefined** — now means: zero network code paths in assessment; all logic local; encrypted storage; resumable event log.
11. **Numeracy C-P-A** — was reversed in §3 of v1 (Abstract before Concrete). Fixed to C→R→A and moved place value earlier.
12. **Fidelity metrics without an instrument** — dashboards can't show data nobody records. Added the 5-item weekly log.
13. **Time-per-child** — was a claim; now a measured endpoint with a stop rule.
14. **No consent/ethics** — added §0/§4 ethics pre-clearance + no-PII guarantee.
