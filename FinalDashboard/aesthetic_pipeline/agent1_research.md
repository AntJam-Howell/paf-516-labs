# Agent 1 — Research & Spec Extraction

Extract exact values from two reference sources, then produce a
complete design spec that Agent 2 implements without guessing.

---

## Source 1: Urban Institute urbnthemes colors

Fetch the exact hex codes from the official source:

  curl -s https://raw.githubusercontent.com/UrbanInstitute/urbnthemes/master/R/colors.R

Extract and document every hex code. Key ones needed:
  - palette_urbn_main (8 colors)
  - palette_urbn_diverging (8 colors)
  - palette_urbn_quintile (5 colors)
  - Any named individual colors (cyan, gray, yellow, magenta, etc.)

---

## Source 2: posit::conf 2024 Olympic dashboard SCSS

Fetch the custom SCSS from the reference dashboard:

  curl -s https://raw.githubusercontent.com/posit-conf-2024/olympicdash/main/olympicdash-r-3-answers.qmd \
    | grep -A5 -B5 "scss\|theme\|navbar\|card"

Also fetch the SCSS file if it exists in a style/ folder:

  curl -s https://raw.githubusercontent.com/posit-conf-2024/olympicdash/main/style/custom.scss 2>/dev/null || \
  curl -s https://raw.githubusercontent.com/posit-conf-2024/olympicdash/main/theme.scss 2>/dev/null || \
  echo "No SCSS file found at expected paths"

---

## Source 3: Current dashboard state

Read the current SCSS and QMD to understand what exists:

  cat assets/dashboard-theme.scss
  grep -n "theme_dark_dash\|theme_void\|plot.background\|fill.*#\|color.*#" \
    FinalDashboard/Dashboard/Final_Project_Template.qmd | head -30

---

## Output: Complete Design Spec

After fetching all sources, produce this exact output document
(Agent 2 reads this and implements it — no decisions needed):

  ═══════════════════════════════════════════════════════
  DESIGN SPEC — PAF 516 Dashboard
  ═══════════════════════════════════════════════════════

  BASE BOOTSWATCH THEME: flatly
  (Clean professional light theme — not darkly)

  FONT: Lato (Google Fonts)
  Import URL: https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap
  $font-family-sans-serif: 'Lato', sans-serif

  COLORS (from urbnthemes):
    $urbn-cyan:     [extracted hex]   ← primary accent
    $urbn-gray:     [extracted hex]   ← neutral
    $urbn-yellow:   [extracted hex]   ← secondary
    $urbn-magenta:  [extracted hex]   ← tertiary
    $urbn-green:    [extracted hex]
    $urbn-red:      [extracted hex]
    $urbn-spacegray:[extracted hex]
    $urbn-black:    #000000

  NAVBAR:
    background: #1a365d  (deep navy — policy authority)
    foreground: #ffffff
    bottom border: 3px solid [urbn-cyan]
    brand font-weight: 700

  CARDS:
    background: #ffffff
    border: 1px solid #e3e3e3
    border-radius: 4px
    box-shadow: 0 1px 4px rgba(0,0,0,0.06)

  CARD HEADERS:
    background: #ffffff
    border-bottom: 1px solid #e3e3e3
    border-left: 4px solid [urbn-cyan]
    font: Lato 700, 0.72rem, uppercase, letter-spacing 0.08em
    color: #555555
    padding-left: 0.65rem (to account for left border)

  VALUE BOXES (semantic mapping to policy meaning):
    danger   → [urbn-red]      (hot spots, worsening — alarm)
    primary  → #1a365d         (navy — authority/context)
    success  → [urbn-green]    (improving — positive)
    warning  → [urbn-yellow]   (caution — watch areas)
    secondary→ [urbn-gray]     (neutral stats)

  VALUE BOX TYPOGRAPHY:
    .value-box-value: Lato 900, 1.9rem
    .value-box-title: Lato 700, 0.65rem, uppercase, letter-spacing 0.09em

  TABLES:
    font-size: 0.82rem
    thead background: #f5f5f5
    thead border-bottom: 2px solid [urbn-cyan]
    thead font: Lato 700, 0.7rem, uppercase
    tbody hover: rgba([urbn-cyan], 0.06)
    striped: rgba(0,0,0,0.02)

  TAB NAV:
    .active background: #1a365d
    .active color: #ffffff
    font: 0.83rem, Lato

  GGPLOT THEME (theme_urbn_dash):
    plot.background:  #ffffff
    panel.background: #ffffff
    plot.title:       Lato 700, 13px, #333333
    plot.subtitle:    Lato 400, 11px, #767676
    plot.caption:     Lato 400, 9px, #767676, hjust=0
    legend.background: #ffffff
    legend.key: #ffffff
    legend.text: 11px, #333333
    legend.title: 11px, #767676
    plot.margin: margin(8,8,8,8)

  GGPLOT DIVERGING MAP MIDPOINT COLOR:
    mid = "#f5f5f5"  (light grey, visible against white card bg)
    low = [urbn-cyan-dark]  e.g. "#0a4c6a" (improved)
    high = [urbn-red]       (worsened)

  MAPGL: REMOVED — replaced with static ggplot shift_geometry()
  (Already done in previous fix — confirm mapgl not in file)

  ═══════════════════════════════════════════════════════

Print the complete spec with actual hex values filled in.
Agent 2 reads this output and implements it.
