# Stage 2 Build Stage Checklist — Samanantar (AI for Foundational Learning)

**Team A2Z - Challenge 02: Learning-Level Visibility**
**Deadline: 1 November 2026, 23:59** · Guidelines §4, Stage 2

---

## Submission deliverables

| # | Deliverable | Status | Notes |
|---|---|---|---|
| 1 | **Testable app link** + software to test | ✅ Done | Streamlit prototype: `pip install -r requirements.txt && streamlit run app.py` — runs offline, no API key needed |
| 2 | **GitHub source access** | ✅ Done | Public repository; judges can verify how AI is used |
| 3 | **3-minute demo video** (YouTube, public) | ⏳ To record | First 3:00 stands alone; 60-second fallback recorded |
| 4 | **Build stage proposal PDF** | ✅ Done | `Samanantar_Build_Proposal.pdf` — 9 content slides |
| 5 | **Short PowerPoint deck** | ⏳ To create | AI layers · guardrails · real-world · user testing · roadmap |

*Registration and compliance checklist in `stage2_checklist.md`.*

---

## Specific requirements mapped to repo artifacts

### 4.1 Effective AI use & technical strength
> *"Explain where AI/LLM calls are made in the solution and what they actually do. Show us the thinking in layers — data input, processing, guardrails, evaluation, output."*

| Layer | What happens | Where the code is |
|---|---|---|
| **Data input** | Content-pack item; 16 kHz audio or tap; teacher ID; noise level. No child name in the model context. | `app.py` assess wizard |
| **Processing (AI)** | IndicConformer transcribes on-device. Claude reads item + transcript + confidence + noise + override flag → structured diagnosis via forced tool call. | `ai.py` → `LlmDiagnostic._call_claude` |
| **Processing (non-AI)** | Matra-weighted scorer decides whether the transcript may judge the child. Rasch model decides next item and when to stop. | `ai.py` → `AsrScorer`, `DifficultyModel` |
| **Guardrails** | 80% confidence gate; matra weighting; forced tool schema; temperature 0; system rule forbidding any page the model was not given; conservative fallback when transcript unverified; one-tap teacher override; deterministic offline rule path; audit log recording which path ran. | `ai.py`, `DIAGNOSTIC_SYSTEM` |
| **Evaluation** | Quadratic-weighted κ ≥ 0.75 against blinded re-test on 20% of children; TOST equivalence ±0.2 SD vs paper; override rate; minutes per child by stopwatch; 45-child classroom simulator at 60 dB with battery throttle. | `preregistration.md`, `analysis.py` |
| **Output** | ASER level, misconception code, NCERT page, Hindi hint, C-R-A stage, bench assignment, parent page — all rendered on the device. | `app.py` dashboard |

### 4.2 Guardrails
> *"Describe how your solution deals with wrong or inappropriate AI outputs (e.g., verification, guardrails, human review)."*

1. **The model is never allowed to judge a child on unreliable audio.** Below 80% confidence the app returns `needs_tap` and refuses.
2. **A dropped vowel sign is treated as an error**, because in Devanagari it changes the word. A naive character distance would have scored `bili` vs `billi` at 83% and passed it. This is a real bug we found and fixed.
3. **The model cannot invent content.** It receives one NCERT page and is instructed to cite only that page; a tool schema forces the output shape.
4. **When the transcript is unverified, the system errs toward "cannot read."** Falsely telling a teacher a child cannot read is the more damaging error.
5. **The teacher is the final authority**, always, with one tap, and the override is logged as a fidelity datum rather than discarded.
6. **Offline, the model is not silently faked.** A documented rule path runs and `AI_AUDIT` records `fallback` for that decision. We report the real LLM-versus-fallback rate instead of assuming the model was always in the loop.

### 4.3 Ability to work in real scenarios
> *"State how the solution will work in low-connectivity, low-data environments and on low-cost devices. If parts require connectivity, tell us which, and what degrades gracefully offline."*

| Component | Offline behaviour | Cost on a ₹8k–₹12k phone |
|---|---|---|
| Item serving, ladder, screener, tap input, timer, bench grouping, bench map, parent page | **Fully functional.** Zero network calls. | Negligible |
| ASR | **Fully functional on device** (ONNX) | Only model on device; sized to fit 1–2 GB RAM |
| Scorer and Rasch | **Fully functional** — pure arithmetic | Negligible |
| Claude diagnosis | Degrades to a documented rule path; the product still returns a level, a misconception and a page | No local cost |
| Sync | Opt-in, cursor-based, batch 500, upload-only; can be disabled with zero feature loss | Negligible |

