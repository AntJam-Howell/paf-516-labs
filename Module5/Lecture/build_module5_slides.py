"""
Module 5 Lecture Slides PDF Builder
PAF 516 | Community Analytics
Temporal Change Analysis
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
MAROON = colors.HexColor("#8C1D40")
GOLD   = colors.HexColor("#FFC627")
WHITE  = colors.white
LGRAY  = colors.HexColor("#F5F5F5")
DGRAY  = colors.HexColor("#444444")
MGRAY  = colors.HexColor("#888888")
BLUE   = colors.HexColor("#2C7BB6")
RED    = colors.HexColor("#D7191C")
ORANGE = colors.HexColor("#FDAE61")
LBLUE  = colors.HexColor("#ABD9E9")

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
                 "PAF 516  |  Module 5  |  Temporal Change Analysis")
    c.drawRightString(W - MARGIN_R, 0.10*inch, f"{n} / {total}")

def title_slide(c):
    c.setFillColor(MAROON)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08*inch, W, 0.08*inch, fill=1, stroke=0)
    c.rect(0, 0, W, 0.08*inch, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W/2, H*0.62, "Temporal Change Analysis")
    c.setFillColor(GOLD)
    c.rect(W*0.25, H*0.54, W*0.5, 2*pt, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#FFF8E7"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(W/2, H*0.47,
        "ACS Vintages  ·  Boundary Consistency  ·  Pooled Standardization")
    c.drawCentredString(W/2, H*0.39,
        "Diverging Palettes  ·  MOE Significance Testing")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 12)
    c.drawCentredString(W/2, H*0.28,
        "PAF 516  |  Community Analytics  |  Module 5")
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
    """Content frame: x, y, w, h"""
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


# ══════════════════════════════════════════════════════════════════
# SLIDES
# ══════════════════════════════════════════════════════════════════

def make_slides():
    OUTPUT = "/home/claude/Module5_Lecture_Slides.pdf"
    TOTAL  = 16

    c = canvas.Canvas(OUTPUT, pagesize=(W, H))
    c.setTitle("Module 5 – Temporal Change Analysis")
    c.setAuthor("Anthony Howell, PhD")
    c.setSubject("PAF 516 Community Analytics")

    # ── Slide 1: Title ────────────────────────────────────────────
    title_slide(c)
    c.showPage()

    # ── Slide 2: The Core Question ────────────────────────────────
    header(c, "The Core Question", "Adding the time dimension to hardship analysis")
    footer(c, 2, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("Modules 1–4 analyzed Maricopa County at a <b>single point in time.</b>", body_s),
        8.0,
        Paragraph("Phoenix was ground zero for the 2008 housing crisis — one of the highest "
                  "foreclosure rates in the US. This module asks:", body_s),
        10.0,
        Paragraph("<b>Which neighborhoods recovered? Which were left behind?</b>", h1_s),
        14.0,
        Paragraph("<b>Two time points — both on 2010 TIGER/Line boundaries:</b>", h2_s),
        B("<b>2013</b> (2009–2013 ACS) — mid-recovery; unemployment still ~7%"),
        B("<b>2019</b> (2015–2019 ACS) — recovery peak; unemployment ~3.5%, pre-COVID"),
        12.0,
        Paragraph("Same hardship index. Same boundary vintage. One question:", body_s),
        Paragraph("where did the decade take each census tract?", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.60, rw, h*0.60,
            "Module 5 adds the time dimension",
            ["Retrieve the same 4 hardship",
             "variables for both periods.",
             "",
             "Apply pooled standardization",
             "so z-scores are directly",
             "comparable across years.",
             "",
             "Compute change scores,",
             "test significance with MOE,",
             "map with diverging palette,",
             "overlay Lab 4 LISA clusters."])
    c.showPage()

    # ── Slide 3: Boundary Vintage Problem ─────────────────────────
    header(c, "The Boundary Vintage Problem",
           "Why 2013 vs. 2019 — and why not 2010 vs. 2023")
    footer(c, 3, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>Census boundaries are redrawn every decade:</b>", h2_s),
        B("ACS vintages 2013–2019 → <b>2010</b> TIGER/Line boundaries"),
        B("ACS vintages 2020–present → <b>2020</b> TIGER/Line boundaries"),
        12.0,
        Paragraph("<b>Mixing vintages creates holes in the map:</b>", h2_s),
        B("Some tracts were split, merged, or renumbered between 2010 and 2020"),
        B("inner_join(by='GEOID') silently drops mismatched tracts"),
        B("In fast-growing Maricopa → can lose 15–25% of all tracts"),
        B("The map shows white gaps — a <i>methodological artifact</i>, not missing data"),
        12.0,
        Paragraph("<b>The fix: compare two years on the same boundary vintage.</b>", h2_s),
        8.0,
        Paragraph("year = 2013   ←   2009–2013 ACS, <b>2010</b> TIGER/Line", code_s),
        Paragraph("year = 2019   ←   2015–2019 ACS, <b>2010</b> TIGER/Line", code_s),
        6.0,
        Paragraph("Every GEOID matches. Zero missing tracts.", body_s),
        12.0,
        Paragraph("<b>Block group vs. tract:</b>", h2_s),
        B("Block groups: NA rate ~15–20% due to zero-count denominators"),
        B("Census tracts: NA rate ~1–2%; larger populations = stable denominators"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.70, rw, h*0.70,
            "Note: block group availability",
            ["tidycensus does not support",
             "block groups before",
             "year = 2013.",
             "",
             "year = 2013 (2009–2013 ACS)",
             "is the earliest usable",
             "block group vintage.",
             "",
             "For tracts, data goes back",
             "to year = 2009.",
             "",
             "Lab 6 three-point trend:",
             "year = 2016 also uses",
             "2010 boundaries — all",
             "three points match."])
    c.showPage()

    # ── Slide 4: Variable Consistency ─────────────────────────────
    header(c, "Variable Consistency Across Vintages",
           "Adjusting the indicator set when tables change between years")
    footer(c, 4, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("ACS table structures change across years. <b>B27010_017</b> (no insurance, "
                  "ages 18–34) did not exist in the 2013 ACS.", body_s),
        10.0,
        Paragraph("<b>Lab 5 uses a 4-variable hardship index:</b>", h2_s),
        8.0,
    ]
    cy = draw_items(c, left, x, cy, lw)

    # Variable table
    rows = [
        ["Variable", "Census Table", "Direction"],
        ["Poverty rate",      "C17002_002+_003 / _001", "↑ = more hardship"],
        ["Unemployment rate", "B23025_005 / _002",      "↑ = more hardship"],
        ["No HS diploma",     "B15003_002 / _001",      "↑ = more hardship"],
        ["Median income",     "B19013_001",             "↑ = LESS hardship (reversed)"],
    ]
    col_ws = [lw*0.30, lw*0.42, lw*0.28]
    row_h  = 0.30*inch
    for ri, row in enumerate(rows):
        ry = cy - (ri + 1) * row_h
        bg = MAROON if ri == 0 else (WHITE if ri % 2 else LGRAY)
        c.setFillColor(bg)
        c.rect(x, ry, lw, row_h, fill=1, stroke=0)
        cx2 = x
        for ci, (cell, cw) in enumerate(zip(row, col_ws)):
            tc = WHITE if ri == 0 else DGRAY
            c.setFillColor(tc)
            fn = "Helvetica-Bold" if ri == 0 else "Helvetica"
            c.setFont(fn, 8.5)
            c.drawString(cx2 + 5, ry + row_h * 0.32, cell)
            cx2 += cw
    cy -= (len(rows) + 0.3) * row_h

    left2 = [
        12.0,
        Paragraph("All four tables available in every ACS vintage since 2005. Zero gaps.", body_s),
        12.0,
        Paragraph("<b>Lesson for practice:</b>", h2_s),
        Paragraph("Real analysts routinely adjust indicator sets for temporal comparisons. "
                  "Documenting the decision is part of the analysis, not a limitation to hide.", body_s),
    ]
    draw_items(c, left2, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.55, rw, h*0.55,
            "Index construction",
            ["1. Compute rates from",
             "   numerator/denominator",
             "2. Pooled standardization",
             "   (next slide)",
             "3. Reverse-code income",
             "4. Row mean of 4 z-scores",
             "   = hardship index",
             "",
             "Same function applied twice:",
             "apply_pooled_z(r2013, stats)",
             "apply_pooled_z(r2019, stats)"])
    c.showPage()

    # ── Slide 5: Pooled Standardization ───────────────────────────
    header(c, "Pooled Standardization",
           "Why year-specific z-scores cannot be subtracted")
    footer(c, 5, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    # Formula box — constrained to left column
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.52*inch, lw*0.96, 0.46*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + lw/2, cy - 0.20*inch,
                        "z_i,t  =  (x_i,t  −  mean_pooled)  /  sd_pooled")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(x + lw/2, cy - 0.38*inch,
                        "pooled over all observations from both years combined")
    cy -= 0.60*inch

    left = [
        Paragraph("<b>The problem with year-specific z-scores:</b>", h2_s),
        B("Each year standardized to mean=0, SD=1 <i>for that year</i>"),
        B("z=1.0 in 2013 = 1 SD above 2013's mean"),
        B("z=1.0 in 2019 = 1 SD above 2019's mean"),
        B("2013 was a harder year — its mean IS higher"),
        B("Year-specific standardization <b>hides</b> the year-level mean difference"),
        B("Result: most tracts appear 'stable' even if the county improved dramatically"),
        12.0,
        Paragraph("<b>Pooled standardization:</b>", h2_s),
        B("Compute mean and SD from both years <i>combined</i>"),
        B("Apply the same scale to both years"),
        B("Now z=1.0 means the same thing in 2013 and 2019"),
        B("Change scores are directly interpretable in common units"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.80, rw, h*0.80,
            "Worked example",
            ["Unemployment rate: 10%",
             "in both 2013 and 2019.",
             "",
             "Year-specific z-scores:",
             "  2013: (10-12.3)/4.1 = -0.56",
             "  2019: (10-6.8)/2.9 = +1.10",
             "  Change: +1.66 → 'WORSENED'",
             "",
             "Pooled z-scores:",
             "  2013: (10-9.6)/4.4 = +0.09",
             "  2019: (10-9.6)/4.4 = +0.09",
             "  Change: 0.00 → 'STABLE'",
             "",
             "The rate is identical in",
             "both years. Only pooled",
             "correctly says 'stable.'"])
    c.showPage()

    # ── Slide 6: Change Scores ────────────────────────────────────
    header(c, "Computing and Interpreting Change Scores")
    footer(c, 6, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.54 - 0.10*inch
    rw = w * 0.43
    rx = x + w * 0.54 + 0.10*inch
    cy = y + h

    # Formula
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.48*inch, lw*0.96, 0.42*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x + lw/2, cy - 0.20*inch,
                        "Δ_i  =  hardship_2019  −  hardship_2013")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(x + lw/2, cy - 0.36*inch,
                        "Both indices use pooled z-score standardization")
    cy -= 0.56*inch

    left = [
        Paragraph("<b>Sign convention:</b>", h2_s),
        B("<b>Positive Δ</b>: hardship increased (worsened) over the decade"),
        B("<b>Negative Δ</b>: hardship decreased (improved) over the decade"),
        B("<b>Near zero</b>: neighborhood was stable"),
        12.0,
        Paragraph("<b>Magnitude is interpretable:</b>", h2_s),
        B("Δ = +0.5 → moved half a pooled SD toward more hardship"),
        B("Δ = −1.0 → moved one full pooled SD toward less hardship"),
        B("These are meaningful movements on a common scale"),
        12.0,
        Paragraph("<b>Summary statistics to compute:</b>", h2_s),
        B("Mean change — did the county improve or worsen on average?"),
        B("% tracts that worsened vs. improved"),
        B("Distribution shape — symmetric or skewed?"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.55, rw, h*0.55,
            "Watch out for: outliers",
            ["A single tract with an",
             "extreme change score (+4.0)",
             "compresses the entire scale.",
             "",
             "Solution: winsorize at",
             "2nd and 98th percentiles",
             "before mapping.",
             "",
             "lo <- quantile(x, 0.02)",
             "hi <- quantile(x, 0.98)",
             "x_plot <- pmax(pmin(x,hi),lo)"])
    c.showPage()

    # ── Slide 7: MOE Significance ──────────────────────────────────
    header(c, "Margins of Error — Testing Significance of Change",
           "Not all observed change is real change")
    footer(c, 7, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    # Formula
    c.setFillColor(LGRAY)
    c.roundRect(x + lw*0.02, cy - 0.52*inch, lw*0.96, 0.46*inch,
                radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + lw/2, cy - 0.18*inch,
                        "z  =  (est_2019 − est_2013) / sqrt(SE_2019²  +  SE_2013²)")
    c.setFillColor(MGRAY)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(x + lw/2, cy - 0.35*inch,
                        "SE = MOE / 1.645   (for 90% confidence intervals)")
    c.setFillColor(DGRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(x + lw/2, cy - 0.46*inch,
                        "If |z| > 1.645 → significant at 90% level")
    cy -= 0.60*inch

    left = [
        Paragraph("<b>Why test significance?</b>", h2_s),
        B("A change from 15% to 18% poverty looks meaningful on a map"),
        B("But if both estimates have MOE ± 5 ppts, the 'change' is sampling noise"),
        B("Plotting all change scores shows noise as signal"),
        12.0,
        Paragraph("<b>Implementation:</b>", h2_s),
        B("Apply to the poverty rate — most interpretable individual variable"),
        B("Create a sig_change flag (TRUE/FALSE) for each tract"),
        B("Significance map: gray = not significant, colored = significant"),
        B("Expect 40–60% of tracts significant for a strong county-level trend"),
        12.0,
        Paragraph("<b>MOE propagation for a rate (proportion):</b>", h2_s),
        8.0,
        Paragraph("MOE_rate = sqrt(MOE_num² + rate² × MOE_den²) / den", code_s),
        6.0,
        Paragraph("Then SE = MOE_rate / 1.645", code_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.80, rw, h*0.80,
            "Why MOEs are large at small geographies",
            ["ACS 5-year estimates",
             "average ~60 interviews",
             "per block group/year.",
             "",
             "For tracts: ~300–500",
             "interviews per year.",
             "",
             "Spielman et al. (2014):",
             "~30% of block group",
             "estimates have",
             "MOE > estimate.",
             "",
             "Tract-level MOEs are",
             "substantially smaller —",
             "another reason to use",
             "tracts for change analysis."])
    c.showPage()

    # ── Slide 8: Diverging Color Scales ───────────────────────────
    header(c, "Diverging Color Scales for Change Maps",
           "Change has a meaningful midpoint (zero) — use a diverging palette")
    footer(c, 8, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>Why not viridis?</b>", h2_s),
        B("Sequential palettes (viridis) go from low to high — one direction only"),
        B("Change data has two directions: positive AND negative"),
        B("A sequential palette for change gives no visual cue about direction"),
        12.0,
        Paragraph("<b>Diverging palettes: two hues from a neutral center</b>", h2_s),
        8.0,
        Paragraph("scale_fill_gradient2(", code_s),
        Paragraph("  low      = '#2C7BB6',   # blue = improvement", code_s),
        Paragraph("  mid      = 'white',      # neutral = no change", code_s),
        Paragraph("  high     = '#D7191C',    # red = worsening", code_s),
        Paragraph("  midpoint = 0,            # center on ZERO, not median", code_s),
        Paragraph("  limits   = c(-k, k)      # symmetric limits", code_s),
        Paragraph(")", code_s),
        12.0,
        Paragraph("<b>Three critical design rules:</b>", h2_s),
        N(1, "<b>Center on zero</b> — not the data median"),
        N(2, "<b>Symmetric limits</b> — equal visual weight for positive and negative"),
        N(3, "<b>Winsorize before plotting</b> — outliers compress the scale"),
    ]
    draw_items(c, left, x, cy, lw)

    # Color swatch
    swatch_data = [
        (BLUE,                             "Improved (large)"),
        (colors.HexColor("#74ADD1"),       "Improved (moderate)"),
        (colors.HexColor("#E0EEF8"),       "Improved (slight)"),
        (colors.HexColor("#F5F5F5"),       "No change"),
        (colors.HexColor("#F4C2AE"),       "Worsened (slight)"),
        (colors.HexColor("#E8896C"),       "Worsened (moderate)"),
        (RED,                              "Worsened (large)"),
    ]
    sw = rw * 0.38
    sh = (h * 0.80) / len(swatch_data)
    sy_top = y + h * 0.05 + h * 0.80
    for i, (col, label) in enumerate(swatch_data):
        sy = sy_top - (i + 1) * sh
        c.setFillColor(col)
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.3)
        c.rect(rx, sy, sw, sh * 0.88, fill=1, stroke=1)
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8)
        c.drawString(rx + sw + 6, sy + sh * 0.30, label)
    c.showPage()

    # ── Slide 9: Three-Panel Map ───────────────────────────────────
    header(c, "The Three-Panel Map",
           "Connecting starting conditions, ending conditions, and change")
    footer(c, 9, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    intro = Paragraph(
        "A single change map answers <i>what changed</i> but not <i>from what starting point</i>. "
        "The three-panel layout provides full context.", body_s)
    pw, ph = intro.wrap(w, 999)
    intro.drawOn(c, x, cy - ph)
    cy -= ph + 12

    cw3 = (w - 0.3*inch) / 3
    panels = [
        ("Panel 1: Hardship 2013",   BLUE,   "Sequential viridis palette",
         ["2009–2013 ACS", "Post-crisis starting point",
          "Who was worst off at the start?"]),
        ("Panel 2: Hardship 2019",   MAROON, "Sequential viridis palette",
         ["2015–2019 ACS", "Recovery peak (pre-COVID)",
          "Who benefited from recovery?"]),
        ("Panel 3: Change (2019−2013)", colors.HexColor("#444444"),
         "Diverging blue–white–red",
         ["Winsorized at 2nd/98th pct",
          "Centered on zero",
          "Blue = improved | Red = worsened"]),
    ]
    bh_p = cy - y - 0.70*inch
    for i, (title_p, col, palette, notes) in enumerate(panels):
        bx = x + i * (cw3 + 0.15*inch)
        c.setFillColor(col)
        c.roundRect(bx, y + 0.60*inch + bh_p, cw3, 0.34*inch,
                    radius=3*pt, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(bx + cw3/2, y + 0.60*inch + bh_p + 0.11*inch, title_p)
        c.setFillColor(LGRAY)
        c.roundRect(bx, y + 0.55*inch, cw3, bh_p, radius=3*pt, fill=1, stroke=0)
        c.setFillColor(MGRAY)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(bx + cw3/2, y + 0.55*inch + bh_p - 16, palette)
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 8)
        ny = y + 0.55*inch + bh_p * 0.52
        for note in notes:
            c.drawCentredString(bx + cw3/2, ny, f"• {note}")
            ny -= 13

    # Bottom callout
    callout(c, x, y, w, 0.50*inch,
            "Why all three panels?",
            ["A tract that worsened from a position of low hardship is very different from one that worsened from already high hardship. "
             "The three-panel layout provides full policy context."])
    c.showPage()

    # ── Slide 10: LISA Overlay ─────────────────────────────────────
    header(c, "Overlay: Connecting to Lab 4 LISA Clusters",
           "Are hot spots worsening, improving, or stable?")
    footer(c, 10, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>The key policy question from Module 4:</b>", h2_s),
        B("Lab 4 identified statistically significant hot spots (HH) and cold spots (LL)"),
        B("Lab 5 asks: over the decade, did those clusters "
          "<i>persist, worsen, or dissolve?</i>"),
        14.0,
        Paragraph("<b>Three possible findings:</b>", h2_s),
        10.0,
    ]
    cy = draw_items(c, left, x, cy, lw)

    findings = [
        (RED,   "Hot spots worsening",
         "Spatial concentration deepening. Structural hardship entrenching. Urgent."),
        (MGRAY, "Hot spots stable",
         "Recovery bypassed these areas. Persistent structural hardship — not temporary."),
        (BLUE,  "Hot spots improving",
         "Recovery is reaching them. Clusters dissolving — watch for displacement."),
    ]
    for col, label, desc in findings:
        c.setFillColor(col)
        c.roundRect(x, cy - 0.36*inch, lw, 0.32*inch, radius=3*pt, fill=1, stroke=0)
        c.setFillColor(WHITE if col != MGRAY else DGRAY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 8, cy - 0.22*inch, label)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 8, cy - 0.32*inch, desc)
        cy -= 0.42*inch

    callout(c, rx, y + h - 0.12*inch - h*0.70, rw, h*0.70,
            "In R",
            ["ggplot(change_df) +",
             "  geom_sf(aes(",
             "    fill=change_plot),",
             "    color=NA) +",
             "  scale_fill_gradient2(",
             "    ...) +",
             "  # Outline HH hot spots:",
             "  geom_sf(",
             "    data=change_df %>%",
             "      filter(",
             "        lisa_quad=='HH'),",
             "    fill=NA,",
             "    color='black',",
             "    linewidth=0.4)"])
    c.showPage()

    # ── Slide 11: Displacement Paradox ────────────────────────────
    header(c, "What Change Maps Cannot Tell You",
           "The displacement paradox and limits of aggregate census data")
    footer(c, 11, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>A tract where poverty drops from 35% to 12% over six years:</b>", h2_s),
        10.0,
        Paragraph("<b>Interpretation A — Genuine recovery:</b>", h2_s),
        Paragraph("Existing residents' circumstances improved through employment, "
                  "income growth, and better services.", body_s),
        10.0,
        Paragraph("<b>Interpretation B — Displacement:</b>", h2_s),
        Paragraph("Original poor residents replaced by wealthier newcomers. "
                  "The poverty moved elsewhere — to a neighborhood with fewer resources.", body_s),
        14.0,
        Paragraph("<b>The census change score cannot distinguish these.</b>", h1_s),
        12.0,
        Paragraph("<b>What you CAN observe:</b>", h2_s),
        B("Change in average hardship of whoever lives there in 2019"),
        B("Whether the spatial pattern of hardship shifted"),
        B("Statistical significance vs. sampling noise"),
        10.0,
        Paragraph("<b>What you CANNOT observe from census alone:</b>", h2_s),
        B("Whether original residents improved or moved out"),
        B("Where displaced residents went"),
        B("Who moved in vs. who stayed"),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.85, rw, h*0.85,
            "Ding et al. (2016)",
            ["Vulnerable residents in",
             "gentrifying neighborhoods",
             "are not dramatically",
             "more likely to move.",
             "",
             "But when they DO move,",
             "they relocate to",
             "lower-income areas.",
             "",
             "The poverty doesn't",
             "disappear — it moves",
             "somewhere with fewer",
             "resources and services.",
             "",
             "Census change maps are",
             "hypothesis generators,",
             "not causal evidence."])
    c.showPage()

    # ── Slide 12: Theoretical Frameworks ──────────────────────────
    header(c, "Theoretical Frameworks for Neighborhood Change",
           "What drives the patterns on the change map?")
    footer(c, 12, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>Temkin &amp; Rohe (1996) — multidimensional model:</b>", h2_s),
        B("Change driven by: institutional actors, social fabric, metropolitan forces"),
        B("No single driver — requires multi-sector analysis to explain patterns"),
        12.0,
        Paragraph("<b>Freeman (2005) — displacement vs. succession:</b>", h2_s),
        B("Improving neighborhoods don't necessarily displace residents"),
        B("Change often driven by relative affluence of in-movers"),
        B("Displacement is real but aggregate census data can't detect it"),
        12.0,
        Paragraph("<b>Landis (2016) — multi-metro empirical patterns:</b>", h2_s),
        B("Gentrification is ONE of several upward-mobility pathways"),
        B("Other pathways: employment growth, anchor institutions, infrastructure"),
        B("Most neighborhood improvement is NOT classic gentrification"),
        12.0,
        Paragraph("<b>For your Yellowdig post:</b>", h2_s),
        Paragraph("Which framework best explains the pattern you observe in Maricopa County? "
                  "Use specific numbers from your change map.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.55, rw, h*0.55,
            "Analysis vs. description",
            ["Your change map shows",
             "the WHAT.",
             "",
             "These readings give you",
             "vocabulary to argue",
             "about the WHY.",
             "",
             "Good analysis connects:",
             "· Statistical pattern",
             "· Theoretical mechanism",
             "· Policy implication",
             "",
             "This is what separates",
             "analysis from description."])
    c.showPage()

    # ── Slide 13: R Workflow ───────────────────────────────────────
    header(c, "R Workflow — Complete Lab 5 Pipeline")
    footer(c, 13, TOTAL)
    x, y, w, h = cf()

    code_lines = [
        ("# 1. Pull data — same boundary vintage (both 2010 TIGER/Line)", True),
        ("tract_2013 <- get_acs(geography='tract', year=2013, state='AZ', county='Maricopa'...)", False),
        ("tract_2019 <- get_acs(geography='tract', year=2019, state='AZ', county='Maricopa'...)", False),
        ("", False),
        ("# 2. Compute rates from numerator/denominator pairs", True),
        ("wide <- pivot_wider(...) %>% mutate(poverty_rate = (pov_below50+pov_50to99)/pov_den, ...)", False),
        ("", False),
        ("# 3. Pooled standardization", True),
        ("pooled_mean <- mean(c(r2013$poverty_rate, r2019$poverty_rate))", False),
        ("pooled_sd   <- sd(c(r2013$poverty_rate,   r2019$poverty_rate))", False),
        ("z_2013 <- (r2013$poverty_rate - pooled_mean) / pooled_sd", False),
        ("", False),
        ("# 4. Composite index: row mean of 4 pooled z-scores (income reversed)", True),
        ("hardship_index <- rowMeans(cbind(z_pov, z_unemp, z_hs, -z_inc))", False),
        ("", False),
        ("# 5. Join and compute change score", True),
        ("change_df <- inner_join(p2019_sf, p2013_tbl, by='GEOID') %>%", False),
        ("  mutate(hardship_change = hardship_2019 - hardship_2013)", False),
        ("", False),
        ("# 6. MOE significance test for poverty rate", True),
        ("pov_z      <- pov_change / sqrt(se_2013^2 + se_2019^2)", False),
        ("sig_change <- abs(pov_z) > 1.645", False),
        ("", False),
        ("# 7. Winsorize and map", True),
        ("max_abs <- max(abs(quantile(change_df$hardship_change, c(0.02, 0.98))))", False),
        ("ggplot(change_df) + scale_fill_gradient2(midpoint=0, limits=c(-max_abs, max_abs))", False),
    ]
    code_block(c, x, y, w, h, code_lines)
    c.showPage()

    # ── Slide 14: Lab 5 Preview ────────────────────────────────────
    header(c, "Lab 5 Preview")
    footer(c, 14, TOTAL)
    x, y, w, h = cf()
    hw = (w - 0.2*inch) / 2

    # Left box
    c.setFillColor(LGRAY)
    c.roundRect(x, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 10, y + h - 18, "What You Will Build")
    c.setFillColor(GOLD)
    c.rect(x + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)
    steps = [
        "1.  Pull 2013 & 2019 ACS tract data",
        "     (both on 2010 TIGER/Line boundaries)",
        "2.  Compute rates (4 variables)",
        "3.  Pooled standardization",
        "4.  Join + compute change scores",
        "5.  MOE significance test",
        "6.  Winsorized change map",
        "7.  Significance overlay map",
        "8.  Three-panel patchwork",
        "9.  Lab 4 LISA overlay",
    ]
    iy = y + h - 34
    for s in steps:
        c.setFillColor(DGRAY)
        c.setFont("Helvetica", 9)
        c.drawString(x + 12, iy, s)
        iy -= 13

    # Right box
    rx2 = x + hw + 0.2*inch
    c.setFillColor(colors.HexColor("#FFF3F6"))
    c.roundRect(rx2, y, hw, h, radius=4*pt, fill=1, stroke=0)
    c.setFillColor(MAROON)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(rx2 + 10, y + h - 18, "Key Takeaways")
    c.setFillColor(GOLD)
    c.rect(rx2 + 10, y + h - 22, hw - 20, 1.5, fill=1, stroke=0)
    takeaways = [
        ("1.", "Boundary vintage consistency"),
        ("",   "  → same boundaries = zero gaps"),
        ("2.", "Variable consistency"),
        ("",   "  → document dropped indicators"),
        ("3.", "Pooled standardization"),
        ("",   "  → comparable z-scores across years"),
        ("4.", "Change score = Δ hardship index"),
        ("",   "  → magnitude interpretable"),
        ("5.", "MOE significance test"),
        ("",   "  → separate signal from noise"),
        ("6.", "Diverging palette centered on zero"),
        ("",   "  → symmetric, winsorized"),
        ("7.", "Overlay Lab 4 LISA clusters"),
        ("",   "  → hot spots persisting or dissolving?"),
    ]
    iy = y + h - 34
    for num, text in takeaways:
        c.setFillColor(MAROON if num else DGRAY)
        c.setFont("Helvetica-Bold" if num else "Helvetica", 9)
        c.drawString(rx2 + 12, iy, num + text)
        iy -= 12
    c.showPage()

    # ── Slide 15: MOE Deep Dive ────────────────────────────────────
    header(c, "Why ACS MOEs Are Large at Small Geographies",
           "Small populations × rolling 5-year window = high uncertainty")
    footer(c, 15, TOTAL)
    x, y, w, h = cf()
    lw = w * 0.56 - 0.10*inch
    rw = w * 0.41
    rx = x + w * 0.56 + 0.10*inch
    cy = y + h

    left = [
        Paragraph("<b>What drives large MOEs:</b>", h2_s),
        B("ACS 5-year estimates average ~60 interviews per block group per year"),
        B("For census tracts: ~300–500 per year — substantially more reliable"),
        B("Small subpopulations (unemployed, no HS diploma) have few observed cases"),
        B("The 90% CI formula: MOE encompasses the true value 90% of the time"),
        12.0,
        Paragraph("<b>Typical MOEs for poverty rate:</b>", h2_s),
        B("Block groups, rural/low-density: MOE ± 8–12 percentage points"),
        B("Block groups, dense urban:       MOE ± 2–4 percentage points"),
        B("Census tracts:                   MOE ± 1–3 percentage points"),
        12.0,
        Paragraph("<b>Propagating MOE for a rate proportion:</b>", h2_s),
        8.0,
        Paragraph("MOE_rate = sqrt(MOE_num² + rate² × MOE_den²) / den", code_s),
        Paragraph("SE = MOE_rate / 1.645", code_s),
        Paragraph("z_change = (est_2019 - est_2013) / sqrt(SE_2013² + SE_2019²)", code_s),
        12.0,
        Paragraph("<b>Rule of thumb:</b> If MOE > half the estimate, treat as unreliable.", body_s),
    ]
    draw_items(c, left, x, cy, lw)

    callout(c, rx, y + h - 0.12*inch - h*0.88, rw, h*0.88,
            "Reference: Spielman et al. (2014)",
            ["Systematic analysis of",
             "where and why MOEs",
             "are largest in ACS data:",
             "",
             "· Low-population areas",
             "· Rural geographies",
             "· Minority populations",
             "  with small counts",
             "",
             "Key finding: ~30% of",
             "block group estimates",
             "have MOE > estimate.",
             "",
             "Census tracts: far fewer",
             "estimates fail this test.",
             "",
             "Always show significance",
             "alongside change maps."])
    c.showPage()

    # ── Slide 16: Summary ──────────────────────────────────────────
    header(c, "Module 5 Summary")
    footer(c, 16, TOTAL)
    x, y, w, h = cf()
    cy = y + h

    items = [
        Paragraph("<b>Seven key ideas from Module 5:</b>", h1_s),
        10.0,
        N(1, "<b>Boundary vintage consistency</b> — compare years on the same "
             "decennial TIGER/Line boundaries; year=2013 and year=2019 both "
             "use 2010 boundaries, zero missing tracts."),
        N(2, "<b>Variable consistency</b> — adjust the indicator set when "
             "tables change across vintages; document the decision explicitly."),
        N(3, "<b>Pooled standardization</b> — standardize both years against "
             "a combined mean/SD so z-scores measure the same quantity in both periods."),
        N(4, "<b>The change score</b> — positive = worsened, negative = improved; "
             "magnitude is interpretable in pooled standard deviation units."),
        N(5, "<b>MOE significance</b> — the Census Bureau z-test separates real "
             "change from sampling noise; always show the significance overlay."),
        N(6, "<b>Diverging palettes</b> — centered on zero with symmetric limits; "
             "winsorize before mapping to prevent outlier compression."),
        N(7, "<b>LISA overlay</b> — the most important policy question: are the "
             "hot spots from Lab 4 persisting, worsening, or dissolving? "
             "Module 6 answers this with trajectory analysis."),
    ]
    draw_items(c, items, x, cy, w)

    c.save()
    print(f"Module 5 → {OUTPUT}  ({TOTAL} slides)")


make_slides()
