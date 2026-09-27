# Teacher Interview Kit & User Journey Map

### Build-stage user evidence for Samanantar (Challenge 02: Learning-Level Visibility)

**Why this document exists.** The Build stage scores **"user-centricity" and "proof of testing and refinement basis user input" at 35%** — the single heaviest band. It asks for *"any data or evidence showing how user feedback or inputs have been collected and incorporated into the solution"* and *"intended user, user journey map and any inbuilt consideration of existing user constraints."*

This kit produces that evidence. Run it in **Build Week 1** (10–18 Oct). Everything you log here becomes citable in the Finale deck.

> ⚠️ **Integrity rule:** the Ideate deck contains **no** teacher quotes, because these interviews have not happened yet. Do not move any quote from this kit into a submission until it is a real, logged, verbatim quote with a date and a teacher ID. Guidelines §7 allows judges to ask you to explain your process live.

---

## 1. Objectives — what we must walk away knowing

| # | Question | Feeds |
|---|---|---|
| 1 | Where in the day does the multigrade teacher actually lose time? | User journey map (as-is) |
| 2 | How does she currently decide who can read / who can't? | Problem statement credibility |
| 3 | How does she plan for multiple grades today — or does she? | Solution framing, "planner not dashboard" |
| 4 | What is the realistic device, power and connectivity reality? | Offline architecture (`ARCHITECTURE_OFFLINE.md`) |
| 5 | Which of our assumptions are **wrong**? | Innovation slide, roadmap |
| 6 | Would she use a 40-minute AI-assembled block — and what would stop her? | Go / no-go on the core bet |

**Explicitly not** objectives: validating that we are clever; collecting quotes that flatter the pitch. Interview to find the places the product breaks.

---

## 2. Sample & recruitment

**5 teachers + 1 head teacher.** Deliberately not all the same profile:

| # | Profile | Why |
|---|---|---|
| T-01 | Govt primary, **Grades 1–3 multigrade**, small village school (<60 students) | The primary user |
| T-02 | Govt primary, multigrade, **larger class** (>40) | Stress case |
| T-03 | Govt primary, **single grade** (G1 only) | Tests whether the problem is genuinely multigrade-specific |
| T-04 | Govt primary, multigrade, **low literacy/low digital confidence** | The constraint that can kill adoption |
| T-05 | Govt primary, multigrade, **has used some EdTech** (DIKSHA/other) | Prior-tool rejection reasons |
| T-06 | **Head teacher / HM** of a small school | Deployment, scheduling, who approves |

Recruit through existing field contacts. If field access yields fewer than 5, **say so honestly** in the submission and report the actual N — a smaller honest sample beats an inflated one.

---

## 3. Ethics & consent

- **Teacher consent** (separate from the child consent in `consent_template.txt`): purpose, voluntary, can stop anytime, audio only with explicit permission, anonymous in all outputs.
- **Pseudonymous IDs only**: teachers become `T-01…T-06`. No names, no school names, no village names in any artifact.
- **No child data** is collected in these interviews. Do not photograph children. Do not ask teachers to share child names.
- **Recording:** audio only with written consent; otherwise notes only. Delete recordings after transcription and store the transcript pseudonymously.
- **Safeguarding:** interviews are with adults, in a professional setting, never alone with a child.

---

## 4. Logistics

