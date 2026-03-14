"""
Module 6 Lecture Slides PDF Builder
PAF 516 | Community Analytics
Spatio-Temporal Analysis — LISA Trajectories & Space-Time Moran's I
ASU Maroon & Gold theme, 16:9, no content bleed
"""

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

pt = 1.0

# ── Page geometry ─────────────────────────────────────────────────
W, H       = 10*inch, 5.625*inch
MARGIN_L   = 0.45*inch
MARGIN_R   = 0.45*inch
MARGIN_TOP = 0.95*inch
MARGIN_BOT = 0.45*inch
CW         = W - MARGIN_L - MARGIN_R

# ── Colors ────────────────────────────────────────────────────────
MAROON  = colors.HexColor("#8C1D40")
GOLD    = colors.HexColor("#FFC627")
WHITE   = colors.white
LGRAY   = colors.HexColor("#F5F5F5")
DGRAY   = colors.HexColor("#444444")
MGRAY   = colors.HexColor("#888888")
BLUE    = colors.HexColor("#2C7BB6")
RED     = colors.HexColor("#D7191C")
ORANGE  = colors.HexColor("#FDAE61")
LBLUE   = colors.HexColor("#ABD9E9")
YELLOW  = colors.HexColor("#FEE08B")
PURPLE  = colors.HexColor("#9E5BB4")
DBLUE   = colors.HexColor("#2166AC")
NSIG    = colors.HexColor("#CCCCCC")

# ── Paragraph styles ──────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, textColor=DGRAY,
             leading=14, spaceAfter=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

h1_s     = S("h1",   fontName="Helvetica-Bold", fontSize=13,
              textColor=MAROON, leading=17, spaceAfter=4)
h2_s     = S("h2",   fontName="Helvetica-Bold", fontSize=10,
              textColor=MAROON, leading=14, spaceAfter=2)
body_s   = S("body", fontSize=10, textColor=DGRAY, leading=14, spaceAfter=2)
small_s  = S("sm",   fontSize=8.5, textColor=MGRAY, leading=12)
bullet_s = S("bul",  fontSize=9.5, textColor=DGRAY, leading=13,
              leftIndent=14, firstLineIndent=-10, spaceAfter=1)
num_s    = S("num",  fontSize=9.5, textColor=DGRAY, leading=13,
              leftIndent=16, firstLineIndent=-12, spaceAfter=2)
code_s   = S("code", fontName="Courier", fontSize=7.8, textColor=DGRAY,
              leading=11, backColor=colors.HexColor("#F0F0F0"),
              leftIndent=6, rightIndent=6)

def B(text):
    return Paragraph(f"• {text}", bullet_s)

def N(n, text):
    return Paragraph(f"{n}.  {text}", num_s)


# ── Canvas helpers ────────────────────────────────────────────────

def header(c, title, sub=""):
    c.setFillColor(MAROON)
    c.rect(0, H - 0.75*inch, W, 0.75*inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.78*inch, W, 3*pt, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGIN_L, H - 0.50*inch, title)
    if sub:
        c.setFont("Helvetica", 10)
        c.setFillColor(GOLD)
        c.drawString(MARGIN_L, H - 0.66*inch, sub)

def footer(c, n, total):
    c.setFillColor(LGRAY)
    c.rect(0, 0, W, 0.32*inch, fill=1, stroke=0)
    c.setFillColor(MGRAY)
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN_L, 0.10*inch,
                 "PAF 516  |  Module 6  |  Spatio-Temporal Analysis")
    c.drawRightString(W - MARGIN_R, 0.10*inch, f"{n} / {total}")

def title_slide(c):
    c.setFillColor(MAROON)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08*inch, W, 0.08*inch, fill=1, stroke=0)
    c.rect(0, 0, W, 0.08*inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W/2, H*0.62, "Spatio-Temporal Analysis")
    c.setFillColor(GOLD)
    c.rect(W*0.25, H*0.54, W*0.5, 2*pt, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#FFF8E7"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(W/2, H*0.47,
        "LISA Trajectories  ·  Space-Time Moran's I  ·  Three-Point Trends")
    c.drawCentredString(W/2, H*0.39,
        "From 'What Changed' to 'How Change Spreads'")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W/2, H*0.28,
        "PAF 516  |  Community Analytics  |  Module 6")
    c.setFont("Helvetica", 11)
    c.drawCentredString(W/2, H*0.21,
        "Anthony Howell, PhD  |  Arizona State University")
    c.setFillColor(GOLD)
    c.roundRect(W/2 - 1.2*inch, H*0.10, 2.4*inch, 0.36*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, H*0.127, "ARIZONA STATE UNIVERSITY")

def cf():
    x = MARGIN_L
    y = MARGIN_BOT + 0.32*inch
    w = CW
    h = H - MARGIN_TOP - MARGIN_BOT - 0.32*inch
    return x, y, w, h

