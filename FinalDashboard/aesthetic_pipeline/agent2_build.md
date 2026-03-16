# Agent 2 — Build the Theme

Read Agent 1's design spec output carefully.
Implement every value exactly. No creative decisions — just execute.

Scope: ONLY these files:
  assets/dashboard-theme.scss          ← full rewrite
  FinalDashboard/Dashboard/Final_Project_Template.qmd  ← theme function + map colors
  FinalDashboard/Dashboard/Final_Project_Complete.qmd  ← same changes

Do NOT touch any other file.

---

## STEP 1: Rewrite assets/dashboard-theme.scss

Write the complete file from scratch. Structure:

```scss
/*-- scss:defaults --*/

/* ── Fonts ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');
$font-family-sans-serif: 'Lato', -apple-system, BlinkMacSystemFont, sans-serif;

/* ── Core colors from Urban Institute style guide ───────────────── */
/* Primary */
$urbn-cyan:      #1696d2;
$urbn-cyan-dark: #0a4c6a;
/* Neutrals */
$urbn-gray:      #d2d2d2;
$urbn-spacegray: #9d9d9d;
$urbn-black:     #1a1a1a;
/* Accent */
$urbn-yellow:    #fdbf11;
$urbn-magenta:   #ec008b;
$urbn-green:     #55b748;
$urbn-red:       #db2b27;

/* ── Bootstrap overrides ────────────────────────────────────────── */
$body-bg:        #f8f9fa;
$body-color:     #1a1a1a;
$card-bg:        #ffffff;
$navbar-bg:      #1a365d;
$navbar-fg:      #ffffff;
$border-color:   #e3e3e3;

/* ── Valuebox semantic colors (policy-meaningful) ───────────────── */
$valuebox-bg-danger:    #db2b27;   /* hot spots, worsening */
$valuebox-bg-primary:   #1a365d;   /* authority/context */
$valuebox-bg-success:   #55b748;   /* improving */
$valuebox-bg-warning:   #fdbf11;   /* caution */
$valuebox-bg-secondary: #9d9d9d;   /* neutral stats */

/* ── Typography ─────────────────────────────────────────────────── */
$headings-font-weight: 700;
$font-size-base:       0.9rem;

/*-- scss:rules --*/

/* ── Navbar ─────────────────────────────────────────────────────── */
.navbar {
  border-bottom: 3px solid #1696d2;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}
.navbar-brand {
  font-weight: 900;
  font-size: 1.05rem;
  letter-spacing: 0.01em;
}
.navbar-subtitle {
  font-size: 0.78rem;
  opacity: 0.75;
}

/* ── Cards ───────────────────────────────────────────────────────── */
.card {
  border: 1px solid #e3e3e3;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.card-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e3e3e3;
  border-left: 4px solid #1696d2;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: #555555;
  padding: 0.55rem 0.75rem 0.55rem 0.6rem;
}

/* ── Value boxes ────────────────────────────────────────────────── */
.value-box-value {
  font-weight: 900;
  font-size: 1.9rem;
  line-height: 1.15;
}
.value-box-title {
  font-size: 0.63rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  opacity: 0.88;
}
/* Warning box: dark text (yellow bg needs dark text for contrast) */
.bslib-value-box.bg-warning .value-box-value,
.bslib-value-box.bg-warning .value-box-title {
  color: #1a1a1a !important;
}

/* ── Tables ─────────────────────────────────────────────────────── */
.dataTables_wrapper {
  font-size: 0.81rem;
  color: #333333;
}
.dataTables_wrapper thead th {
  background-color: #f5f5f5 !important;
  border-bottom: 2px solid #1696d2 !important;
  font-size: 0.69rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #555555 !important;
}
.dataTables_wrapper tbody tr:nth-child(even) {
  background-color: rgba(0,0,0,0.018);
}
.dataTables_wrapper tbody tr:hover {
  background-color: rgba(22,150,210,0.07) !important;
}
.dataTables_wrapper .dataTables_filter input {
  border: 1px solid #d2d2d2;
  border-radius: 3px;
  padding: 2px 6px;
  font-size: 0.8rem;
}

/* ── Tab navigation ─────────────────────────────────────────────── */
.navbar-nav .nav-link {
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  padding: 0.35rem 0.7rem;
  border-radius: 3px;
  margin: 0 1px;
  transition: background-color 0.12s;
}
.navbar-nav .nav-link.active {
  background-color: rgba(255,255,255,0.18) !important;
  color: #ffffff !important;
  font-weight: 700;
}
.navbar-nav .nav-link:hover:not(.active) {
  background-color: rgba(255,255,255,0.1);
}

/* ── Body padding ───────────────────────────────────────────────── */
.quarto-dashboard .dashboard-fill {
  padding: 0.6rem;
}
```

