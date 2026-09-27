# 📚 Samanantar — every child seen, every child taught at the right level

> A teacher opens the app, assesses one child in 3–5 minutes, and sees the exact reading level, the one
> specific thing the child is getting wrong, and the textbook page that fixes it — offline, on the phone
> already in the classroom.

**Team A2Z** · **Challenge 02 — Learning-Level Visibility** · AI for Foundational Learning Hackathon 2026 (ShikshaNext × Anthropic)

![Challenge](https://img.shields.io/badge/challenge-02%20Learning--Level%20Visibility-0D9488)
![Team](https://img.shields.io/badge/team-A2Z-0F172A)
![Offline](https://img.shields.io/badge/offline--first-100%25%20local-brightgreen)
![Tests](https://img.shields.io/badge/tests-74%20passing-success)
![Pack](https://img.shields.io/badge/content--pack-NCERT%20%2B%20CBSE%20per%20item-informational)

---

## Status

| Item | State |
|---|---|
| Ideate proposal (9 content slides, PDF) | ✅ [`A2Z_Samanantar_Ideate_Proposal.pdf`](A2Z_Samanantar_Ideate_Proposal.pdf) — 31/31 instruction items verified |
| Working prototype (Streamlit) | ✅ `streamlit run app.py` — runs fully offline, no API key needed |
| AI layer with self-tests | ✅ `python ai.py`, `python engines.py` |
| JS engine + 74 tests | ✅ `npm test` — 74/74 passing |
| Pilot design (pre-registered protocol) | ✅ `preregistration.md` — cluster RCT, power calc, endpoints frozen before post-test |
| Demo video (3 min) | ⏳ To record for the Build stage |

---

## The problem

ASER 2024 finds that around **7 in 10 Grade 3 children cannot read a Grade 2-level text**. The gap is
measured every year — and it persists, because measurement and action have been decoupled. ASER needs a
trained assessor, 10–15 minutes per child, on paper: 45 children is nine hours of one-to-one time, so it
is done once, on a sample, and the result arrives months after the teaching decision it should have informed.

The official Challenge 02 statement names three things the teacher lacks. We answer all three:

| The challenge asks for insight into… | Samanantar returns… |
|---|---|
| **Where a lesson should begin** | A per-child ASER/EGRA level — Pre-Letter → Letter → Word → Paragraph → Story — in 3–5 minutes |
| **Which misconceptions need to be solved** | One named, coded misconception — not a score ("drops the long-i matra, so she is decoding, not reading") |
| **Which form of remediation support is required** | A Concrete→Representational→Abstract activity for that exact gap, on a named NCERT page, grouped into benches of max 8 |

> **Scope:** we solve one sub-part — child-level diagnostic visibility — not the whole challenge.
> (Guidelines §3.6 explicitly permits partial solutions.)

---

## The five-minute loop

1. **Screen (10 s)** — name-and-letter screener, the ASER "pre-letter" floor where most Grade 1–3 children sit.
2. **Listen (2–3 min)** — the child reads five laddered items; the teacher may tap instead of speak at any moment.
3. **Diagnose (<1 s)** — the AI step, invisible to the teacher: level, misconception, NCERT page, Hindi hint.
4. **Group (30 s)** — bench map by level band, never by grade; max 8 per bench, regrouped weekly.
5. **Teach (5 min)** — the suggested activity from the textbook already on her desk, plus a one-page parent note.

**₹0 marginal cost per child.** No new textbooks, no 1:1 devices, no network required.

---

## Where the AI is (what judges verify in source)

| Layer | Component | Role | Code |
|---|---|---|---|
| Perceives | **IndicWhisper / IndicConformer** (AI4Bharat), on-device | Child speech → Devanagari transcript + confidence | `ai.py` → model registry |
| Decides | **Claude** (Anthropic), forced tool call, temperature 0 | Level + misconception + NCERT page + Hindi hint + C-R-A stage | `ai.py` → `LlmDiagnostic._call_claude()` |
| Bounds | **Matra-weighted scorer** + 80% confidence gate | Refuses to judge a child on unreliable audio; a lost vowel sign counts 3× a lost consonant | `ai.py` → `AsrScorer` |
| Calibrates | **1PL / Rasch IRT**, damped Newton + Gaussian prior | Live item difficulty, next-item choice, early stop inside the 5-minute budget | `ai.py` → `DifficultyModel` |
| Grounds | **Versioned content pack, CI-validated** | Every item must carry a non-null NCERT page + CBSE FLN skill or the build fails | `content_pack.json` + CI |

**Guardrails:** the model may cite only the NCERT page it was given; below-80% confidence the app declines and
asks the teacher to tap; one-tap teacher override is always available and logged; offline, a documented rule
path takes over and the audit log records that it ran. Inspect it live in the app's **🧠 AI Lab** tab, or read
`ai.py` — every component carries its own self-test (`python ai.py`).

**Privacy:** pseudonymous roll IDs (never names), no photos, a local append-only event log, encrypted storage
at rest in the Android build, opt-in upload-only sync that can be switched off with zero feature loss.

---

## What's in this repo

| Path | What it is |
|---|---|
| `app.py` | Streamlit prototype UI (Dashboard · Assess · Children · Simulator · Fidelity · **AI Lab**) |
| `ai.py` | The AI layer: Claude tool-use + scorer + Rasch + TaRL grouping + `AI_AUDIT` |
| `engines.py` | Pure, testable engines (ladder, remediation lookup, pack validation) |
| `content_pack.json` | v1.3.0 pack: 8 items + 6 error codes, Hindi/Marathi/English prompts, every item NCERT- + CBSE-mapped |
| `A2Z_Samanantar_Ideate_Proposal.pdf` | The submitted Ideate proposal (9 content slides) |
| `build_ideate_proposal.py` | Regenerates the proposal PDF (ReportLab; audited slide-by-slide) |
| `audit_instructions.py` / `audit_submission.py` / `audit_ai_centrality.py` / `audit_layout.py` | The verification suite the submission was checked against |
| `src/` · `tests/` | JS engine mirror + 74 tests + 45-child classroom simulator (60 dB, silence, interruption, kill-and-resume) |
| `preregistration.md` · `analysis.py` | Frozen pilot protocol: cluster RCT, MDES ≈ 0.40 SD, κ ≥ 0.75, TOST ±0.2 SD |
| `technical_doc.md` | Offline-first architecture, ASR pipeline, error taxonomy, testing plan |
| `consent_template.txt` | Parental consent (Hindi + English) + safeguarding checklist |
| `SUBMISSION.md` · `GUIDELINES_COMPLIANCE.md` | Submission checklist + every guideline mapped to where it is satisfied |

---

## Quick start

**Prototype UI (no API key needed — runs fully offline on the deterministic path):**

```bash
pip install -r requirements.txt
streamlit run app.py
# click "Load demo class (90 kids)" for the bench map, then Assess → Voice/Tap → Diagnose
```

**With live Claude** (optional — switches diagnosis to the real model):

```bash
set ANTHROPIC_API_KEY=your-key-here   # Windows CMD — never commit this
streamlit run app.py
```

**Engines, AI layer and JS tests:**

```bash
python engines.py          # pure-engine self-tests
python ai.py               # AI-layer self-tests (scorer, Rasch, grouping, audit)
npm test                   # 74 tests: ladder, TaRL grouping, pack CI rule, simulator
npm run sim                # synthetic 45-child classroom simulation
```

**Regenerate the proposal PDF:**

```bash
python build_ideate_proposal.py   # -> A2Z_Samanantar_Ideate_Proposal.pdf
python audit_submission.py        # must print READY TO SUBMIT
```

> **Honesty note:** pilot numbers in the docs (effect sizes, κ, TOST) are pre-registered *targets*,
> not results. The protocol is frozen before the post-test; we report intervals, not breakthroughs.

---

## Resources this builds on (all brief-provided or public)

NCERT Rimjhim 1–2 + Math-Magic 1–2 · CBSE FLN toolkit & question banks · ASER basic reading & maths ·
EGRA / EGMA toolkits · AI4Bharat IndicWhisper & IndicConformer · J-PAL Teaching at the Right Level (2022).

**Training data: none, and that is deliberate.** No training on children's speech — open ASR weights plus a
content pack of public curriculum references. The only thing that learns from a child is one scalar per item
(Rasch difficulty): no audio, no text, no identifiers.

---

## Team

| Member | Role in this solution |
|---|---|
| **Venkata Narayana G V** | Founder & lead — product, pedagogy & engineering. Built the solution end to end. |
| **Mahesh Babu Ch** | Collaborator — review & domain input. Reviews the assessment flow and mappings for classroom practicality. |

## Licence

MIT — see [`LICENSE`](LICENSE). Team A2Z retains full IP (Guidelines §8); the code is open so it can be
inspected, adapted and reused for learners and educators (+USD 250 Claude credits per §8).
