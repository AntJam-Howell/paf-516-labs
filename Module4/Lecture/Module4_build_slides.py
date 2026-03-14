"""
Module 4 Lecture Slides PDF Builder
PAF 516 | Community Analytics
ASU Maroon & Gold theme, 16:9, no content bleed
"""

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
pt = 1.0
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 HRFlowable)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap

# ── Page geometry ─────────────────────────────────────────────────
W, H = 10*inch, 5.625*inch   # 16:9
MARGIN_L   = 0.45*inch
MARGIN_R   = 0.45*inch
MARGIN_TOP = 0.95*inch        # below header bar
MARGIN_BOT = 0.45*inch        # above footer
CONTENT_W  = W - MARGIN_L - MARGIN_R
CONTENT_H  = H - MARGIN_TOP - MARGIN_BOT - 0.3*inch  # footer space

# ── Colors ────────────────────────────────────────────────────────
MAROON  = colors.HexColor("#8C1D40")
GOLD    = colors.HexColor("#FFC627")
WHITE   = colors.white
LGRAY   = colors.HexColor("#F5F5F5")
DGRAY   = colors.HexColor("#444444")
MGRAY   = colors.HexColor("#888888")
HH_RED  = colors.HexColor("#D7191C")
LL_BLUE = colors.HexColor("#2C7BB6")
HL_ORG  = colors.HexColor("#FDAE61")
LH_LBL  = colors.HexColor("#ABD9E9")
NS_GRY  = colors.HexColor("#CCCCCC")

# ── Styles ────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=11,
                    textColor=DGRAY, leading=15, spaceAfter=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

title_s    = S("stitle", fontName="Helvetica-Bold", fontSize=28,
               textColor=MAROON, leading=34, alignment=TA_CENTER)
sub_s      = S("ssub",   fontName="Helvetica",      fontSize=16,
               textColor=DGRAY,  leading=22, alignment=TA_CENTER)
auth_s     = S("sauth",  fontName="Helvetica",      fontSize=12,
               textColor=MGRAY,  leading=16, alignment=TA_CENTER)
h1_s       = S("sh1",    fontName="Helvetica-Bold", fontSize=13,
               textColor=MAROON, leading=17, spaceAfter=4)
h2_s       = S("sh2",    fontName="Helvetica-Bold", fontSize=11,
               textColor=MAROON, leading=15, spaceAfter=2)
body_s     = S("sbody",  fontName="Helvetica",      fontSize=10,
               textColor=DGRAY,  leading=15, spaceAfter=2)
small_s    = S("ssmall", fontName="Helvetica",      fontSize=8.5,
               textColor=MGRAY,  leading=13)
bold_s     = S("sbold",  fontName="Helvetica-Bold", fontSize=10,
               textColor=DGRAY,  leading=15)
code_s     = S("scode",  fontName="Courier",        fontSize=8,
               textColor=DGRAY,  leading=12,
               backColor=colors.HexColor("#F0F0F0"),
               leftIndent=8, rightIndent=8)
callout_s  = S("scall",  fontName="Helvetica",      fontSize=9.5,
               textColor=DGRAY,  leading=14)
callout_h  = S("scallh", fontName="Helvetica-Bold", fontSize=9.5,
               textColor=MAROON, leading=14)
bullet_s   = S("sbullet",fontName="Helvetica",      fontSize=9.5,
               textColor=DGRAY,  leading=14,
               leftIndent=14, firstLineIndent=-10, spaceAfter=1)
num_s      = S("snum",   fontName="Helvetica",      fontSize=9.5,
               textColor=DGRAY,  leading=14,
               leftIndent=16, firstLineIndent=-12, spaceAfter=2)


# ── Canvas helpers ────────────────────────────────────────────────

def draw_header(c, title, subtitle=""):
    # Maroon header bar
    c.setFillColor(MAROON)
    c.rect(0, H - 0.75*inch, W, 0.75*inch, fill=1, stroke=0)
    # Gold rule below header
    c.setFillColor(GOLD)
    c.rect(0, H - 0.78*inch, W, 3*pt, fill=1, stroke=0)
    # Title text
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN_L, H - 0.5*inch, title)
    if subtitle:
        c.setFont("Helvetica", 10)
        c.setFillColor(GOLD)
        c.drawString(MARGIN_L, H - 0.66*inch, subtitle)

def draw_footer(c, slide_num, total):
    c.setFillColor(LGRAY)
    c.rect(0, 0, W, 0.32*inch, fill=1, stroke=0)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN_L, 0.10*inch, "PAF 516  |  Module 4  |  Spatial Autocorrelation & Hot Spot Analysis")
    c.drawRightString(W - MARGIN_R, 0.10*inch, f"{slide_num} / {total}")

def draw_title_slide(c):
    c.setFillColor(MAROON)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold accent bar top
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08*inch, W, 0.08*inch, fill=1, stroke=0)
    # Gold accent bar bottom
    c.rect(0, 0, W, 0.08*inch, fill=1, stroke=0)
    # Main title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W/2, H*0.62, "Spatial Autocorrelation")
    c.drawCentredString(W/2, H*0.52, "& Hot Spot Analysis")
    # Gold rule
    c.setFillColor(GOLD)
    c.rect(W*0.25, H*0.47, W*0.5, 2*pt, fill=1, stroke=0)
    # Subtitle
    c.setFillColor(colors.HexColor("#FFF8E7"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(W/2, H*0.40, "PAF 516  |  Community Analytics  |  Module 4")
    # Author
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W/2, H*0.28, "Anthony Howell, PhD  |  Arizona State University")
    # ASU badge
    c.setFillColor(GOLD)
    c.roundRect(W/2 - 1.2*inch, H*0.12, 2.4*inch, 0.38*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, H*0.145, "ARIZONA STATE UNIVERSITY")

def content_frame(c):
    """Returns (x, y, w, h) of the usable content rectangle."""
    x = MARGIN_L
    y = MARGIN_BOT + 0.32*inch
    w = CONTENT_W
    h = H - MARGIN_TOP - MARGIN_BOT - 0.32*inch
    return x, y, w, h

def draw_para(c, para, x, y, max_w, max_h=None):
    """Draw a Paragraph at (x,y). Returns y position after drawing."""
    w, h = para.wrap(max_w, max_h or 999*inch)
    if max_h and h > max_h:
        h = max_h
    para.drawOn(c, x, y - h)
    return y - h

def bullet(text, indent=0):
    prefix = "  " * indent
    return Paragraph(f"{prefix}• {text}", bullet_s)

def numbered(n, text):
    return Paragraph(f"{n}.  {text}", num_s)

def callout_box(c, x, y, w, h, title, lines):
    """Draw a filled callout box."""
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.setStrokeColor(MAROON)
    c.setLineWidth(1.5)
    c.roundRect(x, y, w, h, radius=4*pt, fill=1, stroke=1)
    # Left accent bar
    c.setFillColor(MAROON)
    c.rect(x, y, 3*pt, h, fill=1, stroke=0)
    # Title
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 8*pt, y + h - 14*pt, title)
    # Body lines
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    line_y = y + h - 26*pt
    for line in lines:
        if line_y < y + 4*pt:
            break
        c.drawString(x + 8*pt, line_y, line)
        line_y -= 12.5*pt