---

## STEP 2: Update the ggplot theme in both QMDs

In both Template and Complete QMDs, find the `theme_dark_dash` function
and replace it entirely with this `theme_urbn_dash` function:

```r
#| label: plot-theme
# ── Urban Institute-inspired ggplot theme for dashboard maps ──────
theme_urbn_dash <- function(base_size = 11) {
  theme_void(base_size = base_size) +
  theme(
    plot.background   = element_rect(fill = "#ffffff", color = NA),
    panel.background  = element_rect(fill = "#ffffff", color = NA),
    plot.title        = element_text(color = "#333333", size = base_size + 1,
                                     face = "bold", margin = margin(b = 3)),
    plot.subtitle     = element_text(color = "#767676", size = base_size - 1,
                                     margin = margin(b = 6)),
    plot.caption      = element_text(color = "#767676", size = base_size - 2,
                                     hjust = 0, margin = margin(t = 4)),
    legend.background = element_rect(fill = "#ffffff", color = NA),
    legend.key        = element_rect(fill = "#ffffff", color = NA),
    legend.text       = element_text(color = "#333333", size = base_size - 1),
    legend.title      = element_text(color = "#767676", size = base_size - 1),
    plot.margin       = margin(8, 8, 8, 8)
  )
}
```

Then replace ALL occurrences of `theme_dark_dash()` with `theme_urbn_dash()`
throughout both QMDs.

---

## STEP 3: Update map color scales in both QMDs

### Choropleth maps (viridis inferno)
These already work on a light background — keep `option = "inferno"`.
Change `direction = -1` is fine. No change needed.

### Diverging change map
Find the `scale_fill_gradient2` call. Update the midpoint color:

BEFORE:
  scale_fill_gradient2(low="#2C7BB6", mid="white", high="#D7191C", ...)

AFTER:
  scale_fill_gradient2(low="#0a4c6a", mid="#f5f5f5", high="#db2b27",
                       midpoint=0, limits=c(-max_abs, max_abs),
                       name="Hardship\nChange")

The light grey midpoint (#f5f5f5) is visible against white card backgrounds
(unlike pure white which disappears). The low/high colors match Urban Institute
diverging palette.

### LISA cluster map colors
Update the lisa_colors vector to use Urban Institute palette:

BEFORE:
  lisa_colors <- c("HH"="#D7191C","LL"="#2C7BB6","HL"="#FDAE61",
                   "LH"="#ABD9E9","NS"="#CCCCCC")

AFTER:
  lisa_colors <- c("HH"="#db2b27","LL"="#1696d2","HL"="#fdbf11",
                   "LH"="#73bfe2","NS"="#d2d2d2")

### Trajectory colors
Update traj_colors vector:

BEFORE:
  "Persistent HH"="#D7191C", "Emerging HH"="#FDAE61", "Dissolving HH"="#FEE08B",
  "Persistent LL"="#2C7BB6", "Emerging LL"="#ABD9E9", "HL Outlier"="#9E5BB4",
  "Stable NS"="#CCCCCC"

AFTER:
  "Persistent HH"="#db2b27", "Emerging HH"="#fdbf11", "Dissolving HH"="#fdd870",
  "Persistent LL"="#1696d2", "Emerging LL"="#73bfe2", "HL Outlier"="#ec008b",
  "Stable NS"="#d2d2d2"

---

## STEP 4: Update YAML theme in both QMDs

BEFORE:
  theme:
    - darkly
    - ../../assets/dashboard-theme.scss

AFTER:
  theme:
    - flatly
    - ../../assets/dashboard-theme.scss

---

## STEP 5: Render Template only first

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Template.qmd 2>&1 | tail -15
  cd ../..

  # Check size
  ls -lh FinalDashboard/Dashboard/Final_Project_Template.html

  # No _files/ folder
  ls FinalDashboard/Dashboard/ | grep _files && echo "FAIL" || echo "PASS"

---

## STEP 6: Report before touching Complete

Print:
  - Render: PASS/FAIL
  - File size
  - Any errors

⛔ STOP — human reviews rendered template before proceeding to Complete
