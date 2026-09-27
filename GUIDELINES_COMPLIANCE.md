# Ideate Submission — Team A2Z
Product: **Samanantar** · Team: **A2Z** · Source: `AI for Foundational Learning Hackathon — Guidelines.docx` (11 pages) + the event page.
Extract: `guidelines_text.md`.

## Submission requirement → where we satisfy it

| Guideline § | Requirement | Our answer | Where |
|---|---|---|---|
| §3.1 | Teams of 2–4 | 2–4, multidisciplinary, education + AI/ML expert recommended | Proposal p.11 (Team Profiles) |
| §3.2 | One team per participant | Single team | Team Profiles |
| §3.4 | Multiple submissions permitted if unique and substantially different | We make **one** submission, on Challenge 02, so this does not apply. The team continues with it if it advances | Title page, team page |
| §3.5 | **No team or challenge changes after Ideate** | Frozen | Team Profiles |
| §3.6 | Partial solutions allowed | We explicitly scope to one sub-part: child-level diagnostic visibility | Proposal p.2 |
| §3.7 | **AI must be central; source code will be verified** | `ai.py` is the AI layer; the app opens an **AI Lab** tab showing the model registry, live diagnosis, Rasch estimates and the AI audit log | `ai.py`, AI Lab in `app.py` |
| §4 Stage 1 | **7–10 slide PDF**; jury will not read past 10 | **9 content slides** + title/ToC page + team page (all three exclusions explicitly permitted) | `A2Z_Samanantar_Ideate_Proposal.pdf` |
| §4 Stage 1 | Problem Understanding (1 page) | Slide 1 | p.2 |
| §4 Stage 1 | Proposed Solution (1–2 pages) | Slides 2–3 | p.3–4 |
| §4 Stage 1 | Users and Context (1–2 pages), incl. **user journey map** | Slides 4–5, journey map on p.5 | p.5–6 |
| §4 Stage 1 | Innovation and creativity (1–2 pages), incl. **comparison to existing solutions** | Slides 6–7, head-to-head table on p.8 | p.7–8 |
| §4 Stage 1 | Technology and Data feasibility (1–2 pages), incl. **a simple data-flow diagram** | Slides 8–9, **drawn flow diagram** on p.10 | p.9–10 |
| §4 Stage 1 | **PDF** via the Hack2Skill platform | One deck, shipped as PDF; regenerate with `python build_ideate_proposal.py` | — |
| §5.2 | **Must use the Claude credits** for at least one part | Claude is the diagnostic reasoner — the core value step | `ai.py` |
| §7 | Original work built in the window; open-source libraries and AI assistants encouraged | Own idea and implementation; libraries and assistants credited | Team Profiles |
| §8 | Open-sourcing earns an **extra USD 250** in Claude credits | We will open-source under MIT | Team Profiles |

## Judging weights we are optimising against (§6, Stage 1)

| Criterion | Weight | Where we deliberately invest |
|---|---|---|
| **Efficacy + clarity of target user** | **35%** | Slide 1 quantifies the problem and names who is affected; slide 4 gives three concrete users with their real constraints; slide 4 carries the **journey map**; slide 5 answers "what did the constraints cost you", which is the honest version of user-centricity |
| **Innovation + creativity** | **30%** | Slide 6 states three capabilities that are not incremental (misconception-level diagnosis, knowing when *not* to trust ASR, a self-calibrating instrument); slide 7 is a head-to-head table against paper ASER, PadhAI, generic LLM tutors and classic TaRL |
| **AI centricity + technical feasibility** | **25%** | Slide 3 is entirely the AI layer, component by component, including *why a frontier model is needed*; slides 8–9 give the stack, the data, and a drawn data-flow diagram with the AI stages marked |
| **Clarity of presentation** | **10%** | One claim per slide, real tables instead of prose, consistent design system |

### Where the 35% criterion is won or lost
The single highest-leverage slide is **5 (Constraints)**. Judges scoring "clarity of target user" are really asking: *do these people understand the problem, and did the solution come out of contact with them?* We answer with observable facts — 45 children across three grades, 15–20 minutes of level time, a ₹8k phone, 50–60 dB, a teacher trained in pedagogy and not in software, who will not read a manual — and then show what each one forced in the design, including what it cost us. Specificity, not empathy, is what reads as understanding.

## Known gaps and how we handle them

| Gap | Handling |
|---|---|
| We cannot report learning-gain results yet | Slide 6 states the power limitation openly and pre-commits to effect sizes with intervals. Claiming a 20 pp gain at this sample size would be fabrication. |
| ASR accuracy on six-year-olds at 60 dB is unmeasured | Slide 5 names it the biggest risk; slide 3 explains the design already assumes failure via the confidence gate. |
| Languages | Hindi and Marathi only for the pilot, stated plainly on slide 7. A pack version bump adds Telugu; claiming eight languages we cannot demo would be disqualifying. |
| Team names | Placeholders `[Name]` on the team page — **must be filled before upload.** |
| A 7–10 slide cap is a hard limit | We are at 9 content slides with margin for one more if a judge-mandated section needs expanding. |

## Final pre-upload verification

```bash
python -X utf8 build_proposal.py      # regenerates the PDF
python -X utf8 -c "import pdfplumber;print(len(pdfplumber.open('Samanantar_Proposal.pdf').pages))"
python -X utf8 ai.py                  # AI layer self-test
python -X utf8 engines.py             # engine self-test
python -c "import py_compile; py_compile.compile('app.py', doraise=True)"
```

Expected: **11 PDF pages** (1 title/ToC + 9 content + 1 team) for `A2Z_Samanantar_Ideate_Proposal.pdf`; `ai.py` and `engines.py` self-tests pass; `app.py` compiles.