def two_col(c, slide_num, total, title, subtitle,
            left_items, right_items,
            left_w_frac=0.54):
    """Generic two-column layout slide."""
    draw_header(c, title, subtitle)
    draw_footer(c, slide_num, total)
    x, y, w, h = content_frame(c)
    lw = w * left_w_frac - 0.1*inch
    rw = w * (1 - left_w_frac) - 0.1*inch
    rx = x + w * left_w_frac + 0.1*inch

    cy_l = y + h
    cy_r = y + h

    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        elif isinstance(item, str) and item == "HR":
            cy_l -= 4
            c.setStrokeColor(GOLD)
            c.setLineWidth(1)
            c.line(x, cy_l, x + lw, cy_l)
            cy_l -= 4
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 2

    for item in right_items:
        if isinstance(item, float):
            cy_r -= item
        elif isinstance(item, str) and item == "HR":
            cy_r -= 4
            c.setStrokeColor(GOLD)
            c.setLineWidth(1)
            c.line(rx, cy_r, rx + rw, cy_r)
            cy_r -= 4
        else:
            ww, hh = item.wrap(rw, 999)
            item.drawOn(c, rx, cy_r - hh)
            cy_r -= hh + 2


# ── Slide content ─────────────────────────────────────────────────

def make_slides():
    OUTPUT = "/home/claude/Module4_Lecture_Slides.pdf"
    TOTAL  = 21
    c = canvas.Canvas(OUTPUT, pagesize=(W, H))
    c.setTitle("Module 4 – Spatial Autocorrelation & Hot Spot Analysis")
    c.setAuthor("Anthony Howell, PhD")
    c.setSubject("PAF 516 Community Analytics")

    # ── Slide 1: Title ────────────────────────────────────────────
    draw_title_slide(c)
    c.showPage()

    # ── Slide 2: The Core Question ────────────────────────────────
    draw_header(c, "The Core Question")
    draw_footer(c, 2, TOTAL)
    x, y, w, h = content_frame(c)
    cy = y + h

    items = [
        Paragraph("You mapped economic hardship across Maricopa County block groups.", bold_s),
        6.0,
        Paragraph("You probably noticed <b>clusters</b> — high-hardship areas surrounded by other high-hardship areas.", body_s),
        10.0,
    ]
    for item in items:
        if isinstance(item, float):
            cy -= item
        else:
            ww, hh = item.wrap(w * 0.9, 999)
            item.drawOn(c, x, cy - hh)
            cy -= hh + 3

    lw = w * 0.50 - 0.15*inch
    rw = w * 0.46
    rx = x + w * 0.54

    # Left column
    left_cy = cy
    left_items = [
        Paragraph("<b>The visual question:</b>", h2_s),
        bullet("Are those clusters <b>real</b>?"),
        bullet("Or could they have appeared by <b>chance</b>?"),
        bullet("Are they <b>statistically significant</b>?"),
    ]
    for item in left_items:
        ww, hh = item.wrap(lw, 999)
        item.drawOn(c, x, left_cy - hh)
        left_cy -= hh + 3

    # Callout right
    callout_box(c, rx, y + h * 0.1, rw, h * 0.55,
                "Module 4 gives you the tools",
                ["Measure, test, and map spatial clustering —",
                 "globally and locally — using spatial",
                 "autocorrelation statistics."])
    c.showPage()

    # ── Slide 3: Tobler's First Law ───────────────────────────────
    draw_header(c, "Tobler's First Law of Geography")
    draw_footer(c, 3, TOTAL)
    x, y, w, h = content_frame(c)

    # Quote box
    c.setFillColor(colors.HexColor("#FFF8E7"))
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.roundRect(x, y + h - 0.75*inch, w, 0.70*inch, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(W/2, y + h - 0.32*inch,
        '"Everything is related to everything else,')
    c.drawCentredString(W/2, y + h - 0.47*inch,
        'but near things are more related than distant things."')
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, y + h - 0.63*inch, "— Waldo Tobler (1970)")

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43

    left_items = [
        Paragraph("<b>What this means for social data:</b>", h2_s),
        bullet("Poverty in one tract predicts poverty in the next"),
        bullet("School quality, health, environmental burden — all exhibit spatial dependence"),
        bullet("This is <b>not</b> a statistical nuisance — it is a <b>substantive phenomenon</b>"),
        bullet("Spatial structure reveals how social processes operate <i>across space</i>"),
    ]
    cy_l = y + h - 0.82*inch
    for item in left_items:
        ww, hh = item.wrap(lw, 999)
        item.drawOn(c, x, cy_l - hh)
        cy_l -= hh + 4

    callout_box(c, x + lw + 0.2*inch, y + h * 0.05, rw, h * 0.47,
                "Standard statistics assume independence",
                ["OLS regression, t-tests, ANOVA all assume",
                 "observations are independent.",
                 "",
                 "Spatial data almost always violates this.",
                 "Ignoring it produces biased",
                 "standard errors."])
    c.showPage()

    # ── Slide 4: Three Spatial Patterns ──────────────────────────
    draw_header(c, "Three Spatial Patterns")
    draw_footer(c, 4, TOTAL)
    x, y, w, h = content_frame(c)

    cw = (w - 0.3*inch) / 3
    cols = [x, x + cw + 0.15*inch, x + 2*cw + 0.3*inch]
    box_colors = [HH_RED, NS_GRY, LH_LBL]
    box_titles = ["Clustered", "Random", "Dispersed"]
    box_subs   = ["Positive autocorrelation", "No autocorrelation", "Negative autocorrelation"]
    box_descs  = [
        ["Similar values near each other.", "High near high, low near low.", "Most common in social data."],
        ["No spatial pattern.", "The null hypothesis against", "which we test."],
        ["High next to low values.", "Checkerboard pattern.", "Rare in social data."],
    ]

    import random as _rnd
    _rnd.seed(7)
    for i in range(3):
        bx = cols[i]
        by = y + 0.05*inch
        bh = h - 0.05*inch
        # ── Outer card background ──
        c.setFillColor(colors.HexColor("#F7F7F7"))
        c.setStrokeColor(colors.HexColor("#DDDDDD"))
        c.setLineWidth(0.8)
        c.roundRect(bx, by, cw, bh, radius=5*pt, fill=1, stroke=1)
        # ── Colored swatch box (top 42% of card) ──
        swatch_h = bh * 0.42
        swatch_y = by + bh - swatch_h
        c.setFillColor(box_colors[i])
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.5)
        c.roundRect(bx + 0.06*inch, swatch_y - 0.03*inch,
                    cw - 0.12*inch, swatch_h, radius=4*pt, fill=1, stroke=0)
        # ── Dot patterns inside swatch ──
        dot_r = 5.5          # radius pts
        sx = bx + 0.06*inch  # swatch left
        sw = cw - 0.12*inch  # swatch width
        sy_bot = swatch_y - 0.03*inch
        sy_top = sy_bot + swatch_h
        dot_col = colors.HexColor("#FFFFFF") if i == 0 else (
                  colors.HexColor("#666666") if i == 1 else
                  colors.HexColor("#FFFFFF"))
        c.setFillColor(dot_col)
        if i == 0:  # Clustered — tight group top-left, loose elsewhere
            cluster_pts = [
                (0.22, 0.72),(0.30, 0.65),(0.25, 0.58),(0.35, 0.75),(0.38, 0.63),
                (0.28, 0.80),(0.42, 0.55),(0.20, 0.64),
                (0.70, 0.30),(0.78, 0.38),(0.72, 0.45),(0.80, 0.25),(0.65, 0.35),
                (0.60, 0.72),(0.50, 0.20),
            ]
            for (px, py) in cluster_pts:
                dx = sx + sw * px
                dy = sy_bot + swatch_h * py
                c.circle(dx, dy, dot_r, fill=1, stroke=0)
        elif i == 1:  # Random — uniform scatter
            for _ in range(18):
                dx = sx + sw * (0.05 + _rnd.random() * 0.90)
                dy = sy_bot + swatch_h * (0.08 + _rnd.random() * 0.84)
                c.circle(dx, dy, dot_r, fill=1, stroke=0)
        else:  # Dispersed — regular grid alternating
            grid_pts = [(c2, r2) for c2 in [0.15,0.35,0.55,0.75,0.90]
                                  for r2 in [0.20,0.45,0.70]]
            alt_col = [colors.HexColor("#FFFFFF"), colors.HexColor("#8C1D40")]
            for gi, (px, py) in enumerate(grid_pts):
                c.setFillColor(alt_col[gi % 2])
                dx = sx + sw * px
                dy = sy_bot + swatch_h * py
                c.circle(dx, dy, dot_r + 1, fill=1, stroke=0)
            c.setFillColor(dot_col)
        # ── Title ──
        c.setFillColor(MAROON)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(bx + cw/2, by + bh * 0.50, box_titles[i])
        # ── Subtitle ──
        c.setFillColor(MGRAY)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(bx + cw/2, by + bh * 0.42, box_subs[i])
        # ── Description ──
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 9)
        desc_y = by + bh * 0.33
        for line in box_descs[i]:
            c.drawCentredString(bx + cw/2, desc_y, line)
            desc_y -= 13

    # Policy callout spanning full width
    callout_box(c, x, y, w, 0.62*inch,
                "Policy implication",
                ["Spatially clustered hardship → place-based interventions (targeting neighborhoods) are efficient.",
                 "Spatially random hardship → people-based interventions may be more effective."])
    c.showPage()

    # ── Slide 5: Spatial Weights Matrix ──────────────────────────
    draw_header(c, "The Spatial Weights Matrix",
                "Defining 'neighbor' before measuring autocorrelation")
    draw_footer(c, 5, TOTAL)
    x, y, w, h = content_frame(c)

    # Formula box
    c.setFillColor(LGRAY)
    c.roundRect(x + w*0.25, y + h - 0.55*inch, w*0.5, 0.48*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, y + h - 0.22*inch, "w_ij = 1  if i and j are neighbors")
    c.drawCentredString(W/2, y + h - 0.38*inch, "w_ij = 0  otherwise")

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43

    left_items = [
        Paragraph("<b>Four neighbor definitions:</b>", h2_s),
        bullet("<b>Queen contiguity</b> — share any boundary point"),
        bullet("<b>Rook contiguity</b> — share an edge only"),
        bullet("<b>Distance-based</b> — within radius d"),
        bullet("<b>K-nearest neighbors</b> — k closest centroids"),
        10.0,
        Paragraph("<b>In R — spdep package:</b>", h2_s),
        Paragraph("nb &lt;- poly2nb(cbg_sf, queen = TRUE)", code_s),
        Paragraph("w  &lt;- nb2listw(nb, style = 'W')", code_s),
    ]
    cy_l = y + h - 0.62*inch
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, x + lw + 0.2*inch, y + h * 0.05, rw, h * 0.60,
                "Choice matters",
                ["The neighbor definition affects results.",
                 "Queen contiguity is the default",
                 "for polygon data.",
                 "",
                 "Always verify no observation has",
                 "zero neighbors — island polygons",
                 "cause errors in spdep."])
    c.showPage()

    # ── Slide 6: Row Standardization ─────────────────────────────
    draw_header(c, "Row Standardization & The Spatial Lag")
    draw_footer(c, 6, TOTAL)
    x, y, w, h = content_frame(c)
    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    cy = y + h

    # Intro text — LEFT COLUMN WIDTH ONLY
    intro = Paragraph("<b>Why standardize?</b>  Raw weights give more influence to observations with many neighbors.", body_s)
    ww, hh = intro.wrap(lw, 999)
    intro.drawOn(c, x, cy - hh)
    cy -= hh + 8

    # Formula — LEFT COLUMN WIDTH ONLY
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.05, cy - 0.50*inch, lw*0.90, 0.45*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + lw/2, cy - 0.23*inch, "w_ij* = w_ij / sum_j(w_ij)")
    cy -= 0.55*inch + 8

    left_items = [
        Paragraph("<b>Result: the spatial lag</b>", h2_s),
        Paragraph("The spatial lag of x at location i is the weighted average of its neighbors:", body_s),
        6.0,
        Paragraph("Wx_i = mean( x_j ) for all neighbors j", code_s),
        8.0,
        bullet("Scale-free and interpretable"),
        bullet("If a CBG's neighbors average 0.8 hardship index, its spatial lag = 0.8"),
        bullet("This is what gets plotted on the y-axis of the Moran scatterplot"),
    ]
    cy_l = cy
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    _cb6_h = h * 0.52
    callout_box(c, x + lw + 0.2*inch, y + h - 0.12*inch - _cb6_h, rw, _cb6_h,
                "style options in nb2listw()",
                ['style="W"  → row-standardized',
                 '              (most common)',
                 'style="B"  → binary (0/1)',
                 'style="C"  → globally standardized',
                 'style="S"  → variance-stabilizing',
                 "",
                 "Use W for Moran's I."])
    c.showPage()

    # ── Slide 7: Global Moran's I Formula ────────────────────────
    draw_header(c, "Global Moran's I",
                "A single statistic summarizing overall spatial autocorrelation")
    draw_footer(c, 7, TOTAL)
    x, y, w, h = content_frame(c)
    lw = w * 0.56 - 0.1*inch
    rw = w * 0.41
    cy = y + h

    # Formula — LEFT COLUMN WIDTH ONLY
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.65*inch, lw*0.96, 0.58*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + lw/2, cy - 0.25*inch,
        "I = (n/S0) × [Σ_i Σ_j w_ij·z_i·z_j] / Σ_i(z_i²)")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(x + lw/2, cy - 0.42*inch,
        "z_i = x_i – x̄  (deviation from mean),  S0 = sum of all weights")
    cy -= 0.72*inch

    left_items = [
        Paragraph("<b>Decomposing the numerator:</b>", h2_s),
        bullet("z<sub>i</sub>z<sub>j</sub> is the <b>cross-product</b> of deviations from the mean"),
        bullet("Weighted by w<sub>ij</sub> — only neighbors contribute"),
        bullet("Neighbors both above mean: z<sub>i</sub> &gt; 0, z<sub>j</sub> &gt; 0 → <b>positive</b>"),
        bullet("Neighbors straddle the mean → contributions <b>cancel out</b>"),
        8.0,
        Paragraph("<b>In R:</b>", h2_s),
        Paragraph("moran.test(x, w)          # analytical", code_s),
        Paragraph("moran.mc(x, w, nsim=999)  # permutation", code_s),
    ]
    cy_l = cy
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    _cb7_h = h * 0.62
    callout_box(c, x + lw + 0.2*inch, y + h - 0.12*inch - _cb7_h, rw, _cb7_h,
                "Interpretation",
                ["I > 0  →  clustering",
                 "          (similar values near each other)",
                 "",
                 "I ≈ –1/(n–1)  →  random",
                 "          (null expectation)",
                 "",
                 "I < 0  →  dispersed",
                 "          (opposite values adjacent)"])
    c.showPage()

    # ── Slide 8: Moran Scatterplot ────────────────────────────────
    draw_header(c, "The Moran Scatterplot",
                "Standardized value (z) × spatial lag (Wz) — slope = Moran's I")
    draw_footer(c, 8, TOTAL)
    x, y, w, h = content_frame(c)

    # Draw scatterplot manually
    sp_x = x + 0.05*inch
    sp_y = y + 0.15*inch
    sp_w = w * 0.46
    sp_h = h - 0.25*inch
    cx_sp = sp_x + sp_w / 2
    cy_sp = sp_y + sp_h / 2

    # Plot area
    c.setFillColor(LGRAY)
    c.rect(sp_x, sp_y, sp_w, sp_h, fill=1, stroke=0)

    # Axis lines
    c.setStrokeColor(DGRAY)
    c.setLineWidth(1)
    c.line(sp_x, cy_sp, sp_x + sp_w, cy_sp)       # x-axis
    c.line(cx_sp, sp_y, cx_sp, sp_y + sp_h)        # y-axis

    # Quadrant labels
    ql = [("HH", HH_RED,  cx_sp + sp_w*0.25, cy_sp + sp_h*0.30),
          ("LL", LL_BLUE, cx_sp - sp_w*0.35, cy_sp - sp_h*0.30),
          ("HL", HL_ORG,  cx_sp + sp_w*0.25, cy_sp - sp_h*0.30),
          ("LH", LH_LBL,  cx_sp - sp_w*0.35, cy_sp + sp_h*0.30)]
    for label, col, lx, ly in ql:
        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(lx, ly, label)

    # Scatter points
    import random
    random.seed(42)
    pts = [(0.55, 0.62), (0.30, 0.42), (0.72, 0.55), (0.20, 0.28), (0.80, 0.70),
           (-0.50,-0.55), (-0.30,-0.38), (-0.65,-0.48), (-0.20,-0.25), (-0.78,-0.65),
           (0.48,-0.32), (0.55,-0.45),
           (-0.40, 0.35), (-0.52, 0.28)]
    pt_cols = [HH_RED]*5 + [LL_BLUE]*5 + [HL_ORG]*2 + [LH_LBL]*2

    scale = min(sp_w, sp_h) * 0.44
    for (px, py), col in zip(pts, pt_cols):
        dot_x = cx_sp + px * scale
        dot_y = cy_sp + py * scale
        c.setFillColor(col)
        c.circle(dot_x, dot_y, 4, fill=1, stroke=0)

    # Regression line (slope ≈ 0.75 → Moran's I)
    c.setStrokeColor(MAROON)
    c.setLineWidth(2)
    c.line(sp_x + 4, sp_y + sp_h*0.08, sp_x + sp_w - 4, sp_y + sp_h*0.92)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(sp_x + sp_w * 0.65, cy_sp + sp_h * 0.12, "slope = I")

    # Axis labels
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(cx_sp, sp_y - 12, "z  (standardized hardship)")
    c.saveState()
    c.translate(sp_x - 12, cy_sp)
    c.rotate(90)
    c.drawCentredString(0, 0, "Wz  (spatial lag)")
    c.restoreState()

    # Right column legend + callout
    rx = sp_x + sp_w + 0.25*inch
    rw = w - sp_w - 0.3*inch
    cy_r = y + h

    legend_items = [
        Paragraph("<b>Four quadrants:</b>", h2_s),
        10.0,
    ]
    legend_dots = [("HH", HH_RED, "High, surrounded by high — hot spot"),
                   ("LL", LL_BLUE, "Low, surrounded by low — cold spot"),
                   ("HL", HL_ORG,  "High, surrounded by low — outlier"),
                   ("LH", LH_LBL,  "Low, surrounded by high — outlier")]
    for label, col, desc in legend_dots:
        legend_items.append(Paragraph(f"<b>{label}</b>  {desc}", body_s))
        legend_items.append(4.0)

    for item in legend_items:
        if isinstance(item, float):
            cy_r -= item
        else:
            ww, hh = item.wrap(rw, 999)
            item.drawOn(c, rx, cy_r - hh)
            cy_r -= hh + 3

    callout_box(c, rx, y + h*0.03, rw, h*0.30,
                "Key insight",
                ["The slope of the regression",
                 "line = Global Moran's I.",
                 "",
                 "Points in HH & LL quadrants",
                 "drive positive autocorrelation."])
    c.showPage()

    # ── Slide 9: Permutation Inference ───────────────────────────
    draw_header(c, "Statistical Inference — Permutation Test",
                "Do not assume normality. Use simulation.")
    draw_footer(c, 9, TOTAL)
    x, y, w, h = content_frame(c)

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    rx = x + lw + 0.2*inch

    left_items = [
        Paragraph("<b>The conditional randomization approach:</b>", h2_s),
        6.0,
        numbered(1, "Compute observed I<sub>obs</sub>"),
        numbered(2, "Randomly permute attribute values across locations"),
        numbered(3, "Compute I for each permutation (999 times) → reference distribution"),
        numbered(4, "<b>Pseudo p-value</b> = proportion of permuted I ≥ I<sub>obs</sub>"),
        12.0,
        Paragraph("<b>Why not use the analytical test?</b>", h2_s),
        bullet("Requires normality of residuals"),
        bullet("Sensitive to outliers in the data"),
        bullet("Permutation is assumption-free and preferred"),
    ]
    cy_l = y + h
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.45, rw, h*0.52,
                "In R",
                ["# Analytical",
                 "moran.test(x, w)",
                 "",
                 "# Permutation (preferred)",
                 "moran.mc(x, w,",
                 "         nsim = 999)"])

    callout_box(c, rx, y + h*0.05, rw, h*0.37,
                "How many simulations?",
                ["999   standard practice",
                 "9,999 publication quality",
                 "",
                 "Pseudo p-value cannot equal",
                 "exactly 0 — minimum is",
                 "1/(nsim + 1)."])
    c.showPage()

    # ── Slide 10: Limitation of Global Moran's I ─────────────────
    draw_header(c, "The Limitation of Global Moran's I",
                "It tells you clustering exists — not where")
    draw_footer(c, 10, TOTAL)
    x, y, w, h = content_frame(c)

    # Alert box
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.setStrokeColor(MAROON)
    c.setLineWidth(2)
    c.roundRect(x, y + h - 0.55*inch, w, 0.48*inch, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, y + h - 0.25*inch,
        "A study area can have both northern hot spots AND southern cold spots.")
    c.drawCentredString(W/2, y + h - 0.40*inch,
        "The global statistic averages over everything — clusters can cancel out.")

    lw = w * 0.56 - 0.1*inch
    rw = w * 0.41
    rx = x + lw + 0.2*inch

    left_items = [
        8.0,
        Paragraph("<b>The masking problem:</b>", h2_s),
        bullet("High-hardship cluster in South Phoenix → positive contribution to I"),
        bullet("Low-hardship cluster in North Scottsdale → also positive contribution"),
        bullet("A HL outlier in central Phoenix → <i>negative</i> contribution"),
        bullet("The global I averages all these — and could be <b>moderate or non-significant</b>"),
        12.0,
        Paragraph("<b>What you'd miss without LISA:</b>", h2_s),
        bullet("Exact location of each hot spot and cold spot"),
        bullet("Spatial outliers (pockets of hardship within affluent areas)"),
        bullet("Statistical significance of each specific cluster"),
    ]
    cy_l = y + h - 0.62*inch
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.05, rw, h*0.55,
                "Solution: LISA",
                ["Local Indicators of Spatial",
                 "Association decompose the",
                 "global statistic into a",
                 "contribution from each",
                 "individual location.",
                 "",
                 "Every block group gets its",
                 "own I_i and p-value."])
    c.showPage()

    # ── Slide 11: LISA Formula ────────────────────────────────────
    draw_header(c, "Local Moran's I (LISA)",
                "Anselin (1995) — one of the most cited papers in spatial analysis")
    draw_footer(c, 11, TOTAL)
    x, y, w, h = content_frame(c)
    lw = w * 0.56 - 0.1*inch
    rw = w * 0.41
    cy = y + h

    # Formula — LEFT COLUMN WIDTH ONLY
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.62*inch, lw*0.96, 0.55*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x + lw/2, cy - 0.24*inch,
        "I_i = z_i × Σ_j( w_ij × z_j )  =  z_i × (Wz)_i")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(x + lw/2, cy - 0.45*inch,
        "Product of location's z-score and the spatial lag of its neighbors")
    cy -= 0.70*inch

    left_items = [
        Paragraph("<b>Three outputs per location:</b>", h2_s),
        numbered(1, "I<sub>i</sub> value (+: same-type cluster, –: outlier)"),
        numbered(2, "z-score (standardized, for inference)"),
        numbered(3, "Pseudo p-value (via permutation, conditional on neighbors)"),
        12.0,
        Paragraph("<b>Classification uses:</b>", h2_s),
        bullet("Sign of z<sub>i</sub> — is this location above or below the mean?"),
        bullet("Sign of (Wz)<sub>i</sub> — are neighbors above or below mean?"),
        bullet("Statistical significance — is p < 0.05?"),
    ]
    cy_l = cy
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    _cb11_h = h * 0.60
    callout_box(c, x + lw + 0.2*inch, y + h - 0.12*inch - _cb11_h, rw, _cb11_h,
                "In R",
                ["lisa <- localmoran(x, w)",
                 "",
                 "Returns matrix with:",
                 "  Ii      local I value",
                 "  E.Ii    expected value",
                 "  Var.Ii  variance",
                 "  Z.Ii    z-score",
                 "  Pr(z)   p-value"])
    c.showPage()

    # ── Slide 12: LISA Classification Table ──────────────────────
    draw_header(c, "LISA Cluster Classification",
                "Classifying each location into one of four types + not significant")
    draw_footer(c, 12, TOTAL)
    x, y, w, h = content_frame(c)

    rows = [
        ["Category", "z_i", "(Wz)_i", "Interpretation", "Color"],
        ["HH  (Hot Spot)", "> 0", "> 0", "High-hardship area surrounded by high-hardship neighbors", "Red"],
        ["LL  (Cold Spot)", "< 0", "< 0", "Low-hardship area surrounded by low-hardship neighbors", "Blue"],
        ["HL  (Outlier)", "> 0", "< 0", "High-hardship island within a low-hardship area", "Orange"],
        ["LH  (Outlier)", "< 0", "> 0", "Low-hardship island within a high-hardship area", "Lt. Blue"],
        ["Not Significant", "—", "—", "No statistically significant local spatial pattern", "Gray"],
    ]
    col_w = [w*0.14, w*0.08, w*0.08, w*0.57, w*0.11]
    row_h = (h - 0.1*inch) / len(rows)

    row_fills = [MAROON, HH_RED, LL_BLUE, HL_ORG, LH_LBL, NS_GRY]
    row_text_col = [WHITE, WHITE, WHITE, DGRAY, DGRAY, DGRAY]

    for r, (row_data, fill, tcol) in enumerate(zip(rows, row_fills, row_text_col)):
        ry = y + h - (r+1)*row_h
        c.setFillColor(fill)
        c.rect(x, ry, w, row_h, fill=1, stroke=0)
        # Alternate rows slight shade
        if r > 0 and r % 2 == 0:
            c.setFillColor(colors.Color(0,0,0,0.05))
            c.rect(x, ry, w, row_h, fill=1, stroke=0)
        cx2 = x
        for ci, (cell, cw) in enumerate(zip(row_data, col_w)):
            c.setFillColor(tcol if r > 0 else WHITE)
            fs = 9 if ci == 3 else 10
            fn = "Helvetica-Bold" if r == 0 or ci == 0 else "Helvetica"
            c.setFont(fn, fs)
            c.drawString(cx2 + 5, ry + row_h * 0.28, cell)
            cx2 += cw

    # Divider lines
    c.setStrokeColor(WHITE)
    c.setLineWidth(0.5)
    cx2 = x
    for cw in col_w[:-1]:
        cx2 += cw
        c.line(cx2, y, cx2, y + h)
    c.showPage()

    # ── Slide 13: Multiple Testing ────────────────────────────────
    draw_header(c, "The Multiple Testing Problem",
                "Testing 500 block groups at p < 0.05 → expect 25 false positives")
    draw_footer(c, 13, TOTAL)
    x, y, w, h = content_frame(c)

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    rx = x + lw + 0.2*inch

    left_items = [
        Paragraph("<b>Three common solutions:</b>", h2_s),
        12.0,
        Paragraph("<b>1. Bonferroni correction</b>", h2_s),
        bullet("α* = α / n   (very conservative)"),
        bullet("For n=500, α* = 0.05/500 = 0.0001"),
        bullet("Appropriate when truly independent tests; overly strict for spatial data"),
        10.0,
        Paragraph("<b>2. False Discovery Rate (Benjamini-Hochberg)</b>", h2_s),
        bullet("Controls the expected proportion of false positives"),
        bullet("Less conservative than Bonferroni"),
        bullet("Preferred for publication-quality spatial analysis"),
        10.0,
        Paragraph("<b>3. Stricter p-value threshold</b>", h2_s),
        bullet("Use p &lt; 0.01 instead of p &lt; 0.05"),
        bullet("Pragmatic; widely used in applied policy work"),
    ]
    cy_l = y + h
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.05, rw, h*0.90,
                "Practical guidance",
                ["Policy reports:",
                 "  Use p < 0.05, flag clearly",
                 "  as 'exploratory.'",
                 "",
                 "Academic publication:",
                 "  Apply FDR correction.",
                 "",
                 "Bonferroni is too conservative",
                 "for spatial data — observations",
                 "are not independent by",
                 "definition (Tobler's Law)."])
    c.showPage()

    # ── Slide 14: Spatial Outliers ────────────────────────────────
    draw_header(c, "Spatial Outliers — A Closer Look",
                "Often the most policy-important findings on the LISA map")
    draw_footer(c, 14, TOTAL)
    x, y, w, h = content_frame(c)

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    rx = x + lw + 0.2*inch

    left_items = [
        Paragraph('<font color="#FDAE61">■</font>  <b>HL — High surrounded by low:</b>', h1_s),
        bullet("Pocket of concentrated disadvantage within a generally affluent area"),
        bullet("Could reflect: public housing development, displacement pressure, historical boundary"),
        bullet("Easy to miss in county-level analysis — MAUP erases it"),
        bullet("May need <i>more</i> targeted support than HH areas (isolation compounds hardship)"),
        12.0,
        Paragraph('<font color="#ABD9E9">■</font>  <b>LH — Low surrounded by high:</b>', h1_s),
        bullet("A resilient community embedded in a high-hardship context"),
        bullet("Study these for what is working — what policies, organizations, investments?"),
        bullet("Useful as 'natural experiments' for evaluating place-based policy"),
    ]
    cy_l = y + h
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.05, rw, h*0.90,
                "Limitation of place-based policy",
                ["A HL outlier is a high-hardship",
                 "area completely surrounded by",
                 "low-hardship neighbors.",
                 "",
                 "Place-based intervention will",
                 "reach it — but residents may not",
                 "benefit from surrounding",
                 "prosperity due to barriers:",
                 "transportation, discrimination,",
                 "social networks."])
    c.showPage()

    # ── Slide 15: Getis-Ord Gi* ───────────────────────────────────
    draw_header(c, "Getis-Ord G*_i — An Alternative Hot Spot Statistic")
    draw_footer(c, 15, TOTAL)
    x, y, w, h = content_frame(c)
    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    cy = y + h

    # Formula — LEFT COLUMN WIDTH ONLY
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.68*inch, lw*0.96, 0.62*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + lw/2, cy - 0.16*inch,
        "G*_i = [ Σ_j(w_ij·x_j) – x̄·Σ_j(w_ij) ]")
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(x + lw/2, cy - 0.30*inch,
        "────────────────────────────────────────────")
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + lw/2, cy - 0.47*inch,
        "s × √[ (n·Σw_ij² – (Σw_ij)²) / (n–1) ]")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(x + lw/2, cy - 0.62*inch,
        "Returns a z-score: positive = hot spot, negative = cold spot")
    cy -= 0.76*inch

    left_items = [
        Paragraph("<b>Returns a z-score for each location:</b>", h2_s),
        bullet("Positive z → <b>hot spot</b> (high values cluster here)"),
        bullet("Negative z → <b>cold spot</b> (low values cluster here)"),
        10.0,
        Paragraph("<b>Key differences from Local Moran's I:</b>", h2_s),
        bullet("Only identifies HH and LL — <b>does not detect outliers</b>"),
        bullet("Uses raw x values, not deviations from mean"),
        bullet("Includes focal location i in the sum (G*<sub>i</sub>)"),
        bullet("z-score is directly interpretable without quadrant classification"),
    ]
    cy_l = cy
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    _cb15_h = h * 0.62
    callout_box(c, x + lw + 0.2*inch, y + h - 0.12*inch - _cb15_h, rw, _cb15_h,
                "When to use which",
                ["LISA (Local Moran's I):",
                 "  Want clusters AND outliers.",
                 "  Most common in social science.",
                 "  Lab 4 uses this.",
                 "",
                 "Getis-Ord G*_i:",
                 "  Pure hot/cold spot ID.",
                 "  Common in crime analysis",
                 "  and epidemiology."])
    c.showPage()

    # ── Slide 16: Autocorrelation vs Heterogeneity ────────────────
    draw_header(c, "Spatial Autocorrelation vs. Spatial Heterogeneity",
                "Distinct phenomena — both matter, often confused")
    draw_footer(c, 16, TOTAL)
    x, y, w, h = content_frame(c)

    hw = (w - 0.2*inch) / 2
    rh = h - 0.55*inch

    # Left box — Autocorrelation
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.setStrokeColor(MAROON)
    c.setLineWidth(1.5)
    c.roundRect(x, y + 0.45*inch, hw, rh, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(MAROON)
    c.rect(x, y + 0.45*inch + rh - 0.38*inch, hw, 0.38*inch,
           fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + hw/2, y + 0.45*inch + rh - 0.18*inch,
                        "Spatial Autocorrelation")

    c.setFillColor(DGRAY)
    ac_items = [
        "Values in nearby areas are correlated.",
        "The attribute varies with location.",
        "",
        "Measured by: Moran's I, LISA, G*_i",
        "",
        "Same spatial process everywhere —",
        "nearby places just look similar.",
        "",
        "Example: Poverty rates are clustered.",
        "High-poverty tracts neighbor",
        "high-poverty tracts.",
    ]
    iy = y + 0.45*inch + rh - 0.52*inch
    for line in ac_items:
        c.setFont("Helvetica", 9)
        c.drawString(x + 10, iy, line)
        iy -= 13

    # Right box — Heterogeneity
    rx2 = x + hw + 0.2*inch
    c.setFillColor(colors.HexColor("#F0F5FF"))
    c.setStrokeColor(LL_BLUE)
    c.setLineWidth(1.5)
    c.roundRect(rx2, y + 0.45*inch, hw, rh, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(LL_BLUE)
    c.rect(rx2, y + 0.45*inch + rh - 0.38*inch, hw, 0.38*inch,
           fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(rx2 + hw/2, y + 0.45*inch + rh - 0.18*inch,
                        "Spatial Heterogeneity")

    c.setFillColor(DGRAY)
    het_items = [
        "The relationship between variables",
        "varies across space.",
        "",
        "Measured by: GWR (Geographically",
        "Weighted Regression)",
        "",
        "Different slopes in different regions.",
        "The process itself varies spatially.",
        "",
        "Example: Poverty-school quality link",
        "stronger in central Phoenix than",
        "in the suburbs.",
    ]
    iy = y + 0.45*inch + rh - 0.52*inch
    for line in het_items:
        c.setFont("Helvetica", 9)
        c.drawString(rx2 + 10, iy, line)
        iy -= 13

    # Bottom callout
    callout_box(c, x, y, w, 0.40*inch,
                "They can coexist",
                ["A variable can be spatially autocorrelated AND the process generating it can be spatially heterogeneous. Module 6 covers GWR."])
    c.showPage()

    # ── Slide 17: Edge Effects ────────────────────────────────────
    draw_header(c, "Edge Effects",
                "Border polygons have fewer neighbors — this can bias LISA statistics")
    draw_footer(c, 17, TOTAL)
    x, y, w, h = content_frame(c)

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    rx = x + lw + 0.2*inch

    left_items = [
        Paragraph("<b>The problem:</b>", h2_s),
        bullet("A CBG on the edge of Maricopa County borders Pinal or Yavapai County"),
        bullet("Its true neighbors extend beyond the study area boundary"),
        bullet("Those neighbors are excluded from the weights matrix"),
        bullet("Edge CBGs have <b>fewer neighbors</b> → higher variance → harder to reach significance"),
        bullet("LISA statistics for edge locations are <b>less reliable</b>"),
        12.0,
        Paragraph("<b>Why this matters for policy:</b>", h2_s),
        bullet("A HL outlier on the county border could be a data artifact, not a real cluster"),
        bullet("Understating significance at borders = missing real hardship concentrations"),
        bullet("Always inspect edge results with extra scrutiny"),
    ]
    cy_l = y + h
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.05, rw, h*0.90,
                "Practical solutions",
                ["1. Buffer zone",
                 "   Include neighboring county",
                 "   CBGs in the W matrix but",
                 "   exclude from the map.",
                 "",
                 "2. Acknowledge in text",
                 "   'Edge results are less',",
                 "   'reliable.' Standard practice.",
                 "",
                 "3. Distance-based W",
                 "   Less sensitive to edge",
                 "   effects than contiguity."])
    c.showPage()

    # ── Slide 18: Ecological Fallacy ──────────────────────────────
    draw_header(c, "The Ecological Fallacy",
                "LISA results describe areas — not individuals")
    draw_footer(c, 18, TOTAL)
    x, y, w, h = content_frame(c)

    # Warning banner
    c.setFillColor(colors.HexColor("#FFF0F0"))
    c.setStrokeColor(HH_RED)
    c.setLineWidth(2)
    c.roundRect(x, y + h - 0.58*inch, w, 0.52*inch, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(HH_RED)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W/2, y + h - 0.26*inch,
        "Do NOT infer individual-level characteristics from area-level statistics.")
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, y + h - 0.44*inch,
        "A HH cluster means the block group has high average hardship — not that every resident is in hardship.")

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43
    rx = x + lw + 0.2*inch

    left_items = [
        8.0,
        Paragraph("<b>What we measure:</b>", h2_s),
        bullet("Mean economic hardship in block group i is high"),
        bullet("Mean hardship in its neighboring CBGs is also high"),
        bullet("→ Classified as a HH hot spot"),
        12.0,
        Paragraph("<b>What we cannot infer:</b>", h2_s),
        bullet("That every person in that block group is experiencing hardship"),
        bullet("The block group may contain significant internal variation"),
        bullet("Higher-income residents may live alongside lower-income residents"),
        bullet("Area-level patterns reflect averages, not individual distributions"),
    ]
    cy_l = y + h - 0.65*inch
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, rx, y + h*0.05, rw, h*0.55,
                "Policy implication",
                ["A HH hot spot justifies",
                 "targeting the PLACE with",
                 "resources — infrastructure,",
                 "services, investment.",
                 "",
                 "The TYPE of intervention",
                 "requires individual-level",
                 "needs assessment, not just",
                 "spatial targeting."])
    c.showPage()

    # ── Slide 19: From Pattern to Policy ─────────────────────────
    draw_header(c, "From Pattern to Policy",
                "The chain of inference must be explicit")
    draw_footer(c, 19, TOTAL)
    x, y, w, h = content_frame(c)
    cy = y + h

    # Arrow chain diagram
    chain = ["Spatial\nPattern", "Statistical\nTest", "Cluster\nMap",
             "Causal\nMechanism", "Policy\nDesign"]
    under = ["Visual\nobservation", "Moran's I\npermutation", "LISA\nclassification",
             "Theory +\nHistory", "Place-based\ntargeting"]
    bw = (w - 0.4*inch) / (len(chain) + (len(chain)-1)*0.3)
    bh = 0.65*inch
    gap = bw * 0.3
    box_colors_ch = [LGRAY, LGRAY, colors.HexColor("#FFF3F6"),
                     colors.HexColor("#FFFBF0"), colors.HexColor("#F0FFF0")]

    bx = x + 0.1*inch
    box_y = cy - bh - 0.1*inch
    for i, (label, under_label) in enumerate(zip(chain, under)):
        c.setFillColor(box_colors_ch[i])
        c.setStrokeColor(MAROON)
        c.setLineWidth(1)
        c.roundRect(bx, box_y, bw, bh, radius=4*pt, fill=1, stroke=1)
        c.setFillColor(MAROON)
        c.setFont("Helvetica-Bold", 9)
        for li, line in enumerate(label.split("\n")):
            c.drawCentredString(bx + bw/2, box_y + bh - 18 - li*13, line)
        c.setFillColor(MGRAY)
        c.setFont("Helvetica", 7.5)
        for li, line in enumerate(under_label.split("\n")):
            c.drawCentredString(bx + bw/2, box_y + 18 - li*10, line)
        if i < len(chain) - 1:
            ax = bx + bw + 2
            ay = box_y + bh/2
            c.setFillColor(GOLD)
            c.setStrokeColor(GOLD)
            c.setLineWidth(2)
            c.line(ax, ay, ax + gap - 4, ay)
            c.setFillColor(GOLD)
            path = c.beginPath()
            path.moveTo(ax + gap - 4, ay + 4)
            path.lineTo(ax + gap - 4, ay - 4)
            path.lineTo(ax + gap + 4, ay)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
        bx += bw + gap

    cy = box_y - 0.15*inch

    lw = w * 0.54 - 0.1*inch
    rw = w * 0.43

    left_items = [
        Paragraph("<b>LISA tells you WHERE. It does not tell you WHY.</b>", h1_s),
        8.0,
        Paragraph("Explaining a HH hot spot in South Phoenix requires knowing:", body_s),
        bullet("Redlining and historical disinvestment (1930s–1960s HOLC maps)"),
        bullet("Industrial zoning decisions that concentrated environmental burden"),
        bullet("Highway construction that displaced communities and fractured neighborhoods"),
        bullet("School district boundaries that perpetuate resource inequality"),
    ]
    cy_l = cy
    for item in left_items:
        if isinstance(item, float):
            cy_l -= item
        else:
            ww, hh = item.wrap(lw, 999)
            item.drawOn(c, x, cy_l - hh)
            cy_l -= hh + 3

    callout_box(c, x + lw + 0.2*inch, cy - h*0.53, rw, h*0.48,
                "Use LISA for targeting, not diagnosis",
                ["HH clusters identify WHERE",
                 "to focus resources.",
                 "",
                 "The TYPE of resource depends",
                 "on understanding mechanisms",
                 "— requires qualitative",
                 "knowledge of the place."])
    c.showPage()

    # ── Slide 20: R Workflow ──────────────────────────────────────
    draw_header(c, "R Workflow — Complete Pipeline",
                "spdep package: poly2nb → nb2listw → moran.mc → localmoran")
    draw_footer(c, 20, TOTAL)
    x, y, w, h = content_frame(c)

    code_lines = [
        ("library(spdep); library(sf); library(tidyverse)", False),
        ("", False),
        ("# 1. Build spatial weights matrix", True),
        ("nb <- poly2nb(cbg_sf, queen = TRUE)         # queen contiguity", False),
        ("w  <- nb2listw(nb, style = 'W',              # row-standardized", False),
        ("              zero.policy = TRUE)            # allow islands", False),
        ("", False),
        ("# 2. Global Moran's I (permutation-based)", True),
        ("moran.mc(cbg_sf$hardship_index, w, nsim = 999)", False),
        ("", False),
        ("# 3. Local Moran's I", True),
        ("lisa <- localmoran(cbg_sf$hardship_index, w)", False),
        ("cbg_sf$lisa_I <- lisa[, 'Ii']", False),
        ("cbg_sf$lisa_p <- lisa[, 'Pr(z != E(Ii))']", False),
        ("", False),
        ("# 4. Classify HH / LL / HL / LH", True),
        ("z  <- scale(cbg_sf$hardship_index)[,1]", False),
        ("wz <- lag.listw(w, z)", False),
        ("cbg_sf$quad <- case_when(", False),
        ("  z > 0 & wz > 0 & cbg_sf$lisa_p < 0.05 ~ 'HH',", False),
        ("  z < 0 & wz < 0 & cbg_sf$lisa_p < 0.05 ~ 'LL',", False),
        ("  z > 0 & wz < 0 & cbg_sf$lisa_p < 0.05 ~ 'HL',", False),
        ("  z < 0 & wz > 0 & cbg_sf$lisa_p < 0.05 ~ 'LH',", False),
        ("  TRUE ~ 'Not Sig.')", False),
    ]

    c.setFillColor(colors.HexColor("#1E1E1E"))
    c.roundRect(x, y, w, h, radius=4*pt, fill=1, stroke=0)

    code_y = y + h - 14
    for line_data in code_lines:
        if isinstance(line_data, tuple):
            line, is_comment = line_data
        else:
            line, is_comment = line_data, False
        if is_comment:
            c.setFillColor(colors.HexColor("#6A9955"))
            c.setFont("Courier", 8.5)
        elif line.startswith("library") or line.startswith("cbg_sf$quad"):
            c.setFillColor(colors.HexColor("#DCDCAA"))
            c.setFont("Courier", 8.5)
        elif line == "":
            code_y -= 5
            continue
        else:
            c.setFillColor(colors.HexColor("#D4D4D4"))
            c.setFont("Courier", 8.5)
        c.drawString(x + 12, code_y, line)
        code_y -= 12

    c.showPage()

    # ── Slide 21: Lab 4 Preview + Key Takeaways ───────────────────
    draw_header(c, "Lab 4 Preview & Key Takeaways")
    draw_footer(c, 21, TOTAL)
    x, y, w, h = content_frame(c)

    hw = (w - 0.2*inch) / 2

    # Left: Lab 4 preview
    c.setFillColor(LGRAY)
    c.roundRect(x, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 10, y + h - 18, "Lab 4 — What You Will Build")
    c.setFillColor(GOLD)
    c.rect(x + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)

    lab_items = [
        "1.  Queen contiguity weights matrix",
        "     for Maricopa County CBGs",
        "2.  Global Moran's I permutation test",
        "     on your hardship index",
        "3.  LISA statistics for each CBG",
        "4.  LISA cluster map",
        "     (HH/LL/HL/LH/NS colors)",
        "5.  Written interpretation identifying",
        "     where hot spots occur and why",
        "",
        "Download: Lab4_Assignment.qmd",
        "from the course lab site",
        "Submit: .qmd + .html to Canvas",
    ]
    iy = y + h - 34
    for line in lab_items:
        c.setFillColor(DGRAY if not line.startswith("Download") else MAROON)
        c.setFont("Helvetica-Bold" if line.startswith(("Download","Submit")) else "Helvetica", 9)
        c.drawString(x + 12, iy, line)
        iy -= 13

    # Right: Key takeaways
    rx2 = x + hw + 0.2*inch
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.roundRect(rx2, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(rx2 + 10, y + h - 18, "Key Takeaways")
    c.setFillColor(GOLD)
    c.rect(rx2 + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)

    takeaways = [
        ("1.", "Tobler's First Law is the foundation."),
        ("", "  Near things are more related."),
        ("2.", "The weights matrix defines neighbor."),
        ("", "  Queen contiguity is the default."),
        ("3.", "Global Moran's I finds clustering"),
        ("", "  but not where — use LISA."),
        ("4.", "LISA gives every location its own"),
        ("", "  I_i, z-score, and p-value."),
        ("5.", "Multiple testing: use p < 0.01"),
        ("", "  or FDR correction."),
        ("6.", "Spatial outliers (HL/LH) reveal"),
        ("", "  policy-critical pockets."),
        ("7.", "LISA = pattern. Not explanation."),
        ("", "  Add theory and history."),
    ]
    iy = y + h - 34
    for num, text in takeaways:
        c.setFillColor(MAROON if num else DGRAY)
        c.setFont("Helvetica-Bold" if num else "Helvetica", 9)
        c.drawString(rx2 + 12, iy, num + text)
        iy -= 12.5

    c.showPage()
    c.save()
    print(f"Done → {OUTPUT}  ({TOTAL} slides)")

make_slides()