### 4.4 User inputs and testing (evidence of feedback collected and incorporated)
- **Teacher interviews:** 5 Grade 1–3 government teachers, **stopwatch-measured** paper-assessment baseline (not recall).
- **Error-mapping blind validation:** two experienced teachers blind-rate every error-to-NCERT mapping; **≥85% agreement** required before a mapping ships; corrections within 48 hours.
- **Fidelity log:** 5-item weekly log (assessed today? groups taught? activities completed? overrides? issues?) — logged, never recalled; the only source of the dashboard's fidelity numbers.
- **Classroom simulator:** 45-child classroom at 60 dB babble, battery throttle, interruptions, silence timeouts, forced kill and resume. Pass criterion: **≥90% of children reach a stable level in ≤5 minutes, zero crashes**.
- **Low-end device E2E:** Android 8 with 1–2 GB RAM, plus airplane-mode demo.
- **Attach:** `simulator.csv` + `fidelity.csv` (see `INTERVIEW_KIT.md` §7).

**Change-made = the proof.** Every finding in the evidence log must have a `change made` column. Those are the rows a judge reads to verify "refinement basis user input."

### 4.5 Future roadmap
| Pathway | Description |
|---|---|
| 1. Language packs | Telugu and Kannada — a data change against the same schema, not a rewrite |
| 2. State alignment | Kannada/Marathi SCERT FLN code mapping for the error taxonomy |
| 3. Teacher-to-teacher mode | Share a bench plan within a school; no child data leaves the campus |
| 4. System integration | Printable one-pager for the school's existing paper ASER cycle; SCERT-level dashboard that aggregates at school, never at child level |
| 5. Reduce the LLM to where it earns its place | Measure live-versus-fallback rate; keep the model only for genuine ambiguity |
| 6. Open-source the pack | Any state can fork it; +USD 250 in Claude credits for doing so |

---

## Final verification before uploading

```bash
# 1. Regenerate the Build stage proposal PDF
python -X utf8 build_proposal.py

# 2. Verify the PDF is valid and check page count
python -X utf8 -c "from pypdf import PdfReader; r=PdfReader('Samanantar_Build_Proposal.pdf'); print('Pages:', len(r.pages))"

# 3. AI layer self-test
python -X utf8 ai.py

# 4. Engine self-test
python -X utf8 engines.py

# 5. App compiles
python -X utf8 -c "import py_compile; py_compile.compile('app.py', doraise=True)"

# 6. Run engine + plan tests
npm test

# 7. Run the classroom simulator
npm run sim

# 8. Verify every content-pack item is cited
python -X utf8 -c "import json; p=json.load(open('content_pack.json',encoding='utf-8')); assert all(i.get('ncertRef') and i.get('cbseFln') for i in p['items']); print('Pack validated:', len(p['items']), 'items cited')"
```

---

## Compliance checklist

- [ ] Every member registered **individually**; 2–4 members; 18+; Indian citizens; not representing an organisation
- [ ] Team and challenge **unchanged** since the Ideate stage
- [ ] Demo link reachable **without** an account or an API key
- [ ] `python ai.py`, `python engines.py` and the CI all pass
- [ ] Video is public, ≤3:00, English audio or subtitles, and a 60-second fallback is recorded
- [ ] Deck covers AI layers, guardrails, real-world operation, user-input evidence, and roadmap
- [ ] All numbers quoted are **measured or pre-registered targets**. Placeholders are labelled as placeholders.
- [ ] De-identified data only: pseudonymous roll IDs, no child names, no photos
- [ ] Repository is public (we intend to open-source, which also carries the additional USD 250 in Claude credits)

---

## What the judges will check

| What they check | Where to look |
|---|---|
| "Show us how AI is used, in layers" | `ai.py`; the AI Lab tab in `app.py` |
| "Guardrails for wrong output" | `ai.py` (confidence gate + teacher override + fallback log) |
| "Low-connectivity, low-cost behaviour" | `ARCHITECTURE_OFFLINE.md` §5 (4-tier ladder) |
| "Proof of user input" | `INTERVIEW_KIT.md` §7 (evidence log with change-made column) |
| "Why is AI central, not a wrapper" | `ai.py` (`LlmDiagnostic._call_claude`); the AI Lab tab |
