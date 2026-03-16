# Phase 2 — Dashboard Evaluation (6-Agent Review Loop)

Prerequisite: Phase 1 (aesthetic overhaul) committed and pushed.

Read FinalDashboard/Dashboard/Final_Project_Complete.html directly
from the filesystem. Do NOT attempt to fetch a live URL.
The HTML on disk is the authoritative version.

Run all 6 agents in sequence without stopping.

---

## EVAL AGENT A — Content & Data Fidelity

Read Final_Project_Complete.html. Evaluate these specific items:

### National Context tab
- Does the US choropleth show all 50 states + DC with AK/HI as insets?
- Is Maricopa County identifiable on the map?
- Does the national rank value box show a plausible rank for a large
  Sun Belt county (e.g. somewhere between #500-#2500 of ~3100)?
- Is the "Highest Hardship County" a US county (not Puerto Rico)?
- Does the table show real county names with state abbreviations?

### Local Hardship tab
- Do both maps (hardship choropleth + bivariate hardship×renter) render?
- Is the bivariate legend visible and readable?
- Do the maps show Maricopa County census tracts with visible variation?

### Hot Spots tab
- Does the LISA map show colored HH/LL/HL/LH clusters (not all grey)?
- Are the value box counts plausible (e.g. 5-80 HH hot spots)?
- Does the cluster table have rows with GEOID, cluster type, hardship?

### Change & Trajectories tab
- Does the trajectory map show multiple colored trajectory types?
- Does the diverging change map show both blue (improved) and red
  (worsened) tracts — not all one color?
- Do the % improved and % persistent HH value boxes look plausible?

### Policy tab
- Does the priority areas table have rows (Persistent HH + Emerging HH)?
- Are the 3 recommendation cards filled with substantive text
  (not TODO placeholders, not [Your answer here])?
- Do recommendations reference specific numbers and Phoenix geographies?

Report format:
  AGENT A — CONTENT & DATA FIDELITY REPORT
  CRITICAL: [list]
  WARN:     [list]
  INFO:     [list]
  PASS:     [list of items that look correct]

---

## EVAL AGENT B — Visual Design & Typography

Read Final_Project_Complete.html. Evaluate:

1. Navbar: color (#1a365d navy), font weight, tab labels readable?
2. Card headers: left border accent (#1696d2 cyan), uppercase text?
3. Value boxes: do colors match policy meaning (red=hotspots,
   cyan=cold, green=improving, yellow=worsening)?
4. ggplot map backgrounds: white (#ffffff) matching card background?
   No visible dark seam or background mismatch?
5. Font: is Lato loading (check for font-family in CSS)?
6. Table headers: styled with grey background and cyan border?
7. Diverging map: is the midpoint light grey (not pure white that
   disappears into the card)?
8. LISA colors: Urban Institute palette
   (HH=#db2b27, LL=#1696d2, NS=#d2d2d2)?
9. Trajectory colors: does the legend have 7 distinct colors?
10. Overall: does it look like a policy product or a generic Bootstrap
    dark app?

Check by searching the HTML for key signatures:
  grep -c "1696d2" Final_Project_Complete.html  # expect > 10
  grep -c "Lato" Final_Project_Complete.html     # expect > 5
  grep -c "flatly" Final_Project_Complete.html   # expect > 0
  grep -c "darkly" Final_Project_Complete.html   # expect 0

Report format:
  AGENT B — VISUAL DESIGN REPORT
  CRITICAL: [list]
  WARN:     [list]
  PASS:     [list]

---

## EVAL AGENT C — Layout & Usability

Read Final_Project_Complete.html. Evaluate by inspecting the HTML
structure and any embedded CSS/style attributes:

1. Column widths: are map columns ~60% and sidebar ~40%?
2. fig-height values: search for figure dimensions in the HTML.
   Maps should be tall enough (fig-height >= 7 for local maps,
   >= 6 for change maps).
3. Value box text: any values that might be long strings truncating?
   (e.g. county name > 30 chars in a value box)
4. Table pageLength: is it set to show enough rows (8-12)?
5. Tab labels: "National Context", "Local Hardship", "Hot Spots",
   "Change & Trajectories", "Policy" — all 5 present?
6. Bivariate map: does the inset legend have adequate size?
7. National map: is fig-width wide enough to see county variation?
8. Any content that seems cut off or overflowing?
9. Policy tab: are the 3 recommendation cards clearly separated
   and readable?

Search the QMD for specific values:
  grep -n "fig-height\|fig-width\|width=" \
    FinalDashboard/Dashboard/Final_Project_Complete.qmd | head -20

Report format:
  AGENT C — LAYOUT & USABILITY REPORT
  CRITICAL: [list]
  WARN:     [list with specific fix: e.g. "change fig-height: 7 to 9"]
  PASS:     [list]

---

## EVAL AGENT D — Policy Communication

Read Final_Project_Complete.html. Evaluate from the perspective of a
Maricopa County housing official who has never seen this dashboard:

1. Tab narrative: does each tab have explanatory text (not just maps)?
2. Value box labels: do they explain what the number means in plain
   English? (e.g. "Hot Spot Tracts (HH)" is clear; "n_hh" is not)
3. Map titles/subtitles: are they descriptive without jargon?
4. Recommendation 1: does it name a specific Phoenix geography,
   cite a hardship score, and propose a concrete intervention
   with a named entity?
5. Recommendation 2: does it address Emerging HH tracts specifically
   and mention displacement risk?
6. Recommendation 3: does it make a forward-looking argument
   grounded in the temporal evidence?
7. Are any LISA/Moran's I/trajectory terms explained anywhere?
8. Does the dashboard tell a coherent story across the 5 tabs:
   national context → local pattern → clusters → change → action?
9. Is the Limitations section present in the policy brief
   (not in the dashboard — that's correct)?
10. Would a non-expert understand what "pooled z-score
    standardization" means from context?

Report format:
  AGENT D — POLICY COMMUNICATION REPORT
  CRITICAL: [list]
  WARN:     [suggested rewrites where text is unclear/missing]
  PASS:     [list]

---

## EVAL AGENT E — Resolution & Decision

Read all 4 reports (A, B, C, D).

Produce the consolidated action list:

### AGREED FIXES (2+ agents flag it OR any CRITICAL):
Number each fix. Be specific:
  [1] Fix description — exact change required
  [2] ...

### DISPUTED ITEMS:
For each item where agents disagree:
  Item: [description]
  Agent X says: [position]
  Agent Y says: [position]
  Decision: [final call with 1-sentence reasoning]

### DO NOT FIX:
  [item] — reason (too risky / contradictory / low value)

### FINAL ACTION LIST FOR AGENT F:
Numbered, specific, implementable. Each item must name:
  - Which file to edit
  - What exactly to change
  - What the new value should be

---

## EVAL AGENT F — Implementation

Read Agent E's FINAL ACTION LIST. Implement every item.

### Rules
- Use targeted str_replace edits — do NOT rewrite whole files
- Only touch the presentation layer (SCSS, theme function, fig sizes,
  label text, color values) — never touch data analysis code
- If changing fig-height/fig-width, update BOTH Template and Complete
- If changing a color vector (lisa_colors, traj_colors), update
  BOTH Template and Complete
- If changing SCSS, update assets/dashboard-theme.scss only

### After all fixes, render both files:

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
    cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Template.qmd --quiet 2>&1 | tail -5
  echo "Template: exit $?"

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Complete.qmd --quiet 2>&1 | tail -5
  echo "Complete: exit $?"

  cd ../..
  ls -lh FinalDashboard/Dashboard/*.html

### If either render fails:
Fix the error and re-render. Do not proceed to Phase 3 until
both render with exit 0 and both HTML files are < 25 MB.

### Report summary:
Print the complete list of changes made, file by file.
Then print render results and file sizes.
Then proceed automatically to Phase 3.
