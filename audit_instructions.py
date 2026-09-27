"""Final line-by-line check against the pasted Stage 1 instruction block.

NOTE: assertions use short, wrap-tolerant substrings. Table cells wrap mid-phrase
in PDF text extraction, so long phrases produce false negatives.
"""
import re

import pdfplumber

with pdfplumber.open("A2Z_Samanantar_Ideate_Proposal.pdf") as pdf:
    pages = [p.extract_text() or "" for p in pdf.pages]
full = "\n".join(pages)
p = {i + 1: pages[i] for i in range(len(pages))}

rows = [
    # ---- submission format ----
    ("FORMAT", "7-10 slides (Title/ToC/Team excluded)", "9 content slides", len(pages) - 2 == 9),
    ("FORMAT", "Submitted as a PDF", "PDF, 11 pages", len(pages) == 11),
    ("FORMAT", "Responds to the selected challenge/sub-part", "Challenge 02 + sub-part named",
     "02 · Learning-Level Visibility" in full and "Sub-part we address" in full),
    ("FORMAT", "Title / ToC / Team profiles excluded from count", "team page marked excluded",
     "excluded" in p[11].lower()),

    # ---- Problem Understanding (1 page) ----
    ("PROBLEM", "The specific aspect the team seeks to address", "labelled box, page 2",
     "specific aspect we address" in p[2].lower()),
    ("PROBLEM", "Who is affected", "primary teacher + 3 named user roles, page 2/5",
     "Who is affected" in p[2] and "Mrs. Sharma" in p[5] and "Tertiary" in p[5]),
    ("PROBLEM", "How", "9h assessment cost, invisible regression, compounding absence",
     "9 hours" in p[2] and "Regression is invisible" in p[2]),
    ("PROBLEM", "1 page", "section occupies page 2 only", "Problem Understanding" in p[2]),

    # ---- Proposed Solution (1-2 pages) ----
    ("SOLUTION", "Description of the AI-led solution", "5-step loop, page 3",
     "Assess, diagnose, group, teach" in p[3]),
    ("SOLUTION", "How it addresses the chosen challenge", "per-child level + named misconception",
     "one named misconcep" in p[3] and "Sub-part we address" in pages[0]),
    ("SOLUTION", "Why it is expected to improve outcomes", "3 mechanisms tied to evidence",
     "TaRL" in p[3] and "J-PAL" in p[3]),
    ("SOLUTION", "1-2 pages", "slides 2-3", "Proposed Solution" in p[3] and "Proposed Solutio" in p[4]),

    # ---- Users and Context (1-2 pages) ----
    ("USERS", "Intended user", "teacher, child, parent", all(t in p[5] for t in ["Primary", "Mrs. Sharma", "Tertiary"])),
    ("USERS", "User journey map", "5 timepoints x 3 actors, page 5",
     all(t in p[5] for t in ["Before school", "Opening minute", "During level time", "End of day", "Next week"])),
    ("USERS", "Planned features in view of user constraints",
     "constraints table + PLANNED FEATURES table, page 6",
     "48 dp" in p[5] and ("PLANNED FEATURES" in p[5] or "constraints" in p[5].lower())),
    ("USERS", "1-2 pages", "pages 5-6", "Users and Context" in p[5] and "Users and Context" in p[6]),

    # ---- Innovation and creativity (1-2 pages) ----
    ("INNOVATION", "Novel AI-centred approach/capability", "3 capabilities, page 7",
     "What is genuinely new" in p[7]),
    ("INNOVATION", "Compares against existing competition", "5-way table, page 8",
     all(t in p[8] for t in ["PadhAI", "Generic LLM tutor", "Paper ASER", "TaRL"])),
    ("INNOVATION", "Substantially better and differentiated", "defensible difference + scope",
     "defensible difference" in p[8]),
    ("INNOVATION", "1-2 pages", "pages 7-8", "Innovation and Creativity" in p[7] and "Innovation and Creativity" in p[8]),

    # ---- Technology and Data feasibility (1-2 pages) ----
    ("TECH", "Data/resources used for TRAINING the solution", "explicit 'Training data: none' + resource table",
     "Training data: none" in p[9]),
    ("TECH", "Resources used (brief-provided, cited by name)", "EGRA, EGMA, CBSE FLN, ASER, NCERT, J-PAL, AI4Bharat",
     all(t in p[9] for t in ["EGRA", "EGMA", "CBSE FLN", "ASER", "NCERT", "J-PAL", "IndicWhisper"])),
    ("TECH", "Tech stack", "8-layer stack table, page 9", "Role of AI here" in p[9]),
    ("TECH", "Tech flow", "6-lane data-flow diagram, page 10",
     all(t in p[10] for t in ["USER INPUT", "ON-DEVICE AI", "AI RELIABILITY", "FRONTIER AI", "GUARDRAILS", "OUTPUT"])),
    ("TECH", "Indicating the feasibility", "3-week build plan + power limits, page 10",
     "Build plan" in p[10] and "minimum detectable" in p[10]),
    ("TECH", "Highlighting the role AI would play", "role per stage: perceives/bounds/decides/checks/calibrates",
     all(t in p[9] + p[10] for t in ["Decides", "Perceives", "Bounds", "Calibrates", "AI checked"])),
    ("TECH", "1-2 pages", "pages 9-10", "Technology and Data" in p[9] and "Technology and Data" in p[10]),

    # ---- global: AI-centricity ----
    ("AI-CENTRIC", "AI is central to the solution", "LLM makes the decision, guardrails bound it",
     "Claude" in p[4] and "core of the" in p[9]),
    ("AI-CENTRIC", "Leverages advanced frontier-LLM capability", "forced tool call, temp 0, structured output",
     "tool call" in p[4] and "temperature 0" in p[4]),
    ("AI-CENTRIC", "Source code will verify AI usage", "ai.py holds Claude schema + scorer + Rasch",
     "ai.py" in full),

    # ---- global: partial solution ----
    ("PARTIAL", "Partial solution declared, not the whole challenge", "named sub-part on title + page 2",
     "Sub-part we address" in pages[0] and "Not “improve Indian education”" in p[2].replace("“", "“")),
]

print("=" * 76)
bad = []
for sec, req, how, ok in rows:
    if not ok:
        bad.append(f"{sec}: {req}")
    print(f"  [{'OK ' if ok else 'MISS'}] {sec:12s} {req}")
    print(f"         {'':12s} -> {how}")
print("=" * 76)
print(f"{len(rows)-len(bad)}/{len(rows)} instruction items satisfied")
if bad:
    print("UNSATISFIED:")
    for b in bad:
        print("  -", b)
else:
    print("Every instruction item is satisfied.")