def draw_items(c, items, x, cy, w):
    for item in items:
        if isinstance(item, (int, float)):
            cy -= item
        else:
            pw, ph = item.wrap(w, 999)
            item.drawOn(c, x, cy - ph)
            cy -= ph + 3
    return cy

def callout(c, x, y, w, h, title, lines):
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.setStrokeColor(MAROON)
    c.setLineWidth(1.5)
    c.roundRect(x, y, w, h, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(MAROON)
    c.rect(x, y, 3*pt, h, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 8*pt, y + h - 14*pt, title)
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 8.5)
    ly = y + h - 27*pt
    for line in lines:
        if ly < y + 5*pt:
            break
        c.drawString(x + 8*pt, ly, line)
        ly -= 12.5*pt

def code_block(c, x, y, w, h, lines):
    c.setFillColor(colors.HexColor("#1E1E1E"))
    c.roundRect(x, y, w, h, radius=4*pt, fill=1, stroke=0)
    cy = y + h - 13
    for line, is_comment in lines:
        if not line:
            cy -= 5
            continue
        col = colors.HexColor("#6A9955") if is_comment else colors.HexColor("#D4D4D4")
        c.setFillColor(col)
        c.setFont("Courier", 7.8)
        c.drawString(x + 10, cy, line)
        cy -= 11


# ── Trajectory color map ──────────────────────────────────────────
TRAJ_COLORS = {
    "Persistent HH": RED,
    "Emerging HH":   ORANGE,
    "Dissolving HH": YELLOW,
    "Persistent LL": BLUE,
    "Emerging LL":   LBLUE,
    "HL Outlier":    PURPLE,
    "Stable NS":     NSIG,
}


# ══════════════════════════════════════════════════════════════════
# SLIDES
# ══════════════════════════════════════════════════════════════════

