# Agent 3 — Policy Brief + Dashboard Fixes

Two tasks:
  A. Apply all CRITICAL + WARNING fixes from Agent 2 to the dashboard
  B. Build FinalDashboard/Dashboard/Policy_Brief_Template.qmd

---

## TASK A: Apply Agent 2 fixes to dashboard

For every issue in Agent 2's report, fix it in:
  FinalDashboard/Dashboard/Final_Project_Template.qmd

After all fixes, re-run Agent 2's grep checks to confirm clean.
Re-render to confirm it still renders.

---

## TASK B: Build Policy Brief

Policy brief = short professional document: 1-2 pages when rendered.
Three pre-filled figures. Three TODO recommendation callouts.
Students write only the TODO sections.

### File: FinalDashboard/Dashboard/Policy_Brief_Template.qmd

### YAML
```yaml
---
title: "Economic Hardship in `r TARGET_LABEL`"
subtitle: "A Policy Brief"
author: "[Your Name]"
date: today
format:
  html:
    theme: readable
    toc: false
    code-fold: true
    code-summary: "Show code"
    self-contained: true
    number-sections: false
execute:
  echo: false
  warning: false
  message: false
---
```

### Before you begin callout
```
::: {.callout-important}
## Before You Begin
1. **Rename** this file `Policy_Brief_YourLastName.qmd`.
2. **Update the county block** (TARGET_STATE, TARGET_COUNTY, TARGET_LABEL).
   This controls all data pulls and figure titles — no other code changes needed.
3. **Knit the file** to see your county's results.
4. **Write your answers** in each [Your answer here] section.
5. **Submit** both `.qmd` and `.html` to Canvas.
:::
```

### Packages (same renv pattern)

### County parameter block (identical to dashboard)
```r
#| label: county-config
TARGET_STATE  <- "AZ"
TARGET_COUNTY <- "Maricopa"
TARGET_LABEL  <- "Maricopa County, AZ"
```

### Index variables + build_hardship_index() (identical to dashboard)

### Data pulls
  - Local tracts 2023 (current state) — for LISA
  - Local tracts 2013, 2019 (temporal) — for trajectories
  - Local tracts 2016 (three-point) — for trend

### Analysis
  - LISA on 2019 index (same pattern as dashboard)
  - Pooled standardization and trajectories (same as dashboard)

### Document body

```
::: {.callout-note}
## Executive Summary
**[Your answer here — 3-4 sentences]**
Name the county. State hardship level. Describe the spatial pattern.
State your top recommendation.
:::

## Background

[2 short pre-filled paragraphs about the analytical context —
written for Maricopa County, with a TODO note for students to
update for their county. Reference the post-recession recovery
window (2013–2019), the three-variable index, and what spatial
clustering means for policy.]

# Key Findings

## Finding 1 — Where Is Hardship Concentrated?

[Pre-filled LISA cluster map — same styling as Tab 3 of dashboard]
[fig-width: 8, fig-height: 6]

**[Your answer here — 1 paragraph]**
How many hot spot tracts? Where are they located? What does the
Moran's I statistic tell you about the degree of spatial clustering?
Reference specific numbers from the map.

*YOUR ANSWER HERE*

---

## Finding 2 — Which Neighborhoods Are Getting Worse?

[Pre-filled trajectory map — same styling as Tab 4 of dashboard]
[fig-width: 8, fig-height: 6]

**[Your answer here — 1 paragraph]**
What share of tracts are persistent vs. emerging vs. dissolving hot spots?
Where are emerging hot spots located? What does the pattern suggest
about the direction of change in your county?

*YOUR ANSWER HERE*

---

## Finding 3 — The Hardship Profile

[Pre-filled bar chart: mean hardship_2019 by trajectory type, horizontal,
colored with traj_colors, sorted by mean hardship descending]
[fig-width: 7, fig-height: 4]

**[Your answer here — 1 paragraph]**
Which trajectory type has the highest average hardship level?
How do persistent hot spots compare to dissolving ones?
What does this tell you about the pace of recovery?

*YOUR ANSWER HERE*

---

# Recommendations

::: {.callout-tip}
## Recommendation 1 — [TODO: Add a specific policy title]
**[Your answer here — 2-3 sentences]**
Ground in Finding 1 (spatial concentration). Name a specific intervention
type and how many tracts it would target. Name a responsible entity.
:::

::: {.callout-tip}
## Recommendation 2 — [TODO: Add a specific policy title]
**[Your answer here — 2-3 sentences]**
Ground in Finding 2 (trajectories). Focus on emerging hot spots
(early intervention) or dissolving hot spots (displacement risk).
Reference the displacement paradox from Module 5.
:::

::: {.callout-tip}
## Recommendation 3 — [TODO: Add a specific policy title]
**[Your answer here — 2-3 sentences]**
Ground in Finding 3 (hardship profile). Make a data-monitoring
recommendation — what should policymakers track, how often, and why?
:::

---

# Limitations

[Pre-filled — students do not modify this section]

This analysis relies on ACS 5-year estimates, which carry margins of
error that can be substantial at the census tract level. The temporal
comparison (2013–2019) reflects the post-recession recovery decade and
does not capture COVID-era disruptions. Most importantly: a declining
hardship index in a tract may reflect genuine improvement for existing
residents — or it may reflect displacement, with lower-income households
replaced by higher-income newcomers. Census aggregate statistics cannot
distinguish these processes. This analysis identifies candidate
intervention areas; on-the-ground verification is essential before
resource allocation decisions are made.
```

---

## After writing both files

### Render both:
  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Template.qmd --quiet 2>&1 | tail -8
  echo "Dashboard: exit $?"

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Policy_Brief_Template.qmd --quiet 2>&1 | tail -8
  echo "Policy brief: exit $?"
  cd ../..

### Verify:
  grep -c "B15003_002\|crosstalk\|year.*2015\|SharedData" \
    FinalDashboard/Dashboard/Final_Project_Template.qmd \
    FinalDashboard/Dashboard/Policy_Brief_Template.qmd
  (expect: 0 for each)

  ls -lh FinalDashboard/Dashboard/*.html
  ls FinalDashboard/Dashboard/ | grep _files && echo "FAIL — _files found" || echo "PASS"

### Report render status, file sizes, any remaining issues
⛔ STOP — wait for human approval before Agent 4
