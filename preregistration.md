# Pre-registration — Samanantar Cluster RCT (OSF)

**Version:** 1.0 — frozen before post-test (per plam.md §4)
**Pack:** content_pack.json v1.3.0 (hi,mr)

## Hypothesis
Samanantar reduces teacher minutes/child vs paper ASER with no loss of diagnostic fidelity (TOST), and app level agrees with blinded assessor (κ≥0.75). Learning gain reported as effect size (honest, not p breakthrough).

## Design
- Unit: classroom (cluster randomization, coin-flip by external). 4 classes (2T,2C), 2 schools, N≈90–120 G1-3
- Control: paper ASER only, no device in room, deviation log
- Washout: none. Pre 10 Oct → 3-week use → Post 1 Nov

## Endpoints
| Type | Metric | How |
|------|--------|-----|
| Primary | % ≥1 ASER level gain (pre→post) | ASER Pre-Letter→Story, same items pre/post |
| Co-primary | minutes/child | stopwatch, 10 kids/class sample |
| Secondary | teacher confidence 1–5 Likert pre/post, usage days/week, override %, completion % |
| Fidelity | TOST equivalence app vs paper ±0.2 SD |
| Agreement | quadratic-weighted κ app vs blinded re-test 20% |

## Power
ICC 0.15, 2 clusters/arm, ~25 kids/cluster → MDES≈0.40 SD. 20pp at this N not detectable — report d + 95% CI.

## Covariates
grade, gender, baseline level, teacher_id, school_id

## Analysis
Mixed-effects regression (children nested in classroom), baseline as covariate, Cohen's d + 95% CI. Script: `analysis.py` (versioned before post-test).

## Stop rule
Median time/child >6.0 min → pause, fix, don't burn pilot.

## Data
Pseudonymous IDs only, exports: `samanantar_assessments.csv`, `samanantar_events.json`, `fidelity.csv` — no PII, no photos.

## Ethics
Written consent hi+en on file, in teacher view never alone, SQLCipher at rest, opt-in sync, IRB waiver letter.
