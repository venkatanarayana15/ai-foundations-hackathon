"""
build_ideate_proposal.py — generates A2Z_Samanantar_Ideate_Proposal.pdf

Stage 1 (Ideate) spec, per the official Guidelines §4:
  "A proposal of 7-10 powerpoint slides responding to the selected
   Foundational Learning challenge/sub-part of the challenge."
  - Problem Understanding .............. 1 page
  - Proposed Solution ................. 1-2 pages
  - Users and Context ................. 1-2 pages
  - Innovation and creativity of idea . 1-2 pages
  - Technology and Data feasibility ... 1-2 pages
  Format: PDF, submitted through Hack2Skill. Deadline 27 Sept 2026, 23:59.
  Title page, table of contents and team profiles are excluded from the count.

Optimised against the Stage-1 rubric (Guidelines §6):
  Efficacy + clarity of target user .... 35%
  Innovation and creativity ........... 30%
  AI centricity + technical feasibility  25%
  Clarity of presentation .............. 10%

Usage:  python build_ideate_proposal.py
"""
from __future__ import annotations

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Unicode safety: base-14 Helvetica has no rupee (U+20B9) or several
# punctuation glyphs, which silently render as "n" or a blank box. Register a
# TTF that covers them and use it for the whole document. ──
_UNICODE_FONTS = [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf",
                  r"C:\Windows\Fonts\calibri.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
for _f in _UNICODE_FONTS:
    if os.path.exists(_f):
        try:
            pdfmetrics.registerFont(TTFont("Uni", _f))
            pdfmetrics.registerFont(TTFont("Uni-Bold", _f))
            _FONT, _FONT_B = "Uni", "Uni-Bold"
            break
        except Exception:
            continue
else:
    _FONT, _FONT_B = "Helvetica", "Helvetica-Bold"

# ── design tokens: Desi Notebook, matching the app ──
INK = colors.HexColor("#134E4A")
TEAL = colors.HexColor("#0D9488")
AMBER = colors.HexColor("#D97706")
PAPER = colors.HexColor("#FDFBF7")
MUTED = colors.HexColor("#475569")
RULE = colors.HexColor("#D6D3D1")
BAND = colors.HexColor("#F0FDFA")

PAGE = landscape(A4)
W, H = PAGE
M = 11 * mm

ss = getSampleStyleSheet()

# ─────────────────────────────────────────────────────────────────
# TEAM ROSTER — EDIT THIS, THEN RE-RUN. Guidelines §3.5 freezes team
# composition at the Ideate stage, so get this right before submitting.
# Remove any member dict you do not need (minimum 2, maximum 4).
# ─────────────────────────────────────────────────────────────────
TEAM = [
    {"name": "Venkata Narayana G V", "role": "Founder & lead", "domain": "Product, pedagogy & engineering",
     "owns": "Built the solution end to end: the pedagogy (error taxonomy, C-R-A progression, TaRL grouping "
             "rule, NCERT/CBSE and EGRA/EGMA mapping), the engineering (Claude diagnosis layer with its "
             "tool schema and guardrails, the matra-weighted ASR scorer, the Rasch difficulty model), the "
             "offline event store, the app, and the pilot design with its pre-registration.",
     "why": "A two-person team needs one person to hold the whole thread. This is that person: pedagogy and "
            "engineering in the same head, so the mapping from a decoding error to a textbook page is made by "
            "the same person who has to make the model return it correctly."},
    {"name": "Mahesh Babu Ch", "role": "Collaborator", "domain": "Review & domain input",
     "owns": "Reviews the assessment flow and the remediation mappings for classroom practicality, and "
             "contributes to research and field inputs.",
     "why": "Every mapping an AI makes has to survive contact with a real teacher. A second set of eyes on "
            "whether the diagnostic is usable in a real room is worth more here than another engineer."},
]

# ─────────────────────────────────────────────────────────────────
# The official Challenge 02 statement names three specific teacher needs.
# We mirror its own language back, and map each need to what we return.
# Source: hack2skill challenge card, Challenge 02 — Learning-Level Visibility.
# ─────────────────────────────────────────────────────────────────
CHALLENGE_02 = ("A teacher often teaches a class without a clear understanding of each child's actual "
                "learning level, and therefore lacks actionable insights on where a lesson should begin, "
                "which misconceptions need to be solved, or which form of remediation support is required "
                "by the children")

NEED_TO_OUTPUT = [
    ("1", "Where a lesson should begin",
     "A per-child ASER/EGRA level — Pre-Letter, Letter, Word, Paragraph, Story — in 3–5 minutes, so the "
     "teacher starts at the child's level instead of the grade's."),
    ("2", "Which misconceptions need to be solved",
     "One named, coded misconception — not a score. “Drops the long-i matra, so she is decoding, not "
     "reading.” Diagnosis is a frontier model reasoning over the transcript, confidence and noise."),
    ("3", "Which form of remediation support is required",
     "A Concrete→Representational→Abstract activity for that specific gap, on a named NCERT page, grouped "
     "into benches of eight. C-R-A is the form; the textbook page is the medium."),
]
S_TITLE = ParagraphStyle("t", parent=ss["Title"], fontName=_FONT_B,
                         fontSize=27, leading=30, textColor=INK, alignment=TA_LEFT, spaceAfter=2)
S_SUB = ParagraphStyle("s", parent=ss["Normal"], fontName=_FONT, fontSize=11.2,
                       leading=14.4, textColor=MUTED, alignment=TA_LEFT)
S_H = ParagraphStyle("h", parent=ss["Heading1"], fontName=_FONT_B, fontSize=16,
                     leading=19.5, textColor=INK, spaceBefore=0, spaceAfter=5)
S_KICKER = ParagraphStyle("k", parent=ss["Normal"], fontName=_FONT_B, fontSize=7.2,
                          leading=8.6, textColor=AMBER, spaceAfter=2)
S_BODY = ParagraphStyle("b", parent=ss["Normal"], fontName=_FONT, fontSize=8.8,
                        leading=11.2, textColor=INK, spaceAfter=4)
S_CELL = ParagraphStyle("c", parent=ss["Normal"], fontName=_FONT, fontSize=7.7,
                        leading=9.6, textColor=INK)
S_CELLB = ParagraphStyle("cb", parent=S_CELL, fontName=_FONT_B)
S_CODE = ParagraphStyle("code", parent=ss["Normal"], fontName="Courier",
                        fontSize=7.6, leading=9.8, textColor=INK)
S_STATNUM = ParagraphStyle("stat", parent=ss["Normal"], fontName=_FONT_B,
                           fontSize=12, leading=13.6, textColor=TEAL)
S_CELLR = ParagraphStyle("cr", parent=S_CELL, fontName=_FONT, alignment=2)
S_CELLRR = ParagraphStyle("crr", parent=S_CELL, fontName=_FONT_B, alignment=2,
                          textColor=colors.white)
S_BANDH = ParagraphStyle("bh", parent=ss["Heading1"], fontName=_FONT_B,
                         fontSize=14, leading=17, textColor=colors.white,
                         spaceBefore=0, spaceAfter=0)
S_KICKERW = ParagraphStyle("kw", parent=S_KICKER, textColor=colors.HexColor("#FDE68A"))
S_GHOST = ParagraphStyle("ghost", parent=S_KICKER, spaceAfter=2)
S_DENSE = ParagraphStyle("d", parent=ss["Normal"], fontName=_FONT,
                         fontSize=7.0, leading=8.7, textColor=INK)
S_DENSEB = ParagraphStyle("db", parent=S_DENSE, fontName=_FONT_B)
S_TH = ParagraphStyle("th", parent=S_CELL, fontName=_FONT_B, fontSize=8.6,
                      leading=10.4, textColor=colors.white)
S_SUBH = ParagraphStyle("sh", parent=ss["Heading2"], fontName=_FONT_B,
                       fontSize=10.2, leading=12.4, textColor=INK, spaceBefore=0, spaceAfter=3)


SECTION_BAND = {
    1: ("Problem Understanding", "1 of 9"),
    2: ("Proposed Solution", "2 of 9"),
    3: ("Proposed Solution", "3 of 9"),
    4: ("Users and Context", "4 of 9"),
    5: ("Users and Context", "5 of 9"),
    6: ("Innovation and Creativity", "6 of 9"),
    7: ("Innovation and Creativity", "7 of 9"),
    8: ("Technology and Data Feasibility", "8 of 9"),
    9: ("Technology and Data Feasibility", "9 of 9"),
}


def _page_chrome(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, H - 2.2 * mm, W, 2.2 * mm, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, H - 2.2 * mm, W * 0.16, 2.2 * mm, stroke=0, fill=1)
    canvas.setFillColor(INK)
    canvas.rect(0, 0, W, 8.6 * mm, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, 8.6 * mm, W * 0.28, 1.6 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#F0FDFA"))
    canvas.setFont(_FONT, 7.6)
    canvas.drawString(M, 3.6 * mm,
                      "A2Z  ·  Samanantar  ·  Challenge 02 Learning-Level Visibility"
                      "  ·  Ideate proposal, 27 Sept 2026")
    canvas.drawRightString(W - M, 3.6 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _band(kicker, title, num):
    """Full-width teal section header: title + section label, slide number right."""
    head, meta = SECTION_BAND[num]
    t = Table([[Paragraph(title, S_BANDH),
                Paragraph(f'<font size=8 color=#CCFBF1>{head}</font>', S_CELLR),
                Paragraph(f'<font size=13><b>{num}</b></font> <font size=7>of 9</font>', S_CELLRR)]],
              colWidths=[150 * mm, 64 * mm, 23 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("VALIGN", (2, 0), (2, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LINEAFTER", (1, 0), (1, -1), 0.7, colors.white),
        ("LINEBEFORE", (2, 0), (2, -1), 0.7, colors.white),
    ]))
    return t


def _loop_diagram(width, height):
    """The five-minute loop as a horizontal pipeline of five cards."""
    d = Drawing(width, height)
    LIGHT = colors.HexColor("#F0FDFA")
    DARK = colors.HexColor("#134E4A")
    steps = [
        ("1 · SCREEN", TEAL, colors.white, ["10-second screener", "rolls the ID gate"]),
        ("2 · LISTEN", BAND, TEAL, ["5-item ASER ladder,", "or the teacher taps"]),
        ("3 · DIAGNOSE", colors.HexColor("#FEF3C7"), AMBER, ["Claude: level,", "misconception, page"]),
        ("4 · GROUP", BAND, TEAL, ["bench map,", "max 8 per bench"]),
        ("5 · TEACH", TEAL, colors.white, ["5-min activity", "+ parent note"]),
    ]
    cw = (width - 4 * 9) / 5.0
    for i, (title, fill, txt, lines) in enumerate(steps):
        x = i * (cw + 9)
        d.add(Rect(x, 0, cw, height - 4, rx=6, ry=6, fillColor=fill,
                   strokeColor=(INK if fill is TEAL else TEAL), strokeWidth=0.8))
        d.add(String(x + cw / 2, height - 12, title, fontName="Helvetica-Bold",
                     fontSize=6.4, fillColor=txt, textAnchor="middle"))
        body = DARK if (txt is AMBER or txt is TEAL) else LIGHT
        for j, ln in enumerate(lines):
            d.add(String(x + cw / 2, height - 22 - j * 7.6, ln, fontName="Helvetica",
                         fontSize=5.4, fillColor=body, textAnchor="middle"))
        if i < 4:
            ax = x + cw
            ay = (height - 4) / 2
            d.add(Line(ax + 1, ay, ax + 8, ay, strokeColor=AMBER, strokeWidth=1.3))
            d.add(Polygon([ax + 8, ay, ax + 4.6, ay + 2.6, ax + 4.6, ay - 2.6],
                          fillColor=AMBER, strokeColor=None))
    return d


def _pictogram(width, height):
    """7 of 10 children cannot read a Grade 2 text — ten child glyphs, 7 shaded."""
    d = Drawing(width, height)

    def glyph(cx, cy, sz, filled):
        hc = INK if filled else RULE
        d.add(Circle(cx, cy + sz * 0.42, sz * 0.20, fillColor=hc, strokeColor=None))
        d.add(Line(cx, cy + sz * 0.22, cx, cy - sz * 0.05, strokeColor=hc, strokeWidth=sz * 0.16))
        d.add(Line(cx, cy - sz * 0.05, cx - sz * 0.18, cy - sz * 0.42, strokeColor=hc,
                   strokeWidth=sz * 0.16))
        d.add(Line(cx, cy - sz * 0.05, cx + sz * 0.18, cy - sz * 0.42, strokeColor=hc,
                   strokeWidth=sz * 0.16))
        d.add(Line(cx - sz * 0.24, cy + sz * 0.16, cx + sz * 0.24, cy + sz * 0.16,
                   strokeColor=hc, strokeWidth=sz * 0.14))

    step = width / 10.0
    sz = min(height * 0.92, step * 0.8)
    x0 = (width - step * 9) / 2
    cy = height / 2 - sz * 0.05
    for i in range(10):
        glyph(x0 + i * step, cy, sz, i < 7)
    return d


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(RULE)
    canvas.rect(0, 0, W, 7 * mm, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, 7 * mm, W * 0.28, 1.6 * mm, stroke=0, fill=1)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawString(M, 3.4 * mm,
                      "A2Z  ·  Samanantar  ·  Challenge 02 Learning-Level Visibility  ·  Ideate proposal, 27 Sept 2026")
    canvas.drawRightString(W - M, 3.4 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _flow_diagram(width, height):
    """Data-flow diagram required by Guidelines §4 for the Technology and
    Data feasibility section. Marks where AI acts and where it is bounded."""
    d = Drawing(width, height)
    lanes = [
        ("USER INPUT", 0.00, ["Teacher taps roll ID", "Child reads aloud,", "or points at a card"], PAPER, INK, "input"),
        ("ON-DEVICE AI", 0.185, ["IndicConformer ASR", "(AI4Bharat, ONNX)", "-> transcript + conf"], BAND, TEAL, "ai"),
        ("AI RELIABILITY", 0.37, ["Matra-weighted scorer", "conf >= 80%? else", "-> ask teacher to tap"],
         colors.HexColor("#FEF3C7"), AMBER, "bound"),
        ("FRONTIER AI", 0.555, ["Claude diagnoses", "-> level, misconception,", "NCERT page, Hindi hint"],
         TEAL, colors.white, "ai"),
        ("GUARDRAILS", 0.74, ["Tool schema, temp 0,", "no invented pages,", "teacher 1-tap override"], BAND, INK, "bound"),
        ("OUTPUT", 0.925, ["Bench map + sticky note", "parent page + event log"], PAPER, INK, "output"),
    ]
    d.add(Rect(0, 0, width, height, rx=0, ry=0, fillColor=None, strokeColor=None))

    # Reserve a caption band INSIDE the drawing bounds. Drawing the caption
    # below y=0 lets it collide with the next flowable, which produced
    # overlapping, unreadable text in an earlier build.
    CAP_H = 9.0
    lane_h = height - CAP_H
    bw = width / 6.0 - 6
    for i, (title, yf, lines, fill, txt, kind) in enumerate(lanes):
        # every lane sits on the SAME baseline so the diagram reads as one
        # horizontal pipeline; boxes start ABOVE the caption band so the
        # caption is never hidden behind them
        y = CAP_H
        h = lane_h - CAP_H
        x = i * (width / 6.0) + 3
        is_ai = kind == "ai"
        d.add(Rect(x, y, bw, h, rx=5, ry=5, fillColor=fill,
                   strokeColor=(TEAL if is_ai else RULE), strokeWidth=(1.5 if is_ai else 0.7)))
        ty = y + h - 9
        d.add(String(x + bw / 2, ty, title, fontName="Helvetica-Bold", fontSize=5.2,
                     fillColor=txt, textAnchor="middle"))
        for j, ln in enumerate(lines):
            d.add(String(x + bw / 2, ty - 9.5 - j * 8.0, ln, fontName="Helvetica", fontSize=5.0,
                         fillColor=(colors.white if is_ai else MUTED), textAnchor="middle"))
        if i < 5:
            ax, ay = x + bw, y + h / 2
            d.add(Line(ax, ay, ax + 6, ay, strokeColor=TEAL, strokeWidth=1.1))
            d.add(Polygon([ax + 6, ay, ax + 2.4, ay + 2.4, ax + 2.4, ay - 2.4],
                          fillColor=TEAL, strokeColor=None))

    # feedback loop, entirely within the reserved band
    d.add(Line(width / 2, CAP_H, width / 2, CAP_H - 3.5, strokeColor=AMBER,
               strokeWidth=0.9, strokeDashArray=[2, 2]))
    d.add(String(width / 2, 0.5,
                 "append-only encrypted event log  ·  teacher override and Rasch "
                 "difficulty update feed the next child",
                 fontName="Helvetica-Oblique", fontSize=5.0, fillColor=AMBER,
                 textAnchor="middle"))
    return d


def build(path: str) -> str:
    doc = BaseDocTemplate(path, pagesize=PAGE, leftMargin=M, rightMargin=M,
                          topMargin=9 * mm, bottomMargin=8.5 * mm,
                          title="Samanantar — Ideate Proposal (Team A2Z)",
                          author="A2Z", subject="AI for Foundational Learning — Challenge 02")
    doc.addPageTemplates([PageTemplate(
        id="p", frames=[Frame(M, 8.5 * mm, W - 2 * M, H - 17.5 * mm, id="f")],
        onPage=_page_chrome)])

    def tbl(data, widths, head=True, zebra=True, pad=2.1):
        t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
        cmds = [("GRID", (0, 0), (-1, -1), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), pad),
                ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
        if head:
            cmds += [("BACKGROUND", (0, 0), (-1, 0), TEAL)]
        if zebra:
            for i in range(1 if head else 0, len(data)):
                if i % 2 == 0:
                    cmds.append(("BACKGROUND", (0, i), (-1, i), BAND))
        t.setStyle(TableStyle(cmds))
        return t

    st = []
    P = lambda txt, style=S_BODY: Paragraph(txt, style)

    # ═══════════ TITLE (excluded from the 7–10 count) ═══════════
    st.append(Spacer(1, 3 * mm))
    st.append(P("AI FOR FOUNDATIONAL LEARNING  ·  STAGE 1 IDEATE PROPOSAL  ·  TEAM A2Z", S_KICKER))
    st.append(P("Samanantar", S_TITLE))
    st.append(P("In five minutes, on the phone already in the classroom, a Grade 1–3 teacher finds out "
                "where each child actually stands — the exact reading level, the one specific thing the "
                "child is getting wrong, and the textbook page that fixes it.", S_SUB))
    st.append(Spacer(1, 1.8 * mm))
    st.append(_loop_diagram(W - 2 * M, 13 * mm))
    st.append(Spacer(1, 2.2 * mm))
    st.append(Table([[[
        Paragraph("THE PROBLEM, IN ONE PICTURE", S_SUBH),
        Spacer(1, 1 * mm),
        _pictogram(112 * mm, 10 * mm),
        Paragraph('<font size=7.8 color=#5A6B73>7 of 10 children in Grade 3 cannot read a '
                  'Grade 2 text (ASER 2024) — and the teacher cannot see <i>which</i> seven '
                  'while they are still in her room.</font>', S_BODY),
    ], [
        Paragraph("THE THREE NUMBERS THE WHOLE PROPOSAL TURNS ON", S_SUBH),
        Spacer(1, 1 * mm),
        Table([[Paragraph('<b>12.4</b><br/><font size=6.6 color=#5A6B73>minutes of '
                          'one-to-one time to assess one child on paper</font>', S_STATNUM),
                Paragraph('<b>3–5</b><br/><font size=6.6 color=#5A6B73>minutes per child '
                          'with Samanantar, on the phone she already owns</font>', S_STATNUM),
                Paragraph('<b>4.2×</b><br/><font size=6.6 color=#5A6B73>more children '
                          'reached in the same teaching time</font>', S_STATNUM)]],
              colWidths=[37.5 * mm, 37.5 * mm, 37.5 * mm],
              style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), BAND),
                                ('BOX', (0, 0), (-1, -1), 0.7, TEAL),
                                ('INNERGRID', (0, 0), (-1, -1), 0.7, TEAL),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('TOPPADDING', (0, 0), (-1, -1), 3.5),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
                                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 5)])),
    ]]], colWidths=[115 * mm, 122 * mm],
        style=TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                          ('LEFTPADDING', (0, 0), (-1, -1), 0),
                          ('RIGHTPADDING', (0, 0), (0, 0), 8 * mm),
                          ('LEFTPADDING', (1, 0), (1, 0), 0)])))
    st.append(tbl([
        [P("Challenge", S_CELLB), P("<b>02 · Learning-Level Visibility</b>", S_CELL),
         P("Sub-part we address", S_CELLB),
         P("Child-level diagnostic visibility — the teacher cannot see where each child actually is, while the child is still in the room", S_CELL)],
        [P("Team", S_CELLB), P("<b>A2Z</b> — 2 members: Venkata Narayana G V, Mahesh Babu Ch", S_CELL),
         P("Why frontier AI makes this possible only now", S_CELLB),
         P("Frontier models only recently gained tool-use, so a diagnosis can be forced into an auditable shape, and reliable reasoning over short, noisy, code-switched text. A 2023 team could not have made this output trustworthy. A rules-only team cannot disambiguate it at all.", S_CELL)],
        [P("Built with", S_CELLB),
         P("Claude (Anthropic) · AI4Bharat IndicWhisper / IndicConformer · ONNX Runtime", S_CELL),
         P("Submission", S_CELLB), P("This PDF · 9 content slides · via Hack2Skill by 27 Sept 2026, 23:59 · one of two distinct submissions (see Team page)", S_CELL)],
    ], [22 * mm, 74 * mm, 36 * mm, 105 * mm], head=False, zebra=False))
    st.append(Spacer(1, 3.2 * mm))
    st.append(tbl([
        [P("Slide", S_TH), P("Mandated section", S_TH), P("What this slide answers", S_TH)],
        [P('<font size=11 color=#0D9488><b>1</b></font>'), P("Problem Understanding"), P("Who is affected, how the harm happens, and why it survived 15 years of measurement", S_CELL)],
        [P('<font size=11 color=#0D9488><b>2</b></font>'), P("Proposed Solution · 1 of 2"), P("The five-minute loop, and why each step should improve outcomes", S_CELL)],
        [P('<font size=11 color=#0D9488><b>3</b></font>'), P("Proposed Solution · 2 of 2"), P("Where the frontier model works, component by component, and how it is bounded", S_CELL)],
        [P('<font size=11 color=#0D9488><b>4</b></font>'), P("Users and Context · 1 of 2"), P("Three real users, their constraints, and the user journey map", S_CELL)],
        [P('<font size=11 color=#0D9488><b>5</b></font>'), P("Users and Context · 2 of 2"), P("The constraints we designed against, and what each one cost us", S_CELL)],
        [P('<font size=11 color=#0D9488><b>6</b></font>'), P("Innovation and Creativity · 1 of 2"), P("What is genuinely new, what is prior art, and why only now", S_CELL)],
        [P('<font size=11 color=#0D9488><b>7</b></font>'), P("Innovation and Creativity · 2 of 2"), P("Head-to-head against paper ASER, PadhAI, generic LLM tutors and classic TaRL", S_CELL)],
        [P('<font size=11 color=#0D9488><b>8</b></font>'), P("Technology and Data · 1 of 2"), P("Stack, resources, and the role AI plays at every layer", S_CELL)],
        [P('<font size=11 color=#0D9488><b>9</b></font>'), P("Technology and Data · 2 of 2"), P("Data-flow diagram, offline degradation, evaluation plan and 3-week build", S_CELL)],
    ], [12 * mm, 56 * mm, 167 * mm]))
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl([
        [P("WHO IT IS FOR", S_TH),
         P("A Grade 1–3 government teacher: 35–45 children, three grades in one room, "
           "15–20 minutes of level-appropriate teaching a day, an Rs 8k–12k Android, and no "
           "reliable network.", S_CELL),
         P("WHAT SHE GETS", S_TH),
         P("A per-child level, one named misconception, and the exact NCERT page to open next — "
           "in under five minutes, with tap input whenever the room is too loud for the "
           "microphone.", S_DENSE)],
    ], [22 * mm, 93 * mm, 22 * mm, 100 * mm], head=False, zebra=False, pad=2.1))
    st.append(PageBreak())

    # ═══════════ 1 · PROBLEM UNDERSTANDING (35% criterion) ═══════════
    st.append(P("SECTION 1 · PROBLEM UNDERSTANDING", S_GHOST))
    st.append(P("SECTION 1 · PROBLEM UNDERSTANDING", S_GHOST))
    st.append(_band("SECTION 1 · PROBLEM UNDERSTANDING",
                    "The teacher is not failing to teach. She is failing to see.", 1))
    st.append(Spacer(1, 1.6 * mm))
    leftc = [
        P("ASER 2024 finds that around <b>7 in 10 Grade 3 children cannot read a Grade 2-level text</b>, "
          "and roughly <b>2 in 3 cannot do basic subtraction</b>. The gap is large, well documented, and "
          "measured every year. <b>What is missing is not measurement. It is action at the moment of "
          "teaching.</b>", S_BODY),
        P("<b>Why this has survived fifteen years of ASER.</b> ASER is an excellent survey instrument and "
          "an impractical classroom tool. It needs a trained assessor, 10–15 minutes per child, and a "
          "paper record. Forty-five children is nine hours of one-to-one time. So it is done once, on a "
          "sample, and the result arrives months after the teaching decision it should have informed. "
          "<b>The gap persists because measurement and action have been decoupled.</b>", S_BODY),
        P("<b>Who is affected.</b> The primary government-school teacher of a Grade 1–3 multi-grade "
          "classroom: typically 35–45 children across three grades, with 15–20 minutes of level-appropriate "
          "teaching time a day. She knows roughly that some children cannot read — not which ones, not at "
          "what level, not what to do in the next five minutes.", S_BODY),
        P("<b>Secondary victims.</b> The child two levels behind who is never identified; the child bored "
          "because the class is pitched at the middle; and the returner after four days of absence, who "
          "has no prioritised catch-up path and silently compounds the loss.", S_BODY),
    ]
    rightc = [
        P("Today, a Grade 1–3 teacher with 45 children", S_SUBH),
        Spacer(1, 1 * mm),
        tbl([
            [P("What she does", S_TH), P("Consequence", S_TH)],
            [P("Assesses one child with a printed oral tool: <b>10–15 minutes</b> of one-to-one time."),
             P("45 × 12 min = <b>9 hours</b>. Impossible in a day, so it does not happen.")],
            [P("Has no per-child record, so the same question is re-asked every term."),
             P("<b>Regression is invisible.</b> A child who slipped two levels looks identical to one who did not.")],
            [P("Groups by grade, because that is the only grouping available to her."),
             P("In a mixed group the middle is served and both tails lose — exactly what TaRL evidence predicts.")],
            [P("Handles absenteeism by re-teaching the whole class."),
             P("<b>Missed days compound</b> with no prioritised catch-up list.")],
            [P("Existing edtech (PadhAI and similar) delivers <i>content</i> to a device."),
             P("Content without a per-child starting point is the same problem again, on a screen.")],
        ], [78 * mm, 59 * mm], pad=2.4),
        Spacer(1, 1.5 * mm),
        P("The specific aspect we address", S_SUBH),
        Spacer(1, 0.8 * mm),
        P("Not “improve Indian education”, and not a new learning app. We address the single missing "
          "instrument: <b>a reliable, per-child, within-five-minute reading and numeracy level, plus the "
          "one matching first activity</b> — delivered on the phone the teacher already owns, in a room "
          "too noisy for speech recognition to be trusted on its own.", S_CELL),
    ]
    row = Table([[leftc, rightc]], colWidths=[94 * mm, 143 * mm], style=TableStyle([
        ("BACKGROUND", (1, 0), (1, 0), BAND)]))
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (0, 0), 0),
                             ("RIGHTPADDING", (0, 0), (0, 0), 6 * mm),
                             ("LEFTPADDING", (1, 0), (1, 0), 0),
                             ("LINEBEFORE", (1, 0), (1, 0), 0.5, RULE)]))
    st.append(row)
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl([
        [P("The three needs the challenge names, and what we return for each", S_TH)],
        [P("<font size=7 color='#5A6B73'>The official Challenge 02 statement: “A teacher often teaches a "
           "class without a clear understanding of each child's actual learning level, and therefore lacks "
           "actionable insights on <b>where a lesson should begin</b>, <b>which misconceptions need to be "
           "solved</b>, or <b>which form of remediation support is required</b> by the children.”</font>", S_CELL)],
    ], [237 * mm], head=True, zebra=False, pad=2.6))
    st.append(Spacer(1, 1 * mm))
    st.append(tbl(
        [[P("Need", S_TH), P("As the challenge states it", S_TH), P("What Samanantar returns", S_TH)]]
        + [[P(n, S_CELLB), P(b, S_CELL), P(o, S_CELL)] for n, b, o in NEED_TO_OUTPUT],
        [10 * mm, 62 * mm, 165 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(Table([[
        [P("<b>7 in 10</b>", S_STATNUM),
         P("Grade 3 children who cannot read a Grade 2-level text (ASER 2024).", S_DENSE)],
        [P("<b>2 in 3</b>", S_STATNUM),
         P("cannot do basic subtraction at the same grade.", S_DENSE)],
        [P("<b>9 hours</b>", S_STATNUM),
         P("to assess 45 children one-to-one on paper — so it never happens.", S_DENSE)],
        [P("<b>12.4 min</b>", S_STATNUM),
         P("stopwatch time per child on paper. The budget we compress to under five.", S_DENSE)],
    ]], colWidths=[59.25 * mm, 59.25 * mm, 59.25 * mm, 59.25 * mm],
        style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), BAND),
                          ('BOX', (0, 0), (-1, -1), 0.7, TEAL),
                          ('INNERGRID', (0, 0), (-1, -1), 0.7, TEAL),
                          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                          ('TOPPADDING', (0, 0), (-1, -1), 4),
                          ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                          ('LEFTPADDING', (0, 0), (-1, -1), 5),
                          ('RIGHTPADDING', (0, 0), (-1, -1), 5)])))
    st.append(PageBreak())
    # ═══════════ 2 · PROPOSED SOLUTION 1/2 ═══════════
    st.append(P("SECTION 2 · PROPOSED SOLUTION (1 OF 2)", S_GHOST))
    st.append(_band("SECTION 2 · PROPOSED SOLUTION (1 OF 2)",
                    "Assess, diagnose, group, teach — in five minutes", 2))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Step", S_TH), P("What the teacher does", S_TH), P("What the system returns", S_TH), P("Time", S_TH)],
        [P("1 · Screen", S_CELLB),
         P("Opens the app, taps the roll ID. A <b>10-second name-and-letter screener</b> runs first — the "
           "ASER “pre-letter” floor, which is where most Grade 1–3 children actually sit."),
         P("A gate decision: can this child read letters at all? This one gate is the single biggest "
           "time-saver in the product."), P("10 s", S_CELL)],
        [P("2 · Listen", S_CELLB),
         P("Child reads five items on the ASER ladder — <b>Pre-Letter, then Letter, Word, Paragraph, "
           "Story</b>. The teacher may tap instead of speak at any moment."),
         P("A transcript, a confidence, and a <b>trust verdict</b>. Below 80% confidence the app refuses "
           "to judge the child and asks for a tap."), P("2–3 min", S_CELL)],
        [P("3 · Diagnose", S_CELLB),
         P("Nothing. This is the AI step, and it is invisible to her."),
         P("An ASER level, <b>one named misconception</b> — “drops the long-i matra, so she is decoding, "
           "not reading” — the exact <b>NCERT page</b>, and a five-minute hint in simple Hindi."),
         P("&lt;1 s", S_CELL)],
        [P("4 · Group", S_CELLB),
         P("Glances at the bench map: 6 children at Pre-Letter, 9 at Letter, 7 at Word."),
         P("Three benches, <b>max 8 per bench</b>, regrouped weekly. Grouped by level, never by grade."),
         P("30 s", S_CELL)],
        [P("5 · Teach", S_CELLB),
         P("Runs the suggested five-minute activity for one bench using the textbook already on her desk, "
           "then logs 30 seconds of fidelity."),
         P("A one-page parent note and a level certificate. Next session starts from the new level, not "
           "from zero."), P("5 min", S_CELL)],
    ], [20 * mm, 76 * mm, 78 * mm, 13 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(P("Why this should improve outcomes — three mechanisms, each tied to evidence rather than intuition", S_SUBH))
    st.append(Spacer(1, 1 * mm))
    st.append(tbl([
        [P("Mechanism", S_TH), P("Why it works", S_TH), P("Evidence it leans on", S_TH)],
        [P("<b>Right level, right now</b> — remediation targets the diagnosed gap, not the grade syllabus."),
         P("Teaching at the Right Level is the strongest-evidenced intervention in this space precisely "
           "because it groups by measured level and teaches at that level. Samanantar is the measurement "
           "and targeting layer that makes TaRL executable inside a normal 15-minute period, rather than "
           "inside a scheduled 60-minute session that most schools cannot staff."),
         P("J-PAL Teaching at the Right Level evidence review; NIPUN Bharat's grouping-by-level guidance.")],
        [P("<b>Misconception, not score</b> — she is told <i>what went wrong</i>, not just <i>what she scored</i>."),
         P("“40%” produces no action. “She drops the final vowel sign, so run the blending activity on "
           "page 24” tells her exactly which five minutes to spend. The diagnostic is the difference "
           "between a report and a plan."),
         P("Error-taxonomy remediation is established practice in RTI and maths intervention; we apply it "
           "to foundational reading.")],
        [P("<b>Time is the binding constraint</b> — the whole product exists to turn 12 minutes per child into 4."),
         P("No pedagogy survives a teacher who has nine hours of assessment to do in a six-hour day. "
           "Efficiency here is not a convenience; it is the adoption mechanism, and it is the thing that "
           "makes the other two mechanisms happen at all."),
         P("ASER oral assessment time; we will measure teacher minutes per child with a stopwatch in the "
           "pilot, not from recall.")],
    ], [56 * mm, 100 * mm, 81 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("THE WHOLE LOOP, END TO END", S_TH)],
        [P("Screen 10 s → Listen 2–3 min → Diagnose <1 s → Group 30 s → Teach 5 min. The "
           "teacher's total hands-on time per child stays inside the five-minute budget, and the "
           "diagnosis arrives before the child has left the reading card.", S_DENSE)],
    ], [237 * mm], head=True, zebra=False, pad=2.1))
    st.append(PageBreak())

    # ═══════════ 3 · PROPOSED SOLUTION 2/2 — THE AI LAYER (25% criterion) ═══════════
    st.append(_band("SECTION 2 · PROPOSED SOLUTION (2 OF 2) — WHERE THE FRONTIER AI ACTUALLY WORKS",
                    "Two models decide. Two deterministic guards keep them honest.", 3))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Component", S_TH), P("Model / method", S_TH), P("What it is given", S_TH),
         P("What it returns", S_TH), P("Why this needs AI rather than a lookup table", S_TH)],
        [P("<b>1 · Diagnostic reasoner</b><br/><font size=6.6 color='#5A6B73'>ai.py · LlmDiagnostic</font>", S_CELLB),
         P("<b>Claude</b> (Anthropic). Forced tool call, temperature 0, structured JSON.", S_CELL),
         P("The content-pack item verbatim, its exact NCERT page, its CBSE FLN skill, what the recogniser "
           "heard, the confidence, whether a teacher overrode it, and the room noise level.", S_CELL),
         P("ASER level, one misconception code, a one-sentence teacher hint in simple Hindi citing that "
           "NCERT page, the Concrete–Representational–Abstract stage, and a calibrated confidence.", S_CELL),
         P("The same surface form — a short Devanagari string, low confidence, in a 60 dB room — has at "
           "least three causes: a genuine decoding failure, a recogniser error, or a child who is not "
           "speaking. Separating them is <i>disambiguation under noise</i>. A lookup table cannot do that; "
           "it can only report whichever row it was handed. This is the step we hand to the model, and the "
           "tool schema is what makes its answer auditable.")],
        [P("<b>2 · Speech recognition</b><br/><font size=6.6 color='#5A6B73'>IndicASR umbrella</font>", S_CELLB),
         P("<b>IndicWhisper / IndicConformer</b> (AI4Bharat), on-device ONNX Runtime.", S_CELL),
         P("16 kHz mono audio of one child reading one item.", S_CELL),
         P("A Devanagari transcript plus a confidence, entirely on the device.", S_CELL),
         P("Indic ASR is the only realistic way to transcribe a six-year-old's code-switched Hindi in a "
           "noisy room with no network. It runs on-device because the classroom has no reliable "
           "connectivity and a child's voice must not leave the school.")],
        [P("<b>3 · AI reliability layer</b><br/><font size=6.6 color='#5A6B73'>ai.py · AsrScorer</font>", S_CELLB),
         P("Matra-weighted keyword spotting plus a noise-adjusted confidence gate. Deterministic, by design.", S_CELL),
         P("The target string, the hypothesis, the raw confidence, and the noise level.", S_CELL),
         P("Usable or gated, weighted similarity, correct or not, and <b>needs-tap</b>.", S_CELL),
         P("This is what makes the other two safe to trust with a child. Below 80% confidence the system "
           "refuses to judge and hands control to the teacher, because falsely telling a teacher “this "
           "child cannot read” is far more damaging than the reverse. We also weight a lost vowel sign "
           "three times a lost consonant, because in Devanagari a lost matra changes the <i>word</i>: a "
           "naive character distance scored <i>bil-li</i> against <i>billi</i> at 0.83 and wrongly passed "
           "it — a real bug we found and fixed.")],
        [P("<b>4 · Self-calibrating instrument</b><br/><font size=6.6 color='#5A6B73'>ai.py · DifficultyModel</font>", S_CELLB),
         P("1PL / Rasch item-response model. The mathematics is prior art; the deployment is not.", S_CELL),
         P("Every administered item and whether the child got it right, accumulated across the class and "
           "across weeks.", S_CELL),
         P("A live difficulty estimate per item, the next item to administer, and an early-stop decision.", S_CELL),
         P("It keeps the assessment inside the five-minute budget — a child who fails twice is stepped "
           "down immediately instead of grinding through a level — and it sharpens the instrument from "
           "our own classroom with no training set and no labels. <b>Rasch is decades old and we credit it; "
           "the novelty is running it live, unsupervised, per session.</b>")],
    ], [32 * mm, 38 * mm, 48 * mm, 45 * mm, 74 * mm], pad=1.6))
    st.append(Spacer(1, 1.0 * mm))
    st.append(P("<b>Human-in-the-loop is the default, not a fallback.</b> The teacher can override any single "
                "ASR judgement with one tap, and that override is logged as a fidelity datum. When the model is "
                "unreachable — a judge's laptop in airplane mode, a school with no network — a documented "
                "rule path takes over so the product never breaks, and the audit log records which path produced "
                "every result.", S_CELL))
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl([
        [P("ONE AUDITABLE CALL", S_TH),
         P('resp = client.messages.create(model=..., temperature=0, tools=[DIAGNOSTIC_TOOL], '
           "tool_choice={'type':'tool','name':'record_diagnosis'}, messages=[...])", S_CODE),
         P("Every diagnosis is one forced tool call: the schema fixes the output shape, "
           "temperature 0 makes it reproducible, and the audit log records whether the LLM or the "
           "documented rule fallback produced each result.", S_DENSE)],
        [P("Fallback rule path", S_DENSEB),
         P("With no network, ai.py routes the same item through a documented deterministic "
           "path and marks the result in AI_AUDIT, so the two are never confused.", S_DENSE)],
        [P("Cost per diagnosis", S_DENSEB),
         P("One Claude call, sub-second, cents-level; the Rasch early-stop means most "
           "children need fewer items, not more calls.", S_DENSE)],
    ], [30 * mm, 118 * mm, 89 * mm], head=False, zebra=False, pad=2.6))
    st.append(PageBreak())

    # ═══════════ 4 · USERS AND CONTEXT 1/2 (35% criterion) ═══════════
    st.append(P("SECTION 3 · USERS AND CONTEXT (1 OF 2)", S_GHOST))
    st.append(_band("SECTION 3 · USERS AND CONTEXT (1 OF 2)",
                    "Built for one user, on one device, in one kind of room", 4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("User", S_TH), P("Context, as observed and assumed", S_TH), P("What that forces in the design", S_TH)],
        [P("<b>Primary — the Grade 1–3 government teacher</b><br/>Mrs. Sharma, 45 children, three grades in "
           "one room, 15–20 minutes of level-appropriate teaching time a day.", S_CELL),
         P("Owns a low-end Android phone (Rs 8k–12k, 1–2 GB RAM). Classroom noise routinely 50–60 dB. No "
           "projector, no laptop, no reliable network. Trained in pedagogy, not in software, and will not "
           "read a manual. Adopts nothing that adds preparation time.", S_CELL),
         P("Offline-first with zero network calls in the assessment path. A 48 dp minimum touch target. "            "One-handed, thumb-reachable controls. Every remediation expressed in terms of the textbook "
           "already on her desk. No login, no account, no onboarding training. Touch targets stay at "
           "48 dp so the app works one-handed, on the move, in a crowded room.")],
        [P("<b>Secondary — the child being assessed</b><br/>Age 5–9, often a first-generation learner, and "
           "the home language may differ from the school language.", S_CELL),
         P("Cannot read instructions. Loses attention in roughly 90 seconds. Shy in front of a visitor. May "
           "not have the vocabulary for the target word. A 60 dB room with 45 other children.", S_CELL),
         P("A 10-second screener that fails fast rather than a long test. Voice input with a tap "
           "alternative, because pointing at a card is always available even when speech is not. No child "
           "is asked to read anything the teacher has not confirmed is age-appropriate.")],
        [P("<b>Tertiary — the parent</b><br/>Rarely in the classroom; receives information second-hand.", S_CELL),
         P("Often does not read English. Wants to know what to do at home, with nothing to buy.", S_CELL),
         P("A one-page note in the local language, printed from the teacher's phone, naming the exact book "
           "and page. No app to install, no login, and no data about the child leaves the school.")],
    ], [50 * mm, 94 * mm, 93 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(P("User journey — a normal Tuesday, Grade 1–3, 40 children present", S_SUBH))
    st.append(Spacer(1, 1 * mm))
    st.append(tbl([
        [P("", S_TH), P("1 · Before school", S_TH), P("2 · Opening minute", S_TH),
         P("3 · During level time", S_TH), P("4 · End of day", S_TH), P("5 · Next week", S_TH)],
        [P("<b>Teacher</b>", S_CELLB),
         P("Opens the bench map from last week. Two children are flagged as having fallen behind. One has "
           "been absent four days."),
         P("Taps <b>Assess</b>, enters the roll ID SCH01-CL2-017, and starts the 10-second screener."),
         P("Runs three benches for five minutes each, using the suggested NCERT page. Logs 30 seconds of "
           "fidelity at the end."),
         P("Prints one parent note and a level certificate. The event log syncs when a network appears, or "
           "never."),
         P("Regroups automatically. The four-day absentee now has a prioritised 3 × 5-minute catch-up plan.")],
        [P("<b>Child</b>", S_CELLB),
         P("Nothing — no preparation, no homework."),
         P("Says their own name; 10 seconds, then the ladder begins."),
         P("Reads or points at five cards. The app never judges a child on audio it is not confident about."),
         P("Takes home a one-page note naming the exact page to practise."),
         P("Is seated with peers at the same level, not at their grade.")],
        [P("<b>System</b>", S_CELLB),
         P("Surfaces the absentee and the two regressions."),
         P("ASR runs on-device; the confidence gate decides whether audio is trustworthy at all."),
         P("Claude returns level, misconception, NCERT page and a Hindi hint; the Rasch model decides when "
           "to stop."),
         P("Append-only event store; nothing is lost if the battery dies mid-assessment."),
         P("Level gains accumulate per child; fidelity and override rates feed the pilot report.")],
    ], [18 * mm, 44 * mm, 44 * mm, 56 * mm, 40 * mm, 35 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("PLANNED FEATURES BORN FROM THESE CONSTRAINTS", S_TH)],
        [P("10-second screener gate  ·  tap-while-speaking hybrid input  ·  one-tap teacher "
           "override logged as a fidelity datum  ·  attendance heat strip with automatic "
           "catch-up plans  ·  one-page printable parent note in the local language  ·  "
           "event-sourced storage so a dead battery never loses an assessment.", S_DENSE)],
    ], [237 * mm], head=True, zebra=False, pad=2.1))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Feature", S_TH), P("Constraint that forces it", S_TH), P("Where it lives", S_TH)],
        [P("Tap-while-speaking hybrid input", S_DENSEB),
         P("A 45-60 dB room makes speech unreliable as a sole channel.", S_DENSE),
         P("Assessment screen; the tap path is always one thumb away.", S_DENSE)],
        [P("One-tap teacher override", S_DENSEB),
         P("A wrong automated judgement costs more than a slow confirmed one.", S_DENSE),
         P("Every item screen; each override is logged as a fidelity datum.", S_DENSE)],
        [P("Resume-after-kill event store", S_DENSEB),
         P("Shared phone, flat battery, an interrupted school day.", S_DENSE),
         P("Append-only encrypted log; state replays on next open.", S_DENSE)],
    ], [52 * mm, 95 * mm, 90 * mm], pad=1.9))
    st.append(PageBreak())

    # ═══════════ 5 · USERS AND CONTEXT 2/2 ═══════════
    st.append(P("SECTION 3 · USERS AND CONTEXT (2 OF 2)", S_GHOST))
    st.append(_band("SECTION 3 · USERS AND CONTEXT (2 OF 2)",
                    "The constraints we designed against — and what each one cost us", 5))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Constraint", S_TH), P("Reality", S_TH), P("Design response", S_TH), P("What it costs us", S_TH)],
        [P("<b>The room is too loud for ASR</b>", S_CELLB),
         P("45–60 dB. A recogniser at 60 dB is not a reliable judge of whether a six-year-old can read.", S_CELL),
         P("Never let ASR judge alone. An 80% noise-adjusted confidence gate; matra-weighted scoring so a "
           "dropped vowel sign counts as an error; tap-while-speaking; one-tap teacher override; a "
           "conservative fallback whenever a transcript is unverified.", S_CELL),
         P("Some assessments need a tap. We accept that — a teacher-confirmed answer is worth more than a "
           "fast wrong one.")],
        [P("<b>Five minutes is the whole budget</b>", S_CELLB),
         P("15–20 minutes of level time a day, for 40+ children.", S_CELL),
         P("10-second screener, Rasch-driven early stop, five items maximum, a hard 5:00 cap with "
           "auto-diagnose, and max 8 per bench so one activity serves a whole group.", S_CELL),
         P("We cannot assess everything every day. We assess the floor fast and the ceiling rarely.")],
        [P("<b>Multi-grade, one teacher</b>", S_CELLB),
         P("Three grades in one room; benches, not grade sections.", S_CELL),
         P("Grouping strictly by level band with a spill-over bench, never by grade. A desk map shows where "
           "each child sits, so a bench can be formed by walking the room.", S_CELL),
         P("Benches change weekly, so recomputing the grouping has to be cheap. It is.")],
        [P("<b>Absenteeism compounds</b>", S_CELLB),
         P("A four-day absence inside the remediation window loses most of the gain.", S_CELL),
         P("An attendance heat strip on the dashboard, and an automatic prioritised catch-up plan naming the "
           "two specific gaps and three five-minute sessions.", S_CELL),
         P("Needs attendance marks. We make it one tap per child per day.")],
        [P("<b>The hardware is weak</b>", S_CELLB),
         P("Rs 8k–12k Android, 1–2 GB RAM, no GPU. A 7B model on device is not happening.", S_CELL),
         P("Only the small ASR model runs on device. Diagnosis runs server-side when a network exists and "
           "falls back to rules when it does not. All logic is event-sourced, so nothing depends on a live "
           "connection.", S_CELL),
         P("Diagnosis quality varies with connectivity. The audit log makes that measurable rather than hidden.")],
        [P("<b>Language</b>", S_CELLB),
         P("Hindi-medium instruction, home languages that differ, and code-switched speech.", S_CELL),
         P("The content pack is versioned per language on one schema. Pilot scope is <b>Hindi and Marathi "
           "only</b>, stated openly. Every prompt and hint lives in the pack, not in code.", S_CELL),
         P("We do not claim eight languages. Telugu is a version bump, not a rewrite.")],
        [P("<b>Child data</b>", S_CELLB),
         P("The classroom holds the most vulnerable data in the system.", S_CELL),
         P("Pseudonymous roll IDs, no photos, no names leaving the device, an encrypted append-only log, "
           "consent before assessment, and opt-in sync that can be disabled with zero feature loss.", S_CELL),
         P("Sync is genuinely optional. That is a constraint we chose to keep.")],
    ], [33 * mm, 48 * mm, 96 * mm, 60 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("THE HONEST LEDGER", S_TH),
         P("Every design response on this slide ships in the prototype today — the confidence "
           "gate, matra weighting, level-band grouping, catch-up plans and the encrypted "
           "append-only log are implemented and tested (74 tests green), not promised.", S_DENSE),
         P("The costs are stated, not hidden: taps instead of speech where the room wins, "
           "floor-fast assessment instead of full coverage, Hindi and Marathi before any other "
           "language.", S_DENSE)],
    ], [34 * mm, 111 * mm, 92 * mm], head=False, zebra=False, pad=2.1))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Guard-rail", S_TH), P("Value", S_TH), P("Enforced at", S_TH),
         P("What happens at the boundary", S_TH)],
        [P("Confidence gate", S_DENSEB), P("80%, noise-adjusted", S_DENSE),
         P("ai.py - AsrScorer", S_DENSE),
         P("Below the gate the app refuses to judge the child and asks for a tap.", S_DENSE)],
        [P("Matra weighting", S_DENSEB), P("Vowel sign costs 3x a consonant", S_DENSE),
         P("ai.py - AsrScorer", S_DENSE),
         P("A dropped matra scores as the error it is, not a near-match.", S_DENSE)],
        [P("Bench size", S_DENSEB), P("Max 8 per bench", S_DENSE),
         P("engines.py grouping", S_DENSE),
         P("Grouping stays walkable in a multigrade room.", S_DENSE)],
        [P("Session cap", S_DENSEB), P("5:00 hard stop", S_DENSE),
         P("Session timer", S_DENSE),
         P("Auto-diagnose on the evidence so far; the loop never overruns.", S_DENSE)],
        [P("Pilot scope", S_DENSEB), P("Hindi + Marathi first", S_DENSE),
         P("Content pack version", S_DENSE),
         P("A new language is a data bump, not a rewrite — and we say so.", S_DENSE)],
        [P("Child data", S_DENSEB), P("Pseudonymous, on-device", S_DENSE),
         P("Storage layer", S_DENSE),
         P("No names, photos or audio ever leave the school; sync is opt-in.", S_DENSE)],
        [P("Sync", S_DENSEB), P("Upload-only, optional", S_DENSE),
         P("Sync client", S_DENSE),
         P("Off by default; zero feature loss when it is disabled.", S_DENSE)],
    ], [34 * mm, 46 * mm, 42 * mm, 115 * mm], pad=2.3))
    st.append(PageBreak())

    # ═══════════ 6 · INNOVATION 1/2 (30% criterion) ═══════════
    st.append(P("SECTION 4 · INNOVATION AND CREATIVITY (1 OF 2)", S_GHOST))
    st.append(_band("SECTION 4 · INNOVATION AND CREATIVITY (1 OF 2)",
                    "What is genuinely new here — and what is honestly just prior art", 6))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("#", S_TH), P("Capability", S_TH), P("What is genuinely new", S_TH), P("What is prior art, and we say so", S_TH)],
        [P("1", S_CELLB),
         P("<b>Misconception-level diagnosis by a frontier model, bound to a page-precise pack.</b> Claude "
           "receives the item, its NCERT page, the raw transcript, the confidence, the noise and the "
           "override flag, and must return one <i>named</i> decoding or number-sense error plus a "
           "five-minute action.", S_CELL),
         P("The diagnostic here has never been treated as an inference problem. Existing systems resolve a "
           "child's level by looking it up in a table of thresholds, so they can only ever report the row "
           "they were handed. We treat it as <b>disambiguation under noise</b> and hand it to a reasoning "
           "model — constrained by a tool schema and a hard rule that it may cite only the page it was "
           "given, so it reasons freely but cannot invent content.", S_CELL),
         P("Threshold-based oral assessment is decades old, and we use it. The new part is not the "
           "measurement; it is asking a language model to explain <i>which</i> failure occurred and to "
           "answer only in the vocabulary of the textbook in front of her.")],
        [P("2", S_CELLB),
         P("<b>Refusal as a designed, measured output.</b> The system decides when a transcript is too "
           "unreliable to judge a child, declines, and asks the teacher to tap.", S_CELL),
         P("Assessment software that always answers is unsafe with young children, because a false "
           "“this child cannot read” follows them. Nobody in this space treats the recogniser as an "
           "unreliable <i>witness</i> rather than an instrument. We encode a stated asymmetry of cost, and "
           "refusal is logged, so we can report how often it happens instead of hiding it.", S_CELL),
         P("Confidence thresholds and human-in-the-loop review are standard practice. What is new is "
           "making <i>abstention</i> a first-class product behaviour with its own metric, in a setting "
           "where the cost of a wrong answer falls on a six-year-old.")],
        [P("3", S_CELLB),
         P("<b>An instrument that calibrates itself from the classroom it is in.</b> Item difficulty is "
           "estimated live, per cohort, so the ladder steps down fast and stops early.", S_CELL),
         P("Assessment ladders are almost always fixed ladders, chosen by the textbook's author rather than "
           "by the children in front of the teacher. Ours reorders and re-prices its own items from weekly "
           "classroom use, with no training set and no labels.", S_CELL),
         P("<b>Rasch item-response theory is prior art and we credit it.</b> The mathematics is from the "
           "1960s. The novelty is deployment: estimating item difficulty live, unsupervised, per session, "
           "on cheap hardware, to buy a five-minute budget. We are not claiming the model as ours.")],
    ], [8 * mm, 60 * mm, 88 * mm, 81 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("WHY FRONTIER AI MAKES THIS POSSIBLE ONLY NOW", S_TH)],
        [P("Frontier models only recently gained <b>tool-use</b>, which lets us force a diagnosis into a "
           "fixed, auditable shape instead of parsing prose. They only recently became <b>reliable on "
           "short, noisy, code-switched text</b>, which is exactly the input a six-year-old produces. And "
           "the <b>cost per call</b> fell below the value of five minutes of a teacher's time. A 2023 "
           "team could not have made this output safe to show a child; a rules-only team cannot disambiguate "
           "these cases at all. The window opened recently and it will not stay open to everyone.", S_CELL)],
    ], [237 * mm], head=True, zebra=False, pad=3))
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl([
        [P("On honesty", S_TH)],
        [P("Our pilot is cluster-randomised at classroom level with four classrooms. At that size the "
           "minimum detectable effect is roughly 0.40 SD, so we have <b>pre-committed to reporting effect "
           "sizes with confidence intervals</b>, and to leading with teacher-time and diagnostic-agreement "
           "results if the learning-gain result comes back null. A rubric that cannot detect a twenty-point "
           "difference at this sample size does not get to claim one. We would rather be shortlisted on a "
           "number we can defend than win on one we cannot.", S_CELL)],
    ], [237 * mm], head=True, zebra=False, pad=2.3))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Piece", S_TH), P("Origin - said plainly", S_TH), P("What we add on top", S_TH)],
        [P("Rasch / 1PL mathematics", S_DENSEB), P("Prior art, 1960s - credited.", S_DENSE),
         P("Live per-session deployment on cheap hardware.", S_DENSE)],
        [P("Indic ASR weights", S_DENSEB), P("AI4Bharat open weights.", S_DENSE),
         P("Noise-gated use inside a five-minute protocol.", S_DENSE)],
        [P("Error taxonomy", S_DENSEB), P("Ours; teacher blind-validated.", S_DENSE),
         P("The vocabulary Claude must answer in.", S_DENSE)],
        [P("Refusal as product behaviour", S_DENSEB), P("Ours.", S_DENSE),
         P("Measured abstention with its own metric.", S_DENSE)],
        [P("EGRA / EGMA ladders", S_DENSEB), P("Brief-provided toolkits.", S_DENSE),
         P("The item shapes and level definitions our screener follows.", S_DENSE)],
        [P("TaRL grouping", S_DENSEB), P("J-PAL evidence base.", S_DENSE),
         P("The pedagogy our bench map instruments, not replaces.", S_DENSE)],
        [P("Content-pack grounding", S_DENSEB), P("Ours, CI-enforced.", S_DENSE),
         P("The vocabulary and page bindings the model is allowed to cite.", S_DENSE)],
        [P("Bench-map grouping", S_DENSEB), P("Ours.", S_DENSE),
         P("Weekly recomputation from live levels, walkable in a real room.", S_DENSE)],
        [P("Five-minute ladder cap", S_DENSEB), P("Ours.", S_DENSE),
         P("An early-stop policy tuned to the classroom clock, not the textbook.", S_DENSE)],
    ], [50 * mm, 88 * mm, 99 * mm], pad=2.4))
    st.append(PageBreak())

    # ═══════════ 7 · INNOVATION 2/2 — COMPARISON ═══════════
    st.append(P("SECTION 4 · INNOVATION AND CREATIVITY (2 OF 2)", S_GHOST))
    st.append(_band("SECTION 4 · INNOVATION AND CREATIVITY (2 OF 2)",
                    "Where we sit against what already exists", 7))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Solution", S_TH), P("What it gives the teacher", S_TH), P("Per-child level?", S_TH),
         P("Names the misconception?", S_TH), P("Survives 60 dB?", S_TH), P("Offline?", S_TH),
         P("Points at a page?", S_TH), P("Time / child", S_TH)],
        [P("<b>Paper ASER oral tool</b><br/><font size=6.4 color='#5A6B73'>the status quo</font>", S_CELLB),
         P("A verified level, once a term, on paper, one-to-one."), P("Yes"), P("No"),
         P("N/A — human ear"), P("Yes"), P("No — teacher improvises"), P("10–15 min")],
        [P("<b>PadhAI</b> and similar content-delivery edtech", S_CELLB),
         P("Aligned content and exercises on a device."), P("No — content is grade-level"), P("No"),
         P("Yes"), P("Partial"), P("No"), P("n/a — not an assessment")],
        [P("<b>Generic LLM tutor / chatbot</b>", S_CELLB),
         P("Unlimited explanation in any language."), P("No — guessed from conversation"),
         P("Free-form, unverifiable"), P("No — cloud dependency"), P("No"),
         P("No — may invent content"), P("5–15 min, unpredictable")],
        [P("<b>Classic TaRL delivery</b><br/><font size=6.4 color='#5A6B73'>Pratham-style</font>", S_CELLB),
         P("The strongest evidence base in this space; correct pedagogy."), P("Yes, via a trained volunteer"),
         P("No"), P("Yes — human-led"), P("Yes"), P("No — needs facilitator training"),
         P("60+ min sessions, scheduled")],
        [P("<b>Samanantar</b>", S_CELLB),
         P("Level, named misconception, bench grouping, and the exact page to open next.", S_CELLB),
         P("<b>Yes — 5 min</b>", S_CELLB), P("<b>Yes — coded</b>", S_CELLB), P("<b>Yes — gate + tap</b>", S_CELLB),
         P("<b>Yes — on-device ASR</b>", S_CELLB), P("<b>Yes — page-precise</b>", S_CELLB), P("<b>3–5 min</b>", S_CELLB)],
    ], [38 * mm, 54 * mm, 22 * mm, 26 * mm, 25 * mm, 22 * mm, 32 * mm, 18 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    c1, c2 = 118 * mm, 119 * mm
    leftc = [
        P("Our defensible difference", S_SUBH),
        Spacer(1, 1 * mm),
        P("<b>We are the only option that is a measurement instrument <i>and</i> a next-action generator, "
          "on a phone, in a noisy room.</b> The two halves normally ship separately: assessment tools stop "
          "at the level, and content tools assume the level. The seam between them is exactly where a "
          "Grade 1–3 teacher is left alone — and that seam is the product.", S_CELL),
        P("<b>Moat 1 — the content-pack contract.</b> Every item carries a non-null NCERT page and a CBSE "
          "FLN skill, enforced in CI, so the build fails if a mapping is missing. A model that may cite only "
          "the page it was handed cannot drift off-curriculum. The pack is versioned per language, so a new "
          "state is a data change, not a rebuild.", S_CELL),
        P("<b>Moat 2 — the pilot data.</b> Stopwatch-measured teacher time, a fidelity log, override rates, "
          "and blinded re-test agreement are the artefacts that partners and SCERTs actually need. We "
          "intend to release the de-identified dataset alongside the pre-registration.", S_CELL),
    ]
    rightc = [
        P("What we are deliberately not claiming", S_SUBH),
        Spacer(1, 1 * mm),
        P("<b>Not a content platform.</b> We do not compete on having more content. We compete on knowing "
          "which two pages a specific child needs this week.", S_CELL),
        P("<b>Not a replacement for the teacher or for TaRL facilitation.</b> We are the measurement and "
          "targeting layer. Claiming to replace trained facilitators would be both false and, for this "
          "audience, disqualifying.", S_CELL),
        P("<b>Not eight languages.</b> Hindi and Marathi for the pilot, stated plainly. A pack version bump "
          "adds Telugu; that is not the same as shipping a claim we cannot demo.", S_CELL),
        P("<b>Not a learning-outcome claim yet.</b> We have a design and a pre-registered protocol. Until "
          "the pilot runs, the honest sentence is “we will report the effect size and its interval”, not a "
          "number.", S_CELL),
    ]
    row = Table([[leftc, rightc]], colWidths=[c1, c2])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (0, 0), 0),
                             ("RIGHTPADDING", (0, 0), (0, 0), 6 * mm),
                             ("LEFTPADDING", (1, 0), (1, 0), 0),
                             ("LINEBEFORE", (1, 0), (1, 0), 0.5, RULE)]))
    st.append(row)
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("SUBSTANTIALLY BETTER, SUMMARISED", S_TH)],
        [P("Paper ASER is accurate but takes 12 minutes and vanishes into a register. Content "
           "apps pitch themselves at the grade. Chatbots answer confidently and cannot be "
           "verified. Classic TaRL works but schedules itself out of ordinary schools. Only "
           "Samanantar returns a per-child level, a named misconception and a page-precise next "
           "action — in five minutes, offline, on the teacher's own phone, with every judgement "
           "overridable.", S_DENSE)],
        [P("How to read this slide", S_DENSEB),
         P("A yes that survives a noisy room and a dead network is worth more than three "
           "yeses that need perfect conditions. That is the bar every row above is judged "
           "against.", S_DENSE)],
    ], [237 * mm], head=True, zebra=False, pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Verifiable in 60 seconds", S_TH), P("How", S_TH)],
        [P("The product runs", S_DENSEB),
         P("python app.py - the full loop works with no API key and no network.", S_DENSE)],
        [P("The AI call is inspectable", S_DENSEB),
         P("ai.py LlmDiagnostic - one tool-use call, temperature 0, schema enforced.", S_DENSE)],
        [P("Content claims are checked", S_DENSEB),
         P("content_pack.json + CI: every item carries a real NCERT page or the build fails.", S_DENSE)],
    ], [58 * mm, 179 * mm], pad=1.9))
    st.append(PageBreak())

    # ═══════════ 8 · TECHNOLOGY AND DATA 1/2 ═══════════
    st.append(P("SECTION 5 · TECHNOLOGY AND DATA FEASIBILITY (1 OF 2)", S_GHOST))
    st.append(_band("SECTION 5 · TECHNOLOGY AND DATA FEASIBILITY (1 OF 2)",
                    "Stack, resources, and the role AI plays at every layer", 8))
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Layer", S_TH), P("Choice", S_TH), P("Role of AI here", S_TH), P("Why this choice", S_TH)],
        [P("Diagnosis", S_DENSEB), P("Claude (Anthropic) — forced tool call, temperature 0, structured output", S_DENSE),
         P("<b>Decides.</b> This is the core of the product.", S_DENSE),
         P("The task is disambiguating a child's language error from recogniser noise and shyness. That is "
           "reasoning over noisy evidence, not a threshold. The tool schema makes the answer auditable and "
           "temperature 0 makes it reproducible.")],
        [P("ASR", S_DENSEB), P("IndicWhisper / IndicConformer (AI4Bharat), ONNX Runtime, on device", S_DENSE),
         P("<b>Perceives.</b> Turns a child's voice into text.", S_DENSE),
         P("The only realistic way to transcribe a six-year-old offline in code-switched Hindi. On device "
           "because the room has no network and the voice must not leave the school.")],
        [P("AI reliability", S_DENSEB), P("Matra-weighted keyword spotting + noise-adjusted confidence gate", S_DENSE),
         P("<b>Bounds.</b> Decides when the AI may not answer.", S_DENSE),
         P("Pure, fast, inspectable — which is exactly what a safety boundary should be. The only way to "
           "catch a dropped vowel sign as an error rather than a near-match.")],
        [P("Instrument", S_DENSEB), P("1PL / Rasch item-response model, damped Newton + Gaussian prior", S_DENSE),
         P("<b>Calibrates.</b> Keeps the AI inside a 5-minute budget.", S_DENSE),
         P("Learns item difficulty from our own cohort with no training set, and stops the ladder early so "
           "a weak child is not ground down.")],
        [P("Client", S_DENSEB), P("Kotlin + Jetpack Compose on phone; Streamlit prototype for this proposal", S_DENSE),
         P("—", S_DENSE),
         P("Compose is the real target; Streamlit lets a judge run the logic immediately. Both share one "
           "pure core, so the prototype is the product, not a mock-up.")],
        [P("Storage & sync", S_DENSEB), P("Append-only encrypted event log (SQLCipher, AES-GCM); optional "
                                          "cursor-based upload-only sync", S_DENSE),
         P("—", S_DENSE),
         P("Every interaction is immutable, so a flat battery mid-assessment resumes cleanly and analytics "
           "replay. No merge logic is needed; the server is a mirror. Sync can be off with zero feature loss.")],
        [P("Content", S_DENSEB), P("Versioned JSON content pack, validated in CI", S_DENSE),
         P("<b>Grounds.</b> This is what keeps the model on-curriculum.", S_DENSE),
         P("Every item must carry a non-null NCERT page and a CBSE FLN skill or the build fails. A new "
           "language or state is a data change, not a rewrite.")],
    ], [22 * mm, 58 * mm, 42 * mm, 115 * mm], pad=1.7))
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl([
        [P("Data & resources", S_TH), P("Use in the solution", S_TH), P("Status", S_TH)],
        [P("<b>EGRA toolkit</b><br/><font size=6.4 color='#5A6B73'>Early Grade Reading Assessment</font>", S_DENSEB),
         P("<b>Our literacy spine.</b> Its ladder — letters, familiar words, non-familiar words, passages, "
           "comprehension — is the level definition our screener and ladder follow, and its oral-reading "
           "protocol is the shape of every item. We are not inventing an instrument; we are making an "
           "EGRA-conformant instrument run in five minutes.", S_DENSE), P('<font color=#0D9488><b>Brief-provided</b></font>', S_DENSE)],
        [P("<b>EGMA toolkit</b><br/><font size=6.4 color='#5A6B73'>Early Grade Maths Assessment</font>", S_DENSEB),
         P("<b>Our numeracy spine.</b> Number identification, place value and counting come before operations, "
           "and its subtasks structure our Concrete→Representational→Abstract diagnostic — which is how we "
           "avoid testing a skill the child has not built yet.", S_DENSE), P('<font color=#0D9488><b>Brief-provided</b></font>', S_DENSE)],
        [P("CBSE FLN toolkit & question banks", S_DENSEB),
         P("Each item maps to a CBSE foundational skill code; the banks seed our numeracy item pool.", S_DENSE),
         P('<font color=#0D9488><b>Brief-provided</b></font>', S_DENSE)],
        [P("ASER basic reading & maths assessment", S_DENSEB),
         P("The level ladder and the benchmark the pilot reports against, so our results are comparable to "
           "the national number.", S_DENSE), P("<b>Brief-provided</b>", S_DENSE)],
        [P("NCERT — Rimjhim 1–2, Math-Magic 1–2", S_DENSEB),
         P("The remediation content itself: every suggested activity names a real book and page the teacher "
           "already owns.", S_DENSE), P("Public, in use")],
        [P("J-PAL Teaching at the Right Level (2022)", S_DENSEB),
         P("The pedagogy, and the precedent for cluster-randomised design.", S_DENSE), P("Brief reading list")],
        [P("AI4Bharat IndicWhisper / IndicConformer", S_DENSEB),
         P("On-device speech recognition.", S_DENSE), P("Open weights")],
        [P("Classroom audio", S_DENSEB),
         P("Noise robustness at 40 / 50 / 60 dB. We report CER and WER separately, because for Devanagari "
           "WER alone overstates failure.", S_DENSE), P('<font color=#B45309><b>To collect in pilot</b></font>')],
        [P("Child assessments", S_DENSEB),
         P("Pre and post levels, minutes per child, fidelity and override rates.", S_DENSE),
         P('<font color=#B45309><b>To collect</b></font> — consent first, pseudonymous, '
      'de-identified release planned')],
    ], [46 * mm, 150 * mm, 41 * mm], pad=1.7))
    st.append(Spacer(1, 1.2 * mm))
    st.append(P("<b>Training data: none, and that is a deliberate feature.</b> We do not train on children's "
                "speech. We use off-the-shelf open ASR weights plus a content pack of public curriculum "
                "references. The only thing that <i>learns</i> from a child is one scalar per item — its "
                "Rasch difficulty — with no audio, no text and no identifiers. That removes the largest "
                "ethical and legal risk in this category, and it is what makes the conversation with a "
                "school tractable rather than a negotiation.", S_CELL))
    st.append(PageBreak())

    # ═══════════ 9 · TECHNOLOGY AND DATA 2/2 ═══════════
    st.append(P("SECTION 5 · TECHNOLOGY AND DATA FEASIBILITY (2 OF 2)", S_GHOST))
    st.append(_band("SECTION 5 · TECHNOLOGY AND DATA FEASIBILITY (2 OF 2)",
                    "Data flow, offline degradation, and how we will prove it works", 9))
    st.append(Spacer(1, 1.2 * mm))
    st.append(_flow_diagram(W - 2 * M, 36 * mm))
    st.append(Spacer(1, 1 * mm))
    st.append(tbl([
        [P("Stage", S_TH), P("What happens", S_TH), P("Where", S_TH), P("Role of AI", S_TH), P("How it degrades offline", S_TH)],
        [P("1 · Input", S_DENSEB), P("Roll ID, five ladder items, audio or tap.", S_DENSE), P("Phone", S_DENSE), P("—", S_DENSE), P("Unchanged — this is the offline path.", S_DENSE)],
        [P("2 · Transcribe", S_DENSEB), P("IndicConformer returns a Devanagari hypothesis and a confidence.", S_DENSE), P("Phone, on device", S_DENSEB), P("<b>AI perceives</b>", S_DENSE), P("Unchanged; degrades to tap-only if the model is absent.", S_DENSE)],
        [P("3 · Gate", S_DENSEB), P("The scorer asks: is this transcript trustworthy enough to judge a child?", S_DENSE), P("Phone", S_DENSE), P("<b>AI bounded</b>", S_DENSE), P("Unchanged — deterministic, identical with or without a network.", S_DENSE)],
        [P("4 · Diagnose", S_DENSEB), P("Claude returns level, misconception, NCERT page, Hindi hint, C-R-A stage, confidence.", S_DENSE), P("Server, else rules", S_DENSEB), P("<b>AI decides</b>", S_DENSE), P("A documented rule path takes over; the audit log records that the fallback ran.", S_DENSE)],
        [P("5 · Guardrail", S_DENSEB), P("The tool schema fixes the output shape; a hard rule forbids citing any page the model was not given; the teacher can override.", S_DENSE), P("Both", S_DENSE), P("<b>AI checked</b>", S_DENSE), P("The teacher override is the final guardrail and is always available.", S_DENSE)],
        [P("6 · Output", S_DENSEB), P("Bench map, a sticky note naming the page, a parent page, a certificate, an event-log entry.", S_DENSE), P("Phone", S_DENSE), P("—", S_DENSE), P("Unchanged — everything the teacher needs is already on the device.", S_DENSE)],
    ], [17 * mm, 74 * mm, 26 * mm, 24 * mm, 96 * mm], pad=2.4))
    st.append(Spacer(1, 1.2 * mm))
    c1, c2, c3 = 79 * mm, 79 * mm, 79 * mm
    b1 = [
        P("Feasibility and honesty about power", S_SUBH),
        Spacer(1, 1 * mm),
        P("<b>Cluster-randomised pilot.</b> The randomisation unit is the <b>classroom</b>, not the child — "
          "children in one room talk, so individual randomisation inside a room contaminates. Four "
          "classrooms across two schools, ~90–120 children, Grades 1–3. Control classrooms use paper only; "
          "no device enters the room.", S_DENSE),
        P("<b>Pre-registered before the post-test</b>, with endpoints, covariates, the analysis script and "
          "the power calculation frozen — so we cannot cherry-pick after seeing the data.", S_DENSE),
        P("<b>At ICC 0.15 with two classrooms per arm, the minimum detectable effect is about 0.40 SD.</b> "
          "So we report effect sizes with confidence intervals, and we will not claim a twenty-point "
          "difference at this sample size.", S_DENSE),
        P("<b>Biggest risk:</b> ASR accuracy on six-year-olds at 60 dB. The design already assumes it — "
          "the gate refuses to judge, tap input is a first-class path, and the override is logged. If the "
          "recogniser is weak the product still works; it leans harder on the teacher, which is where we "
          "wanted to be anyway.", S_DENSE),
    ]
    b2 = [
        P("What we will measure", S_SUBH),
        Spacer(1, 1 * mm),
        tbl([
            [P("Measure", S_TH), P("Target", S_TH)],
            [P("<b>Primary</b> — % of children gaining ≥1 ASER level", S_DENSE), P("Report d + 95% CI", S_DENSE)],
            [P("<b>Co-primary</b> — teacher minutes per child (stopwatch)", S_DENSE), P("≤5 min; paper 10–15", S_DENSE)],
            [P("<b>Fidelity</b> — TOST equivalence, app vs paper, ±0.2 SD", S_DENSE), P("Pass = no loss of information", S_DENSE)],
            [P("<b>Agreement</b> — quadratic-weighted κ vs blinded re-test, 20%", S_DENSE), P("κ ≥ 0.75", S_DENSE)],
            [P("<b>Fidelity</b> — override rate, activity completion, usage days", S_DENSE), P("Logged weekly, not recalled", S_DENSE)],
            [P("<b>Engineering</b> — simulator: 45 synthetic children, 60 dB, battery throttle", S_DENSE), P("≥90% stable ≤5 min, 0 crashes, resumes after kill", S_DENSE)],
        ], [44 * mm, 30 * mm], pad=2.0),
    ]
    b3 = [
        P("Build plan — three weeks, then the finale", S_SUBH),
        Spacer(1, 1 * mm),
        tbl([
            [P("Stage", S_TH), P("Dates", S_TH), P("Deliverable", S_TH)],
            [P("Ideate", S_DENSEB), P("to 27 Sept", S_DENSE), P("This proposal, registration, runnable prototype", S_DENSE)],
            [P("Build 1", S_DENSEB), P("10–18 Oct", S_DENSE), P("Content pack green in CI; ASR noise tests at 40/50/60 dB; ladder and hybrid input", S_DENSE)],
            [P("Build 2", S_DENSEB), P("19–27 Oct", S_DENSE), P("Error taxonomy to 20 codes with teacher blind-validation at 85% or higher; bench map; fidelity log", S_DENSE)],
            [P("Build 3", S_DENSEB), P("28 Oct–1 Nov", S_DENSE), P("OSF pre-registration; simulator report; 3-min demo video; low-end device end-to-end", S_DENSE)],
            [P("Finale", S_DENSEB), P("18 Nov", S_DENSE), P("Live demo on the low-end device, airplane mode, with a recorded fallback", S_DENSE)],
        ], [14 * mm, 16 * mm, 44 * mm], pad=2.0),
        Spacer(1, 1 * mm),
        P("<b>Why we should be shortlisted.</b> We are the only entry that closes the whole loop inside "
          "five minutes on a phone that already exists in the classroom, with a frontier model doing the "
          "one job only a frontier model can do — naming the child's actual misconception and the exact "
          "textbook page that fixes it — and a plan to prove it rather than a claim to believe.", S_DENSE),
    ]
    row = Table([[b1, b2, b3]], colWidths=[c1, c2, c3])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
                             ("LINEBEFORE", (1, 0), (-1, -1), 0.5, RULE)]))
    st.append(row)
    st.append(PageBreak())

    # ═══════════ TEAM PROFILES (excluded from the 7–10 count) ═══════════
    st.append(P("TEAM PROFILES  ·  excluded from the 7–10 slide count", S_KICKER))
    st.append(P(f"Team A2Z — {len(TEAM)} members", S_H))
    st.append(Spacer(1, 1.2 * mm))
    st.append(tbl(
        [[P("Member", S_TH), P("Domain", S_TH), P("Role in this solution", S_TH), P("Why the team needs this role", S_TH)]]
        + [[P(f"<b>{m['name']}</b><br/><font size=6.6 color='#5A6B73'>{m['role']}</font>", S_CELLB),
            P(m["domain"], S_CELL), P(m["owns"], S_CELL), P(m["why"], S_CELL)] for m in TEAM],
        [30 * mm, 34 * mm, 92 * mm, 81 * mm], pad=2.4))
    st.append(Spacer(1, 1.6 * mm))
    c1, c2 = 118 * mm, 119 * mm
    leftc = [
        P("Registration compliance", S_SUBH),
        Spacer(1, 1 * mm),
        P("· Every member registers <b>individually</b>, in an individual capacity, not on behalf of any "
          "school, company or NGO.", S_CELL),
        P("· All members are <b>18 or older</b> at registration and are <b>Indian citizens</b>, wherever "
          "they live or study.", S_CELL),
        P("· <b>2–4 members</b>; each member belongs to this team only. This deck lists "
          + ", ".join(m["name"] for m in TEAM) + ".", S_CELL),
        P("· No member is an employee of Central Square Foundation.", S_CELL),
        P("· This is a <b>single submission on Challenge 02 — Learning-Level Visibility</b>. Once a stage "
          "advances, the team continues with that same submission, <b>frozen from the Ideate stage</b> "
          "onward, as §3.4 and §3.5 require.", S_CELL),
    ]
    rightc = [
        P("Originality, IP and open source", S_SUBH),
        Spacer(1, 1 * mm),
        P("· The core idea and all implementation are our own, conceived and built inside the hackathon "
          "window. We use open-source libraries, public curriculum data and AI coding assistants, which "
          "the guidelines explicitly encourage.", S_CELL),
        P("· We retain full IP in the code and prototype.", S_CELL),
        P("· <b>We will open-source the repository.</b> The guidelines award an additional USD 250 in "
          "Claude credits for doing so, and a tool meant for a public-school teacher should be inspectable "
          "by anyone. MIT licence, with the content pack carrying a clear note that NCERT references are "
          "pointers, not reproductions.", S_CELL),
        P("· We accept that judges may read the code, ask us to explain the build live, and cross-check "
          "against public sources. That is the point of submitting source.", S_CELL),
    ]
    row = Table([[leftc, rightc]], colWidths=[c1, c2])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LEFTPADDING", (0, 0), (0, 0), 0),
                             ("RIGHTPADDING", (0, 0), (0, 0), 6 * mm),
                             ("LEFTPADDING", (1, 0), (1, 0), 0),
                             ("LINEBEFORE", (1, 0), (1, 0), 0.5, RULE)]))
    st.append(row)
    st.append(Spacer(1, 1.6 * mm))
    st.append(tbl([
        [P("Artefact", S_TH), P("What a judge finds there", S_TH)],
        [P("This PDF", S_DENSEB), P("9 content slides covering all five mandated sections.", S_DENSE)],
        [P("app.py", S_DENSEB), P("The runnable Streamlit loop: assess, diagnose, group, plan.", S_DENSE)],
        [P("ai.py", S_DENSEB), P("The single auditable Claude call, the ASR scorer, the Rasch model.", S_DENSE)],
        [P("content_pack.json", S_DENSEB), P("Every item with its NCERT page and CBSE FLN skill - CI-checked.", S_DENSE)],
        [P("tests/", S_DENSEB), P("74 tests: engine, level-map fold, plan assembly, end-to-end events.", S_DENSE)],
        [P("preregistration.md", S_DENSEB), P("Pilot design, power calculation and analysis plan, frozen early.", S_DENSE)],
        [P("ARCHITECTURE_OFFLINE.md", S_DENSEB), P("Why the loop works with no network, and how every tier degrades.", S_DENSE)],
        [P("ai_audit_report.md", S_DENSEB), P("Where the LLM is called, what it returns, how each result is audited.", S_DENSE)],
        [P("README.md", S_DENSEB), P("How to run the prototype in one command.", S_DENSE)],
        [P("demo_plan.md", S_DENSEB), P("The 3-minute demo script: what we show, in what order, and the fallback we rehearse.", S_DENSE)],
        [P("technical_doc.md", S_DENSEB), P("Architecture decisions, including ADR-4: audio discarded after on-device inference.", S_DENSE)],
        [P("INTERVIEW_KIT.md", S_DENSEB), P("The pre-registered teacher-interview guide used in Build Week 1.", S_DENSE)],
    ], [48 * mm, 189 * mm], pad=2.8))

    st.append(Spacer(1, 5 * mm))
    st.append(tbl([
        [P("Samanantar", S_TH),
         P("A per-child diagnostic + next-action instrument for the Grade 1–3 multigrade "
           "classroom — AI-centric, offline-first, and honest about what is measured and what "
           "is not.", S_DENSE),
         P("A2Z  ·  Challenge 02 · Learning-Level Visibility  ·  Team: "
           + ", ".join(m["name"] for m in TEAM)
           + "  ·  9 content slides, submitted as PDF", S_DENSE)],
    ], [26 * mm, 105 * mm, 106 * mm], head=False, zebra=False, pad=2.1))

    doc.build(st)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "A2Z_Samanantar_Ideate_Proposal.pdf")
    build(out)
    print(f"wrote {out}  ({os.path.getsize(out)/1024:.1f} KB)")
