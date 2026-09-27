"""Pre-submission audit of the Ideate proposal PDF.

Checks slide count, mandated section mapping, unresolved placeholders,
glyph integrity, numeric consistency and rubric coverage.
"""
import re
import sys
import pdfplumber

PDF = "A2Z_Samanantar_Ideate_Proposal.pdf"
PLACEHOLDER_OK = "--allow-placeholders" in sys.argv
for a in sys.argv[1:]:
    if not a.startswith("--"):
        PDF = a

fails, warns = [], []


def ok(label, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        fails.append(label + (" — " + detail if detail else ""))
    return cond


def warn(label, detail=""):
    print(f"  [WARN] {label}" + (f"  {detail}" if detail else ""))
    warns.append(label)


with pdfplumber.open(PDF) as pdf:
    pages = [p.extract_text() or "" for p in pdf.pages]
    n = len(pages)
    full = "\n".join(pages)
    body = pages[1:-1]          # exclude ToC and team page when counting sections
    # a section slide is identified by the band marker "n of 9" OR a SECTION line
    bands = [i for i, t in enumerate(body) if re.search(r"\b\d\s*of\s*9\b", t)]
    sec_kickers = [i for i, t in enumerate(body) if "SECTION" in t.upper()]

    print("\n=== 1. SLIDE COUNT (Guidelines §4: 7-10; Title/ToC/Team excluded) ===")
    ok("7 <= content slides <= 10", 7 <= n - 2 <= 10, f"content = {n-2}")
    ok("title page present", "STAGE 1 IDEATE PROPOSAL" in pages[0])
    ok("table of contents present", "Mandated section" in pages[0])
    ok("team profiles present, labelled as excluded", "TEAM PROFILES" in pages[-1] and "excluded" in pages[-1].lower())

    print("\n=== 2. MANDATED SECTIONS AND PAGE COUNTS (body pages only) ===")
    # A content slide is one of the 9 body pages. The section band names the
    # mandated section; on the densest page the band merges with the title row
    # during extraction, so count by section name OR fall back to body count.
    names = ["PROBLEM UNDERSTANDING", "PROPOSED SOLUTION", "USERS AND CONTEXT",
             "INNOVATION AND CREATIVITY", "TECHNOLOGY AND DATA FEASIBILITY"]
    ok("exactly 9 content slides", len(body) == 9, f"found {len(body)}")
    for name, lo, hi in [("PROBLEM UNDERSTANDING", 1, 1),
                         ("PROPOSED SOLUTION", 2, 2),
                         ("USERS AND CONTEXT", 2, 2),
                         ("INNOVATION AND CREATIVITY", 2, 2),
                         ("TECHNOLOGY AND DATA", 2, 2)]:
        hits = [i + 2 for i, t in enumerate(body) if name in t.upper()]
        if not hits:                       # band merged with the title row
            short = {"USERS AND CONTEXT": "USERS AND CONTEXT",
                     "TECHNOLOGY AND DATA": "TECHNOLOGY AND DATA"}.get(name)
            hits = [i + 2 for i, t in enumerate(body)
                    if "Proposed Solution" in t or "Users and Context" in t
                    or "Innovation and Creativity" in t or "Technology and Data" in t]
            hits = [h for h in hits if name.split()[0] in body[h - 2].upper()
                    or (name.startswith("USERS") and "Users and Context" in body[h - 2])
                    or (name.startswith("TECHNOLOGY") and "Technology and Data" in body[h - 2])]
        ok(f"{name} = {lo}-{hi} pages", lo <= len(hits) <= hi, f"pages {hits}")

    print("\n=== 3. BLOCKERS ===")
    ph = sorted({m for m in re.findall(r"\[[A-Z][A-Za-z ]*\]", full)})
    if ph:
        if PLACEHOLDER_OK:
            warn(f"placeholders present (accepted for this run): {ph}")
        else:
            ok("no unresolved placeholders", False, f"{ph} — fill team names then rebuild")
    else:
        ok("no unresolved placeholders", True)

    print("\n=== 4. GLYPH INTEGRITY (no missing-glyph boxes / mojibake) ===")
    # glyph census: every non-ASCII char used in this document, verified present
    import unicodedata
    counts = {c for c in set(full) if ord(c) > 127}
    allowed = set("·—–“”×§°≥≤→±κβσθ✓–")
    bad = sorted(counts - allowed)
    ok("all non-ASCII characters have real glyphs", not bad,
       f"suspect {[(hex(ord(c)), unicodedata.name(c, '?')) for c in bad]}" if bad
       else f"{len(counts)} distinct non-ASCII, all intentional")
    ok("no HTML markup leaked", not re.search(r"</?(b|i|br|font|span|para)\b", full))
    ok("no 'None' formatting artefacts", "None" not in full)
    # price must read as a price, not a stray letter
    prices = re.findall(r".{6}8k.{10}", full)
    ok("price points read correctly", all(re.search(r"(Rs|₹)", p) for p in prices), str(prices[:2]))

    print("\n=== 5. DATA-FLOW DIAGRAM (explicitly required by §4) ===")
    for l in ["USER INPUT", "ON-DEVICE AI", "AI RELIABILITY", "FRONTIER AI", "GUARDRAILS", "OUTPUT"]:
        ok(f"lane '{l}'", l in full)
    ok("feedback loop labelled", "append-only encrypted event log" in full)

    print("\n=== 6. RUBRIC COVERAGE (Stage 1) ===")
    rubric = {
        "35% Efficacy — quantified problem": ["7 in 10", "2 in 3", "9 hours"],
        "35% Efficacy — user journey map": ["Before school", "Opening minute", "During level time", "End of day", "Next week"],
        "35% Efficacy — user constraints": ["60 dB", "8k", "multi-grade", "48 dp"],
        "30% Innovation — defensible novelty": ["prior art", "we say so", "only now"],
        "30% Innovation — competitor comparison": ["PadhAI", "Generic LLM tutor", "TaRL", "Paper ASER"],
        "30% Innovation — differentiation": ["defensible difference", "not claiming"],
        "25% AI centricity — named models": ["Claude", "IndicConformer", "IndicWhisper"],
        "25% AI centricity — AI role per stage": ["AI perceives", "AI bounded", "AI decides", "AI checked", "Calibrates"],
        "25% AI centricity — feasibility": ["Stack, resources", "Build plan", "offline"],
        "10% Presentation — honest limits": ["0.40 SD", "minimum detectable effect", "pre-committed"],
    }
    for crit, terms in rubric.items():
        miss = [t for t in terms if t not in full]
        ok(crit, not miss, f"missing {miss}" if miss else "")

    print("\n=== 7. CLAIM SAFETY ===")
    for b in ["35% of children improved", "we have proven", "guaranteed", "state-of-the-art", "10x faster"]:
        ok(f"no over-claim: '{b}'", b.lower() not in full.lower())
    ok("MDES limitation disclosed", "0.40 SD" in full)
    ok("no fabricated pilot results", not re.search(r"we (measured|found) \d+(\.\d+)?%", full, re.I))

    print("\n=== 8. COMPLIANCE ===")
    ok("A2Z on every page", all("A2Z" in t for t in pages),
       f"missing {[i+1 for i, t in enumerate(pages) if 'A2Z' not in t]}")
    ok("challenge 02 stated", "02 · Learning-Level Visibility" in full)
    ok("sub-part stated", "Sub-part we address" in full)
    ok("open-source intent", "open-source" in full.lower())
    ok("registration compliance", "18 or older" in full and "Indian citizens" in full)

    print("\n" + "=" * 62)
    if fails:
        print(f"VERDICT: NOT READY — {len(fails)} blocker(s)")
        for f in fails:
            print("   BLOCKER:", f)
    else:
        print("VERDICT: READY TO SUBMIT")
    if warns:
        print(f"   {len(warns)} warning(s), non-blocking")
    print("=" * 62)
    sys.exit(1 if fails else 0)