def make_slides():
    OUTPUT = "/home/claude/Module6_Lecture_Slides.pdf"
    TOTAL  = 16

    c = canvas.Canvas(OUTPUT, pagesize=(W, H))
    c.setTitle("Module 6 – Spatio-Temporal Analysis")
    c.setAuthor("Anthony Howell, PhD")
    c.setSubject("PAF 516 Community Analytics")

    # ── Slide 1: Title ────────────────────────────────────────────
    title_slide(c)
    c.showPage()

    # ── Slide 2: From Change to Structure ────────────────────────
    header(c, "From 'What Changed' to 'How Change Spreads'",
           "Module 5 answered what — Module 6 asks whether change is spatially structured")
    footer(c, 2, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    # Alert box
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.setStrokeColor(MAROON)
    c.setLineWidth(2)
    c.roundRect(x, cy - 0.56*inch, w, 0.50*inch, radius=4*pt, fill=1, stroke=1)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, cy - 0.24*inch,
        "If change is spatially autocorrelated, decline and recovery are spreading processes.")
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(W/2, cy - 0.42*inch,
        "Intervening at the boundary of an expanding hot spot — before it consolidates — is more cost-effective.")
    cy -= 0.66*inch

    # Two boxes
    hw = (w - 0.2*inch) / 2
    for i, (title_b, col, items_list) in enumerate([
        ("Module 5 showed", BLUE, [
            "Which tracts improved (negative Δ)",
            "Which tracts worsened (positive Δ)",
            "Whether change exceeded MOE",
            "Where Lab 4 hot spots stand today",
        ]),
        ("Module 6 asks", MAROON, [
            "Are hot spots persistent or dissolving?",
            "Is change itself spatially clustered?",
            "Does decline/recovery spread spatially?",
            "What is the sustained trend (3 points)?",
        ]),
    ]):
        bx = x if i == 0 else x + hw + 0.2*inch
        bh = cy - y - 0.10*inch
        c.setFillColor(col)
        c.roundRect(bx, y + 0.08*inch, hw, bh, radius=4*pt, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(bx + hw/2, y + 0.08*inch + bh - 0.20*inch, title_b)
        c.setFont("Helvetica", 9.5)
        for j, item in enumerate(items_list):
            c.drawCentredString(bx + hw/2,
                                y + 0.08*inch + bh - 0.38*inch - j*0.13*inch,
                                f"• {item}")
    c.showPage()

    # ── Slide 3: LISA Trajectory Analysis ────────────────────────
    header(c, "LISA Trajectory Analysis",
           "Cross-tabulating cluster membership at two time points")
    footer(c, 3, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>The idea:</b> Run LISA at 2013 and again at 2019.", h2_s),
        Paragraph("Each tract belongs to one of 5 categories in each year.", body_s),
        Paragraph("Cross-tabulating gives a <b>5×5 transition matrix</b>.", body_s),
        12.0,
        Paragraph("<b>Policy-relevant trajectory categories:</b>", h2_s),
        8.0,
    ]
    cy = draw_items(c, left, x, cy, lw)

    traj_data = [
        ("Persistent HH", "HH→HH", RED,    "Deep structural hardship — sustained investment needed"),
        ("Emerging HH",   "→HH",   ORANGE, "Deteriorating — early intervention window open"),
        ("Dissolving HH", "HH→",   YELLOW, "Recovering — study what worked here"),
        ("Persistent LL", "LL→LL", BLUE,   "Stably low hardship — low equity urgency"),
        ("Emerging LL",   "→LL",   LBLUE,  "Improving — watch for displacement"),
        ("HL Outlier",    "HL",    PURPLE, "Isolated pocket — barriers to spillover"),
        ("Stable NS",     "NS→NS", NSIG,   "No significant clustering in either period"),
    ]
    row_h2 = (cy - y - 0.05*inch) / len(traj_data)
    for i, (name, trans, col, meaning) in enumerate(traj_data):
        ry = cy - (i + 1) * row_h2
        c.setFillColor(col)
        c.rect(x, ry, lw * 0.04, row_h2 * 0.85, fill=1, stroke=0)
        c.setFillColor(DGRAY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + lw * 0.07, ry + row_h2 * 0.52, name)
        c.setFillColor(MGRAY)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(x + lw * 0.07, ry + row_h2 * 0.18, trans)
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + lw * 0.35, ry + row_h2 * 0.38, meaning)

    callout(c, rx, y + h - 0.12*inch - h*0.68, rw, h*0.68,
            "In R",
            ["change_df %>% mutate(",
             " trajectory =",
             " case_when(",
             "  l13=='HH'&",
             "  l19=='HH'~",
             "  'Persistent HH',",
             "  l13!='HH'&",
             "  l19=='HH'~",
             "  'Emerging HH',",
             "  l13=='HH'&",
             "  l19!='HH'~",
             "  'Dissolving HH',",
             "  ...))"])
    c.showPage()

    # ── Slide 4: Transition Matrix ────────────────────────────────
    header(c, "Reading the Transition Matrix",
           "What the off-diagonal cells reveal about neighborhood change dynamics")
    footer(c, 4, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>The diagonal: persistence</b>", h2_s),
        B("HH→HH, LL→LL: cluster membership unchanged across the decade"),
        B("High diagonal proportion → structural conditions dominate → slow change"),
        12.0,
        Paragraph("<b>Off-diagonal transitions tell different stories:</b>", h2_s),
        B("<b>HH→NS</b>: hot spot dissolved — recovery reached this area"),
        B("<b>NS→HH</b>: new hot spot formed — deterioration spreading"),
        B("<b>HH→LL</b>: full reversal — extremely rare; possible displacement signal"),
        B("<b>LL→HH</b>: rapid decline — look for local economic shock"),
        12.0,
        Paragraph("<b>Key proportions to report:</b>", h2_s),
        B("What % of 2013 HH clusters are still HH in 2019? (persistence rate)"),
        B("What % of 2019 HH clusters were not HH in 2013? (emergence rate)"),
        B("What % of 2013 HH clusters dissolved? (recovery rate)"),
        12.0,
        Paragraph("Each proportion has direct implications for intervention design.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.88, rw, h*0.88,
            "Interpretation guide",
            ["High persistence (>70%",
             "on diagonal):",
             "  Structural problem;",
             "  long-term multi-sector",
             "  investment required.",
             "",
             "High dissolution (<40%",
             "HH→HH):",
             "  Recovery is possible;",
             "  identify what worked.",
             "",
             "High emergence (>30%",
             "new HH in 2019):",
             "  Spreading decline;",
             "  early warning signal;",
             "  tipping point proximity."])
    c.showPage()

    # ── Slide 5: Space-Time Moran's I ─────────────────────────────
    header(c, "Space-Time Moran's I",
           "Testing whether change itself is spatially autocorrelated")
    footer(c, 5, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    # Formula
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.52*inch, lw*0.96, 0.46*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + lw/2, cy - 0.18*inch,
                        "I_change = Moran's I applied to Δ_i (the change score)")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(x + lw/2, cy - 0.36*inch,
                        "Same weights matrix W from Lab 4 — queen contiguity, row-standardized")
    cy -= 0.60*inch

    left = [
        Paragraph("<b>The question:</b>", h2_s),
        B("Do tracts that improved cluster together?"),
        B("Do tracts that worsened cluster together?"),
        B("Or is change randomly distributed across space?"),
        12.0,
        Paragraph("<b>The test:</b>", h2_s),
        8.0,
        Paragraph("moran.mc(change_df$hardship_change, w, nsim=999)", code_s),
        12.0,
        Paragraph("<b>Interpreting the result:</b>", h2_s),
        B("<b>Significant positive I</b>: Change clusters spatially — "
          "improvement and decline are spreading processes"),
        B("<b>Non-significant I</b>: Change is spatially random — "
          "neighborhood-specific shocks dominate, not spatial diffusion"),
        12.0,
        Paragraph("<b>Policy implication of significant I_change:</b>", h2_s),
        B("Intervene at the boundary of worsening clusters before they expand"),
        B("Recovery is spatially contagious — anchor investments may spread outward"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.70, rw, h*0.70,
            "Mechanism: spatial diffusion",
            ["Galster & Tatian (2009):",
             "Housing value trajectories",
             "in declining neighborhoods",
             "are spatially autocorrelated.",
             "",
             "Disinvestment signals in",
             "one tract reduce neighboring",
             "tract property values.",
             "",
             "This is the diffusion",
             "mechanism that I_change",
             "detects.",
             "",
             "If I_change is significant,",
             "the decline is contagious —",
             "not just idiosyncratic."])
    c.showPage()

    # ── Slide 6: LISA on Change Scores ───────────────────────────
    header(c, "LISA on Change Scores",
           "Where is change itself spatially clustered?")
    footer(c, 6, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>One step further:</b> run LISA on the change score itself.", h2_s),
        Paragraph("Identifies not just where change occurred, but where change "
                  "is <i>spatially clustering</i>.", body_s),
        8.0,
        Paragraph("lisa_change <- localmoran(change_df$hardship_change, w)", code_s),
        12.0,
        Paragraph("<b>Four spatial change types:</b>", h2_s),
        B("<b>HH of change</b>: Tract worsened AND surrounded by worsening neighbors "
          "— a <b>spreading decline front</b>"),
        B("<b>LL of change</b>: Tract improved AND surrounded by improving neighbors "
          "— a <b>recovery cluster</b>"),
        B("<b>HL of change</b>: Worsened surrounded by improving — isolated deterioration"),
        B("<b>LH of change</b>: Improved surrounded by worsening — isolated recovery"),
        12.0,
        Paragraph("<b>Overlay on change map:</b>", h2_s),
        B("Maroon outline = areas of clustered worsening"),
        B("Blue outline = areas of clustered improvement"),
        B("Identifies the expanding frontier — not just current hot spots"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.72, rw, h*0.72,
            "The spreading decline front",
            ["HH clusters of change =",
             "areas where worsening",
             "is spatially contagious.",
             "",
             "These areas haven't",
             "become a persistent HH",
             "hot spot yet — but they",
             "are heading there.",
             "",
             "This is the highest-value",
             "early intervention target:",
             "the cluster is forming,",
             "not yet entrenched.",
             "",
             "Emerging HH +",
             "HH of change =",
             "double signal."])
    c.showPage()

    # ── Slide 7: Three-Point Trend ────────────────────────────────
    header(c, "Three-Point Trend Analysis",
           "Adding a middle observation to distinguish trend from noise")
    footer(c, 7, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>The problem with two-point change scores:</b>", h2_s),
        B("A tract could show apparent improvement from 2013 to 2019"),
        B("Because of a one-time shock at either endpoint"),
        B("Not because of sustained structural change"),
        12.0,
        Paragraph("<b>Solution: add a middle time point</b>", h2_s),
        B("year = 2016 (2012–2016 ACS, also 2010 TIGER/Line boundaries)"),
        B("Three observations: 2013, 2016, 2019 — all GEOIDs match"),
        12.0,
        Paragraph("<b>Monotonicity classification:</b>", h2_s),
        B("<b>Consistently improving</b>: h_2013 > h_2016 > h_2019"),
        B("<b>Consistently worsening</b>: h_2013 < h_2016 < h_2019"),
        B("<b>V-shaped</b>: worsened mid-decade, recovered by 2019"),
        B("<b>Inverted-V</b>: peaked mid-decade, improved by 2019"),
        B("<b>Flat</b>: no clear monotone pattern"),
        12.0,
        Paragraph("An OLS <b>trend slope</b> across the three points provides a "
                  "continuous measure. Positive = increasing hardship per year; "
                  "negative = decreasing.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.78, rw, h*0.78,
            "Why 2016 works",
            ["year = 2016 pulls the",
             "2012–2016 ACS 5-year.",
             "",
             "ALSO uses 2010 TIGER",
             "boundaries — GEOIDs",
             "match all three points.",
             "",
             "OLS slope in R:",
             "slopes <- all_years %>%",
             "  group_by(GEOID) %>%",
             "  summarise(",
             "    slope = coef(",
             "      lm(index~year)",
             "    )[['year']])",
             "",
             "Slope > 0: worsening",
             "Slope < 0: improving"])
    c.showPage()

    # ── Slide 8: Persistent Hot Spots ────────────────────────────
    header(c, "Policy Deep Dive: Persistent Hot Spots (HH→HH)",
           "What a decade of persistence tells us about structural hardship")
    footer(c, 8, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>What HH→HH tells us:</b>", h2_s),
        B("These tracts have been in the highest-hardship tier for a decade"),
        B("Economic recovery broadly missed them — not a temporary shock"),
        B("Spatial clustering persisted — neighboring areas didn't pull them up"),
        12.0,
        Paragraph("<b>What drives persistence? (Sampson, 2012):</b>", h2_s),
        B("Concentrated poverty generates neighborhood effects that amplify disadvantage"),
        B("School quality, peer effects, violence, environmental exposure"),
        B("Network closure: residents can't access jobs in other areas"),
        B("Institutional abandonment: banks redline, businesses don't locate there"),
        12.0,
        Paragraph("<b>Intervention implications:</b>", h2_s),
        B("Single-program interventions rarely sufficient for persistent hot spots"),
        B("Simultaneous investment in: housing + schools + health + economic opportunity"),
        B("Comprehensive community development is evidence-backed approach"),
        B("Timeline measured in years to decades, not months"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.70, rw, h*0.70,
            "Sampson (2012)",
            ["Concentrated poverty",
             "persists for decades",
             "even as individuals",
             "come and go.",
             "",
             "It is a property of",
             "the PLACE, not just",
             "the current residents.",
             "",
             "This is why place-based",
             "policy makes sense for",
             "persistent hot spots,",
             "even accounting for",
             "selection bias.",
             "",
             "The place itself",
             "perpetuates disadvantage."])
    c.showPage()

    # ── Slide 9: Emerging Hot Spots ───────────────────────────────
    header(c, "Policy Deep Dive: Emerging Hot Spots (→HH)",
           "The early intervention window — Galster's tipping point theory")
    footer(c, 9, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>What NS/LL→HH tells us:</b>", h2_s),
        B("This area was not a hot spot in 2013 but became one by 2019"),
        B("Deterioration has accelerated and begun to cluster spatially"),
        B("Clustering means it's spreading — adjacent areas being pulled down"),
        12.0,
        Paragraph("<b>Galster's tipping point theory:</b>", h2_s),
        B("Neighborhoods have thresholds beyond which self-reinforcing decline begins"),
        B("Below threshold: idiosyncratic shocks, recovery possible"),
        B("Above threshold: feedback loops lock in decline"),
        B("The emerging hot spot may be near the threshold — intervention has "
          "highest expected value here"),
        12.0,
        Paragraph("<b>What to look for in Maricopa County:</b>", h2_s),
        B("Emerging hot spots near persistent hot spots (spatial spread?)"),
        B("Emerging hot spots in areas with recent economic shocks"),
        B("Emerging hot spots where housing affordability has deteriorated fastest"),
        12.0,
        Paragraph("<b>Key question:</b> Is emergence due to spatial spread or local shock? "
                  "Space-time Moran's I helps answer this.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.72, rw, h*0.72,
            "Prevention vs. remediation",
            ["It is generally cheaper",
             "to prevent a neighborhood",
             "from becoming a persistent",
             "hot spot than to remediate",
             "one already entrenched.",
             "",
             "The emerging hot spot",
             "is the early warning signal.",
             "",
             "Effective interventions:",
             "· Code enforcement",
             "· Small business lending",
             "· Proactive tenant",
             "  protections",
             "· Anchor institution",
             "  engagement"])
    c.showPage()

    # ── Slide 10: Dissolving Hot Spots ────────────────────────────
    header(c, "Policy Deep Dive: Dissolving Hot Spots (HH→NS)",
           "Recovery success — but whose recovery?")
    footer(c, 10, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>What HH→NS tells us:</b>", h2_s),
        B("These areas were hot spots in 2013 but the cluster broke up by 2019"),
        B("Hardship levels declined in aggregate"),
        B("Spatial concentration of hardship dissipated"),
        12.0,
        Paragraph("<b>Two very different causes of dissolution:</b>", h2_s),
        B("<b>Genuine recovery</b>: Existing residents' circumstances improved — "
          "jobs, income, services"),
        B("<b>Displacement-driven change</b>: Original residents replaced by wealthier "
          "newcomers; poverty moved elsewhere"),
        12.0,
        Paragraph("<b>How to investigate (Ding et al., 2016):</b>", h2_s),
        B("Census alone cannot distinguish these two causes"),
        B("Look for signals: falling poverty + rapidly rising rents + demographic shift"),
        B("HMDA loan data: are new mortgages going to higher-income borrowers?"),
        B("Building permits: is the housing stock turning over rapidly?"),
        12.0,
        Paragraph("<b>Policy priority:</b>", h2_s),
        B("If displacement: anti-displacement measures, community land trusts, "
          "affordable housing preservation"),
        B("If genuine recovery: stabilization, prevent re-deterioration"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.72, rw, h*0.72,
            "Ding et al. (2016)",
            ["Vulnerable residents in",
             "gentrifying neighborhoods",
             "are not dramatically",
             "more likely to move.",
             "",
             "But when they DO move,",
             "they tend to relocate",
             "to lower-income areas.",
             "",
             "The poverty doesn't",
             "disappear — it moves",
             "somewhere with fewer",
             "resources and services.",
             "",
             "Monitor rents and",
             "demographic composition",
             "alongside hardship index."])
    c.showPage()

    # ── Slide 11: HL Outliers ─────────────────────────────────────
    header(c, "Policy Deep Dive: Spatial Outliers (HL)",
           "Isolated pockets of hardship — the hardest cases to reach")
    footer(c, 11, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>What HL tells us:</b>", h2_s),
        B("High-hardship tract completely surrounded by low-hardship neighbors"),
        B("Spatial spillover of recovery from nearby areas is NOT reaching this tract"),
        B("Something about this location maintains hardship despite prosperous surroundings"),
        12.0,
        Paragraph("<b>Common causes in urban areas:</b>", h2_s),
        B("Concentrated public housing — creates sharp hardship boundary"),
        B("Language or cultural isolation — community doesn't access nearby opportunities"),
        B("Physical barriers: highway, railroad, or industrial zone"),
        B("Historical boundary: redlining legacy creates a persistent pocket"),
        12.0,
        Paragraph("<b>Why HL outliers are often underserved:</b>", h2_s),
        B("Many place-based programs require a contiguous area above a threshold"),
        B("A single isolated tract may not qualify for Promise Zone, OZ, or CDBG targeting"),
        B("Invisible in county-level analysis — MAUP hides them completely"),
        B("Easy to miss when focusing only on the large persistent hot spot cluster"),
        12.0,
        Paragraph("<b>Implication:</b> HL outliers need individualized outreach, "
                  "not just area-based targeting.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.80, rw, h*0.80,
            "The isolation mechanism",
            ["Recovery in nearby areas",
             "doesn't help if residents",
             "can't access it due to:",
             "",
             "· No transportation to",
             "  nearby job centers",
             "· Language barriers",
             "· Discrimination in",
             "  hiring or housing",
             "· Social network",
             "  separation",
             "",
             "Two-pronged intervention:",
             "Place-based investment IN",
             "the area AND removing",
             "barriers TO nearby",
             "opportunity."])
    c.showPage()

    # ── Slide 12: R Workflow ──────────────────────────────────────
    header(c, "R Workflow — Complete Lab 6 Pipeline")
    footer(c, 12, TOTAL)
    x, y, w, h = cf()

    code_lines = [
        ("# 1. Spatial weights (from Lab 5 change_df)", True),
        ("nb <- poly2nb(change_df, queen=TRUE)", False),
        ("w  <- nb2listw(nb, style='W', zero.policy=TRUE)", False),
        ("", False),
        ("# 2. LISA on both periods", True),
        ("classify_lisa <- function(x, w, p=0.05) {", False),
        ("  lisa <- localmoran(x, w, zero.policy=TRUE)", False),
        ("  z <- scale(x)[,1]; wz <- lag.listw(w, z, zero.policy=TRUE)", False),
        ("  case_when(z>0&wz>0&lisa[,'Pr(z!=E(Ii))']<p ~ 'HH', ...)", False),
        ("}", False),
        ("change_df$lisa_2013 <- classify_lisa(change_df$hardship_2013, w)", False),
        ("change_df$lisa_2019 <- classify_lisa(change_df$hardship_2019, w)", False),
        ("", False),
        ("# 3. Transition matrix", True),
        ("table(change_df$lisa_2013, change_df$lisa_2019)", False),
        ("prop.table(..., margin=1) * 100", False),
        ("", False),
        ("# 4. Trajectory + space-time Moran's I", True),
        ("change_df$trajectory <- case_when(l13=='HH'&l19=='HH'~'Persistent HH', ...)", False),
        ("moran.mc(change_df$hardship_change, w, nsim=999)", False),
        ("", False),
        ("# 5. Three-point trend (year=2016 also uses 2010 boundaries)", True),
        ("cbg_2016 <- get_acs(..., year=2016)", False),
        ("r2016_z  <- apply_pooled_z(r2016, pooled_stats)  # same pooled_stats", False),
        ("slopes   <- all_years %>% group_by(GEOID) %>%", False),
        ("  summarise(slope=coef(lm(hardship_index~year))[['year']])", False),
    ]
    code_block(c, x, y, w, h, code_lines)
    c.showPage()

    # ── Slide 13: Trajectory Map Design ──────────────────────────
    header(c, "Trajectory Map — Color Design",
           "Seven categories: policy-intuitive colors communicate urgency")
    footer(c, 13, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    intro = Paragraph(
        "The trajectory map is the key deliverable of Lab 6. "
        "Colors are chosen to communicate <b>urgency and direction</b> at a glance.", body_s)
    pw, ph = intro.wrap(CW, 999)
    intro.drawOn(c, x, cy - ph)
    cy -= ph + 12

    traj_full = [
        ("Persistent HH",  "HH→HH",  RED,    "Deep red",     "Highest urgency — structural crisis"),
        ("Emerging HH",    "→HH",    ORANGE, "Orange",       "High urgency — deteriorating, intervention window open"),
        ("Dissolving HH",  "HH→",    YELLOW, "Pale yellow",  "Moderate — recovering, watch for displacement"),
        ("Persistent LL",  "LL→LL",  BLUE,   "Deep blue",    "Stably affluent — low equity urgency"),
        ("Emerging LL",    "→LL",    LBLUE,  "Light blue",   "Improving — monitor for displacement"),
        ("HL Outlier",     "HL",     PURPLE, "Purple",       "Isolated pocket — individualized outreach needed"),
        ("Stable NS",      "NS→NS",  NSIG,   "Gray",         "No significant spatial clustering in either period"),
    ]
    row_ht = (cy - y - 0.05*inch) / len(traj_full)
    for i, (name, trans, col, col_name, desc) in enumerate(traj_full):
        ry = cy - (i + 1) * row_ht
        # Swatch
        c.setFillColor(col)
        c.roundRect(x, ry + row_ht*0.10, 0.50*inch, row_ht*0.72,
                    radius=2*pt, fill=1, stroke=0)
        # Name + transition
        c.setFillColor(MAROON)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(x + 0.58*inch, ry + row_ht*0.55, name)
        c.setFillColor(MGRAY)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(x + 0.58*inch, ry + row_ht*0.22, trans)
        # Color name
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 1.60*inch, ry + row_ht*0.38, col_name)
        # Description
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 2.50*inch, ry + row_ht*0.38, desc)
    c.showPage()

    # ── Slide 14: Pattern → Mechanism → Policy ────────────────────
    header(c, "From Pattern to Policy",
           "The chain of inference must be explicit")
    footer(c, 14, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    # Chain diagram — safe layout, no text overlap
    steps = [
        ("Spatial\nPattern",   "LISA map\nModule 4"),
        ("Temporal\nChange",   "Change map\nModule 5"),
        ("Trajectory\nType",   "Persistent,\nEmerging..."),
        ("Causal\nMechanism",  "Theory +\nHistory"),
        ("Policy\nDesign",     "Targeted\nintervention"),
    ]
    n_steps = len(steps)
    box_h   = 0.85*inch           # tall enough for two lines of main + two of sub
    gap_frac = 0.28
    total_box_w = CW * 0.96
    bw = total_box_w / (n_steps + (n_steps - 1) * gap_frac)
    gap = bw * gap_frac
    bx  = x + CW * 0.02
    box_y = cy - box_h - 0.12*inch

    box_fills = [LGRAY, LGRAY, colors.HexColor("#FFF3F6"),
                 colors.HexColor("#FFFBF0"), colors.HexColor("#F0FFF0")]

    for i, (main, sub) in enumerate(steps):
        # Box
        c.setFillColor(box_fills[i])
        c.setStrokeColor(MAROON)
        c.setLineWidth(1)
        c.roundRect(bx, box_y, bw, box_h, radius=4*pt, fill=1, stroke=1)

        # Main label — anchored from TOP of box
        c.setFillColor(MAROON)
        c.setFont("Helvetica-Bold", 9)
        main_lines = main.split("\n")
        top_y = box_y + box_h - 15
        for li, line in enumerate(main_lines):
            c.drawCentredString(bx + bw/2, top_y - li*13, line)

        # Sub label — anchored from BOTTOM of box
        c.setFillColor(MGRAY)
        c.setFont("Helvetica", 7.5)
        sub_lines = sub.split("\n")
        bot_y = box_y + 22
        for li, line in enumerate(reversed(sub_lines)):
            c.drawCentredString(bx + bw/2, bot_y + li*10, line)

        # Arrow
        if i < n_steps - 1:
            ax = bx + bw + 2
            ay = box_y + box_h / 2
            c.setStrokeColor(GOLD)
            c.setFillColor(GOLD)
            c.setLineWidth(2)
            c.line(ax, ay, ax + gap - 5, ay)
            path = c.beginPath()
            path.moveTo(ax + gap - 5, ay + 4)
            path.lineTo(ax + gap - 5, ay - 4)
            path.lineTo(ax + gap + 3, ay)
            path.close()
            c.drawPath(path, fill=1, stroke=0)

        bx += bw + gap

    cy = box_y - 0.14*inch

    # Two columns below
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch

    left = [
        Paragraph("<b>LISA trajectory analysis provides steps 1–3.</b>", h2_s),
        Paragraph("Steps 4–5 require:", body_s),
        B("Theoretical knowledge (Galster, Sampson)"),
        B("Historical knowledge of Maricopa County"),
        B("Awareness of redlining, highway construction, school funding, zoning"),
        B("Knowledge of existing programs and institutions"),
        10.0,
        Paragraph("<b>The trajectory map is not a policy prescription.</b>", h2_s),
        Paragraph("It identifies <i>where</i> to look and <i>what questions</i> to ask.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, cy - h*0.48, rw, h*0.44,
            "The analyst's responsibility",
            ["The map shows WHERE.",
             "You must explain WHY.",
             "",
             "A persistent hot spot in",
             "South Phoenix reflects",
             "decades of redlining,",
             "highway construction,",
             "school funding inequity,",
             "and environmental",
             "injustice.",
             "",
             "Numbers without history",
             "are incomplete analysis."])
    c.showPage()

    # ── Slide 15: Lab 6 Preview ────────────────────────────────────
    header(c, "Lab 6 Preview")
    footer(c, 15, TOTAL)
    x, y, w, h = cf()
    hw = (w - 0.2*inch) / 2

    c.setFillColor(LGRAY)
    c.roundRect(x, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 10, y + h - 18, "What You Will Build")
    c.setFillColor(GOLD)
    c.rect(x + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)
    steps_lab6 = [
        "1.  Rebuild Lab 5 dataset (tract level)",
        "2.  Spatial weights matrix",
        "3.  LISA on 2013 hardship",
        "4.  LISA on 2019 hardship",
        "5.  Transition matrix (5×5)",
        "6.  Trajectory classification",
        "7.  Trajectory map (7 categories)",
        "8.  Space-time Moran's I",
        "9.  LISA on change scores",
        "10. Pull 2016 ACS data",
        "11. Three-point trend classification",
        "12. Trend slope map",
    ]
    iy = y + h - 34
    for s in steps_lab6:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 9)
        c.drawString(x + 12, iy, s)
        iy -= 12

    rx2 = x + hw + 0.2*inch
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.roundRect(rx2, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(rx2 + 10, y + h - 18, "Questions")
    c.setFillColor(GOLD)
    c.rect(rx2 + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)
    qs = [
        ("Q1", "Interpret trajectory map +"),
        ("",   "  transition matrix"),
        ("",   "  + space-time Moran's I"),
        ("",   "  + three-point trend"),
        ("",   "  Min. 200 words with specific"),
        ("",   "  numbers from outputs"),
        ("Q2", "Rerun with p < 0.01 threshold"),
        ("",   "  Compare trajectory distributions"),
        ("",   "  How many hot spots survive?"),
        ("Q3", "Policy brief: recommend which"),
        ("",   "  two trajectory types to"),
        ("",   "  prioritize and why."),
        ("",   "  Cite at least one reading."),
        ("",   "  Min. 150 words"),
    ]
    iy = y + h - 34
    for num, text in qs:
        c.setFillColor(MAROON if num else DGRAY)
        c.setFont("Helvetica-Bold" if num else "Helvetica", 9)
        c.drawString(rx2 + 12, iy, (num + "  " if num else "") + text)
        iy -= 12
    c.showPage()

    # ── Slide 16: Summary ─────────────────────────────────────────
    header(c, "Module 6 Summary")
    footer(c, 16, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    items = [
        Paragraph("<b>Six key ideas from Module 6:</b>", h1_s),
        10.0,
        N(1, "<b>LISA trajectories</b> — cross-tabulate cluster membership "
             "at two time points to classify tracts as persistent, emerging, "
             "dissolving, or stable."),
        N(2, "<b>Transition matrix</b> — diagonal measures persistence; "
             "off-diagonal measures change; high persistence signals structural "
             "conditions; high dissolution signals recovery pathway exists."),
        N(3, "<b>Space-time Moran's I</b> — tests whether change scores are "
             "spatially autocorrelated; significant positive I means decline "
             "or recovery is a spreading process."),
        N(4, "<b>LISA on change scores</b> — identifies where change is itself "
             "spatially clustering; HH of change = spreading decline front; "
             "highest-value early intervention target."),
        N(5, "<b>Three-point trend</b> — year=2016 adds a middle observation; "
             "classify as monotone or non-monotone; OLS slope gives a continuous "
             "trajectory measure."),
        N(6, "<b>Trajectory → policy</b> — persistent HH needs comprehensive "
             "multi-year investment; emerging HH needs prevention; dissolving HH "
             "needs anti-displacement monitoring; HL needs individualized outreach."),
    ]
    draw_items(c, items, x, cy, w)

    c.save()
    print(f"Module 6 → {OUTPUT}  ({TOTAL} slides)")


make_slides()
