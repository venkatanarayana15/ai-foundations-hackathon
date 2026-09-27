"""Detect real clipping / overlap on every page of the proposal.

Two failure modes reportlab can produce:
  1. Content drawn below the footer rule (bottom clipping)
  2. Two flowables drawn on top of each other (overlap)
"""
import pdfplumber

PDF = "A2Z_Samanantar_Ideate_Proposal.pdf"
FOOTER_TOP_MARGIN = 26   # pts below page bottom; footer band lives here

with pdfplumber.open(PDF) as pdf:
    print("=" * 66)
    print("CLIPPING / OVERLAP CHECK")
    print("=" * 66)
    issues = 0
    for i, page in enumerate(pdf.pages):
        h, w = page.height, page.width
        words = page.extract_words()

        # --- bottom clipping: anything below the footer text baseline ---
        # The footer is a fixed 16-token string; if the only words down there
        # are those tokens, nothing is clipped.
        FOOTER_TOKENS = {
            "A2Z", "·", "Samanantar", "Challenge", "02", "Learning-Level",
            "Visibility", "Ideate", "proposal,", "27", "Sept", "2026", "Page",
        }
        CLIP_Y = h - 18
        low = [x for x in words if x["bottom"] > CLIP_Y]
        body = [x for x in low
                if x["text"] not in FOOTER_TOKENS and not x["text"].isdigit()]
        # --- horizontal overflow past the right margin ---
        over = [x for x in words if x["x1"] > w - 20]

        # --- overlap: pairs of words whose boxes intersect significantly ---
        overlaps = 0
        boxes = [(x["x0"], x["top"], x["x1"], x["bottom"], x["text"]) for x in words]
        for a in range(len(boxes)):
            ax0, at, ax1, ab, _ = boxes[a]
            if (ab - at) > 18:      # skip tall blocks (table cells) - not a defect
                continue
            for b in range(a + 1, len(boxes)):
                bx0, bt, bx1, bb, _ = boxes[b]
                if bt > ab + 2:
                    break
                ix = min(ax1, bx1) - max(ax0, bx0)
                iy = min(ab, bb) - max(at, bt)
                if ix > 1.5 and iy > 2.0:
                    overlaps += 1

        bad = len(body) or len(over) or overlaps
        if bad:
            issues += 1
            print(f"  p{i+1}:  footer-intrusion={len(body)}  right-overflow={len(over)}  overlaps={overlaps}")
            for x in body[:4]:
                print(f"        below: {x['text']!r} @y={x['bottom']:.0f}")
        else:
            print(f"  p{i+1}:  clean")
    print("=" * 66)
    print("PAGES WITH DEFECTS:", issues)
