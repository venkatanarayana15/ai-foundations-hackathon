# Submission Checklist — Team A2Z

**Challenge 02 — Learning-Level Visibility** · *Samanantar* · Ideate deadline **27 Sept 2026, 23:59**

## Submit this file

`A2Z_Samanantar_Ideate_Proposal.pdf` — 11 pages = title/ToC + **9 content slides** + team page
(regenerate: `python build_ideate_proposal.py`)

## Ideate stage (27 Sept 2026) — REQUIRED

- [x] **Proposal: 7–10 slides as a PDF.** 9 content slides; Title, ToC and Team Profiles are excluded from the count, as §4 allows
- [x] **Problem Understanding (1 page)** — the specific aspect, who is affected, and how the harm happens
- [x] **Proposed Solution (2 pages)** — the five-minute loop, how it addresses the challenge, and why outcomes improve
- [x] **Users and Context (2 pages)** — three users, a five-point journey map, and seven constraints with what each cost us
- [x] **Innovation and creativity (2 pages)** — three novel capabilities, prior art credited, and a five-way comparison
- [x] **Technology and Data feasibility (2 pages)** — stack, resources, a **data-flow diagram**, feasibility, and AI's role at each stage
- [x] **Partial solution declared** — §3.6 permits it; the sub-part and the three named teacher needs are quoted on slide 1
- [x] **AI-centric** — Claude is the diagnostic reasoner; `ai.py` holds the tool schema, guardrails, matra-weighted scorer and Rasch model
- [x] **Team: 2 members** — Venkata Narayana G V, Mahesh Babu Ch (2–4 permitted by §3.1)
- [x] **Both members registered individually** — §2.4 forbids organisation registration
- [x] **Team and challenge frozen** — §3.5; no additions or changes after this submission

## Verify before you upload

```bash
python build_ideate_proposal.py     # regenerate the PDF
python audit_instructions.py        # must print 31/31
python audit_submission.py          # must print READY TO SUBMIT
python audit_ai_centrality.py       # must print 30/30
```

## Then, for the Build stage (10 Oct – 1 Nov)

- [ ] Push to a **public** GitHub repo — also earns the extra USD 250 in Claude credits
- [ ] `streamlit run app.py` — works offline, no API key required; the AI Lab tab shows the model registry and audit log
- [ ] 3-minute YouTube video + a 60-second fallback recording
- [ ] Short deck: AI in layers (input → processing → guardrails → evaluation → output), guardrails, offline behaviour, user-input evidence, roadmap
- [ ] Pilot: cluster-randomised, pre-registered on OSF, κ ≥ 0.75, TOST ±0.2 SD, stopwatch-measured minutes per child

See `STAGE2_BUILD_PACK.md` and `preregistration.md`.

## Judging weights we are optimising against (§6, Stage 1)

| Criterion | Weight | Where we invest |
|---|---|---|
| Efficacy + clarity of target user | **35%** | Slide 1 quantifies the problem and names the three needs; slide 4 gives the journey map; slide 5 answers "what did the constraints cost you" |
| Innovation and creativity | **30%** | Slide 6 separates genuine novelty from prior art and adds the "why now"; slide 7 is the head-to-head |
| AI centricity + technical feasibility | **25%** | Slide 3 is the AI layer end to end; slides 8–9 give the stack, data and the drawn flow diagram |
| Clarity of presentation | **10%** | One claim per slide, real tables instead of prose, consistent design |

## Known gaps, stated openly

| Gap | How we handle it |
|---|---|
| No learning-gain results yet | Slide 6 states the 0.40 SD minimum detectable effect and pre-commits to reporting effect sizes with intervals |
| ASR accuracy on six-year-olds at 60 dB is unmeasured | Named the biggest risk; the design already assumes failure via the confidence gate |
| Languages | Hindi and Marathi only for the pilot, stated plainly on slide 7 |
| Two people, one doing most of the work | Roles described accurately rather than claiming a two-expert split we do not have |