- **Length:** 35–45 minutes. Do not run long; respect the school day.
- **Format:** in person, at the school, ideally **after** teaching hours or in a free period.
- **Bring:** this guide, printed consent form, notebook, stopwatch/phone timer, pen, and the prototype on a **low-end device** (show, don't tell).
- **Roles:** interviewer (asks and listens) + note-taker (captures verbatim, does not lead). If solo, record with consent.
- **Bring a small gift of respect** — tea, or a thank-you certificate for her time. Teachers give up break time for this.

---

## 5. Baseline measurements (do these first, with a stopwatch)

These give you the numbers that make the impact claim honest. **Time them, do not ask for estimates.**

| # | Measurement | How |
|---|---|---|
| M1 | **Minutes to assess one child's reading on paper** | Ask her to demonstrate with any child willing and present; time it. Repeat for 3 children, or ask her to recall the last time she did a full round. |
| M2 | **Minutes to assemble one multigrade lesson plan** | "Show me how you'd plan tomorrow's reading period." Time it. |
| M3 | **How groups are formed today** | Ask her to write the names of children who "can read well" and "cannot read". Time it. This reveals whether the map exists in her head and how coarse it is. |
| M4 | **Device reality** | Her own phone model, RAM, storage free, charging availability, daily data, how often she uses it for work. |
| M5 | **Class composition** | Number present today, by grade; how many are actually at each level *by her own judgement* — compare later with the app's map. |

> M5 is quietly the most powerful number: if she believes 20 of 34 can read and the assessment finds 9, that gap **is** the problem statement.

---

## 6. Semi-structured interview guide

**Rules:** open questions first, never lead, never offer the product as an answer. Ask "how do you do X today?" not "would you use X?". Stay silent for two seconds after she finishes — the next sentence is usually the real one.

### Section A — Context (5 min)
1. Walk me through your day from when you arrive to when you leave. *(map the real timetable)*
2. How many children are in your room, and which grades sit together?
3. How many teachers does this school have? Does that change during the year?
4. Who decides what you teach each day — a timetable, the state, the textbook?

### Section B — The multigrade reality (10 min)
5. When you teach reading, how do you handle the different grades in the room?
6. Tell me about the last time a lesson worked well in this room. What made it work?
7. Tell me about the last time it didn't. What happened? *(listen for: time, one group idling, syllabus pressure)*
8. What do the children actually do while you are working with another grade? *(probe: worksheets? copying? nothing?)*
9. How much of the period do you spend on teaching versus organising? *(this is the core pain — let her quantify)*

### Section C — Knowing the level (10 min)
10. How do you know which children can read and which can't? Show me how you'd check. *(do M3 here)*
11. When did you last do a full check of every child's reading? How long did it take?
12. Does anything record this — a register, a note, a test paper? What happens to it?
13. What do you do when you find out a child in Grade 3 can't read letters? *("What do you actually do tomorrow morning?")*

### Section D — Planning (5 min)
14. Show me how you plan for tomorrow. What do you start from? *(do M2 here)*
15. Where does the NIPUN Bharat / FLN material fit in? Do you get TLM? Do you use it?
16. How long does planning one day take you at home?

### Section E — Devices & constraints (5 min)
17. What phone do you use? Is it yours? *(do M4)*
18. What's the network and power like on a normal day?
19. Have you used any teaching app? What happened — why did you stop? *(critical for T-05; listen for: too long to learn, needed internet, English, one-device-per-child)*
20. If an app was in the way of your teaching, how long before you'd abandon it? *(elicit a tolerance threshold)*

### Section F — Constraint test (5 min) *— do this last*
21. In one sentence: what is the hardest part of teaching three grades at once?
22. If you could have one thing done for you every morning, what would it be? *(let her describe the product's job in her own words — this becomes your headline quote)*
23. If it existed, when would you want it delivered — night before, or morning of?
24. Is there anything important about your classroom I didn't ask about?
25. May we come back and show you something we're building?

---

## 7. Evidence log *(the artifact the Build stage asks for)*

One row per finding. This is what you attach to the submission.

| ID | Date | Teacher | Context | Verbatim (original language + English) | Implication | Product change made | Status |
|---|---|---|---|---|---|---|---|
| E-01 | | T-01 | | | | | open |
| E-02 | | T-01 | | | | | open |
| E-03 | | T-04 | | | | | open |
| … | | | | | | | |

**Rules for the log**
- Verbatim means verbatim — keep the original Hindi/regional wording and translate.
- Every row must have an **implication** and, once acted on, a **change made**. The change column is the literal proof of "refinement basis user input."
- Log **negative** findings too. "Three teachers said they would not use a phone while teaching" is more valuable in the deck than a compliment, and judges trust it.

---

## 8. Rapid analysis (same day, 60 minutes)

1. **Affinity map:** write every finding on a sticky (physical or Miro). Cluster silently — no discussing until clusters form.
2. **Severity × frequency table:** which pains are both common and severe? Those define the product; the rare ones go to the roadmap.
3. **Assumption audit:** list the assumptions in `IDEATE_DECK.md` (hybrid voice+tap, 40-min block, one shared device, plan-before-class). Mark each **confirmed / contradicted / untested**. Contradicted assumptions are the most publishable finding you have.
4. **Top 10 quotes:** the ten that best represent the clusters, with IDs.
5. **Journey map validation:** move any stage of the map that the data disagrees with. Record what moved.

---

## 9. Prototype usability test (Build Week 2–3, 3 teachers)

Different instrument: this is *testing the build*, not the problem.

**Session (30 min):** 5 minutes context → 20 minutes tasks (observe, do not help) → 5 minutes debrief.

**Five tasks, on a low-end device, in airplane mode first:**
1. "Show me where a child is in this app." → *finds level-map in <60 s?*
2. "Set up tomorrow's reading period." → *arrives at a plan, correctly, unaided*
3. "One child in this group can actually read better than the app says. Fix it." → *finds the override*
4. "The internet is off. Does it still work?" → *observes the degradation*
5. "Class is over. Tell the app what happened." → *finds the log*

**Metrics per task:** success (unaided / prompted / failed) · time to complete · number of mis-taps or requests for help · verbatim reaction.

**Debrief questions:** What would you change? What would you remove? Would you use this tomorrow? What would make you stop using it?

**Success bar (set it before you test, and report the truth):** ≥4 of 5 tasks completed unaided by ≥2 of 3 teachers within the target times.

---

## 10. User Journey Map (as-is — validate and correct it with the interviews)

**Persona:** the multigrade primary teacher. **Unit:** one teaching day. **Emotion:** 1 (worst) – 5 (best).

| Time | Stage | Doing | Thinking | Feeling | Pain point | Opportunity | Product touchpoint |
|---|---|---|---|---|---|---|---|
| 7:45 | Arrive & set up | Sweeps, arranges room, writes on board | "Which grade do I start with today?" | 3 | No plan yet for three grades | Pre-built block waiting | Open app → today's plan card |
| 8:00 | Whole-class start | Teaches to the middle | "Some are lost, some are bored" | 2 | One lesson must serve three grades | A shared 5-min opener everyone can do | Warm-up activity (whole class) |
| 8:15 | **Differentiated work** | Hands out one worksheet, moves between groups | "Who do I help first?" | **1** | **Doesn't know who can do what; worksheet fits nobody** | A pre-sequenced 3-band rotation | The 40-min block + station cards |
| 8:35 | The gap | Bright children finish; strugglers copy or sit idle | "I'm managing, not teaching" | 2 | Attention spent on order, not learning | Point her to the 2–3 children who need her most | "Help first" chip |
| 9:00 | Numeracy | Repeats the whole struggle for maths | "Same problem again" | 2 | Duplicated effort | Same loop, numeracy pack | Numeracy block |
| 10:30 | Break | Tea, paperwork, attendance | "No idea if this is working" | 3 | Learning invisible | A weekly picture of movement | Weekly regroup + progress view |
| 13:00 | After school | Goes home; planning begins at night | "I'll plan tonight" | 2 | Planning eats personal time | Plan assembled during the day | Auto-logged plan → tomorrow |
| 21:00 | Home | Plans tomorrow from the textbook | "Where do I even start for three groups?" | 2 | Hours of unpaid planning | 10-second plan generation | Generate block for tomorrow |

**The dip is 8:15–8:35.** That is the product's entire reason to exist. Our success criterion is deliberately narrow and honest: **lift that one point of the curve.**

### To-be map (target)

| Time | Stage | With Samanantar | Target feeling |
|---|---|---|---|
| 7:45 | Arrive | Plan already generated (night before or 8:00) | 4 — prepared |
| 8:00 | Whole-class start | 5-min shared opener from the plan | 4 |
| 8:15 | Differentiated work | 3 bands, 2 stations, talk-line in hand | **4 — capable** |
| 8:35 | The gap | "Help first" sends her to the right 3 children | 4 |
| 9:00 | Numeracy | Same loop, numeracy pack | 4 |
| 13:00 | After school | One tap: what happened today | 4 — informed |

---

## 11. What this buys you at each stage

| Stage | How this kit is used |
|---|---|
| **Ideate (27 Sep)** | Nothing from here is claimed yet — the deck labels every user statement a hypothesis. The *plan* is disclosed on slide 5. |
| **Build (1 Nov)** | The 35% user band: evidence log with dated quotes, baseline stopwatch numbers (M1/M2), assumption audit with contradicted assumptions, usability metrics, and the **change log** showing what we altered. |
| **Finale (18 Nov)** | Top-10 quotes, the validated journey map, the honest "what we could not measure" slide, and the roadmap shaped by real constraints. |

**The single most valuable output of this kit is a contradiction.** If teachers reject the 40-minute block, or the morning check, or voice-first — you must know it in Week 1, not in the Finale.
