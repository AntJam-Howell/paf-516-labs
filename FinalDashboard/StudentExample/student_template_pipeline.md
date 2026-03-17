# PAF 516 Student Template Pipeline — Full Context & Multi-Agent Workflow

## PROJECT CONTEXT — READ FIRST

### What this project is
PAF 516: Community Analytics (ASU) final project dashboard. Students pick
any large US metro county, change 3 lines of R code, render the dashboard,
and write policy recommendations. Everything else auto-computes.

### Deprecated files — DO NOT TOUCH
The following files are deprecated and should be ignored entirely:
  FinalDashboard/StudentExample/Final_Project_SanDiego.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego.html
  FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.html
  FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego.html
  FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.html

These were hand-coded for San Diego and are replaced by the new
location-agnostic student template.

### The ONE file that matters
  FinalDashboard/StudentExample/Final_Project_Template_student.qmd

This is the student-facing template. A student changes ONLY these
3 lines in the county-config chunk:

  TARGET_STATE  <- "CA"
  TARGET_COUNTY <- "Los Angeles"
  TARGET_LABEL  <- "Los Angeles County, CA"

Nothing else should require student modification. All data pulls,
maps, statistics, and visualizations must update automatically.

### The design contract
- ONLY pull-national has cache: true (3,100 US counties, location-independent)
- Every other data chunk: NO cache directive whatsoever
- Every geographic reference must derive from TARGET_STATE/TARGET_COUNTY
- No hardcoded state names ("Arizona"), county names ("Maricopa"), or
  coordinate bounds — all must be computed dynamically
- Tab titles use static strings (not !expr) — dynamic labels go inside
  R plot/table code, not in YAML chunk options
- embed-resources: true in YAML — fully self-contained HTML, no external files
- dplyr::select() everywhere — MASS package masks base select()

### Dashboard structure (4 tabs)
1. National Context — US county choropleth (mapgl) + state county table +
   dot plot comparing state counties vs US extremes
2. State in Focus — state tract EHI choropleth (mapgl) + poverty/unemp
   scatter + state LISA map + county heterogeneity table + value boxes
3. County Clusters & Trajectories — Sankey (EHI mobility 2013→2023) +
   trajectory map (mapgl) + value boxes
4. Policy Implications — 3 auto-stats cards (red/yellow/green) +
   3 student recommendation cards (TODO placeholders)

### EHI methodology
3-variable pooled z-score:
  poverty_rate = (C17002_002 + C17002_003) / C17002_001
  unemp_rate   = B23025_005 / B23025_002
  median_income = B19013_001 (reversed: multiplied by -1)
  EHI = rowMeans(z_poverty, z_unemp, z_income_reversed)
  Higher EHI = worse off. Temporal: pooled standardization 2013+2019.

---

## PIPELINE: 6 AGENTS + VERIFICATION LOOP

Run all agents in sequence. If any agent fails or flags CRITICAL issues,
the pipeline loops back to the implementation agent before proceeding.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/
Target file: FinalDashboard/StudentExample/Final_Project_Template_student.qmd

---

## AGENT 1 — Audit: Dynamic Update Completeness

Read Final_Project_Template_student.qmd in full.

Your job: find every place in the file where a specific state, county,
geography, or hardcoded value appears that should instead derive from
TARGET_STATE, TARGET_COUNTY, or TARGET_LABEL.

Check every chunk for:

### Data pull issues
- Any get_acs() call missing state = TARGET_STATE or county = TARGET_COUNTY
- Any filter like filter(str_detect(NAME, "Arizona")) instead of
  filter(str_detect(NAME, state_full)) or filter(str_detect(NAME, TARGET_COUNTY))
- Any str_remove(NAME, "County, Arizona") instead of
  str_remove(NAME, paste0("County, ", state_full))
- Any hardcoded year that contradicts the EHI methodology

### Geographic bounds issues
- Any maplibre() call with hardcoded numeric bounds like
  c(-115.0, 31.0, -108.5, 37.5) that only fit Arizona
  These must be replaced with dynamic bounds computed from st_bbox()
  on the actual loaded data
- bounds for the national map c(-125.0, 24.0, -66.0, 50.0) is OK
  (that's CONUS and is always correct)

### Caching issues
- Any chunk other than pull-national that has #| cache: true
  These must be removed

### String/label issues
- Any user-visible string containing "Arizona", "Maricopa", "AZ" that
  should be dynamic
- Any !expr in chunk title options (these cause YAML errors)

### select() masking issues
- Any select() call not qualified as dplyr::select()
  (MASS package masks dplyr's select)

### State name derivation
- Confirm state_full <- state.name[match(TARGET_STATE, state.abb)]
  is defined BEFORE it is used anywhere
- Confirm all county filters use state_full not a hardcoded state name

Report format:
  AGENT 1 — DYNAMIC UPDATE AUDIT
  CRITICAL: [items that will definitely break for non-AZ counties]
  WARN:     [items that may work but are fragile]
  PASS:     [confirmed correct]

---

## AGENT 2 — Independent Assessment: Statistical & Pedagogical Correctness

Read Final_Project_Template_student.qmd in full independently.

Your job: assess whether the dashboard correctly implements the EHI
methodology and tells a coherent analytical story for ANY county.

Check:

### EHI computation
- Does build_hardship_index() correctly compute all 3 components?
- Is the z-score standardization applied correctly (income reversed)?
- For temporal analysis: is pooling across 2013+2019 done correctly?
- Does apply_pooled_z() use the same pooled_stats for both years?

### LISA analysis
- AZ-wide LISA (lisa-az chunk): runs on az_valid, uses w_az — correct
- Maricopa LISA (lisa-analysis chunk): runs on change_df, uses w — correct
- Are there separate LISA objects for state-level vs county-level? Good.
- Are trajectory labels (Persistent HH, Emerging HH etc.) consistent
  with the color palette in traj_colors?

### Sankey diagram
- Does it use actual 2013 and 2023 data (not 2013 and 2019)?
- Does it join correctly on GEOID?
- Are quintile labels sensible?

### Policy tab
- Do the inline R values (n_persist_hh, pct_improved_23, etc.) all
  exist in scope when the Policy tab renders?
- Is pct_persist_hh_23 computed from maricopa_change_23 (which uses
  2013 and 2023 data) — not from the 2013→2019 trajectory analysis?

### Pedagogical coherence
- Does the dashboard tell a clear national → state → county → action story?
- Are value box titles written in plain English (not R variable names)?
- Do TODO placeholders give students enough guidance to write 3+ sentences?

Report format:
  AGENT 2 — STATISTICAL & PEDAGOGICAL ASSESSMENT
  CRITICAL: [methodology errors or broken inline R]
  WARN:     [potential confusion or weak pedagogy]
  PASS:     [confirmed correct]

---

## AGENT 3 — Evaluator: Consolidated Decision

Read both Agent 1 and Agent 2 reports.

Produce:

### MUST FIX (any CRITICAL from either agent, or 2+ WARNs on same issue):
  [numbered list — each item must name exact file location and fix]

### SHOULD FIX (single WARNs worth addressing):
  [numbered list]

### DO NOT FIX (low risk, cosmetic, or contradictory advice):
  [with reasoning]

### FINAL ACTION LIST FOR AGENT 4:
  Numbered, specific, implementable. For each item:
  - Which chunk/line
  - What to change
  - What the correct code should be

---

## AGENT 4 — Orchestrator & Implementation

Read Agent 3's FINAL ACTION LIST.

Implement every MUST FIX item using targeted str_replace edits.
Do NOT rewrite whole chunks unless the chunk is entirely broken.

After all edits, run a self-check:

  echo "=== Banned patterns check ==="
  grep -n "\"Arizona\"\|\"Maricopa\"\|\"AZ\"\|cache: true\|115\.0.*31\.0\|108\.5.*37\.5" \
    FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
    | grep -v "county-config\|TARGET_STATE\|TARGET_COUNTY\|Examples\|#"
  echo "=== select() without dplyr:: ==="
  grep -n "[^:]select(" \
    FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
    | grep -v "dplyr::select\|DT::datatable\|#"
  echo "=== !expr in chunk options ==="
  grep -n "!expr" \
    FinalDashboard/StudentExample/Final_Project_Template_student.qmd

If any banned patterns remain, fix them before rendering.

---

## AGENT 5 — Critical Data Analyst: Pre-Render Validation

Before rendering, validate the logic of the most failure-prone sections
by reading the QMD and mentally tracing through with TARGET_STATE="CA",
TARGET_COUNTY="Los Angeles".

Trace through these specific code paths:

### Path 1: state_full derivation
  state_full <- state.name[match("CA", state.abb)]
  Expected: "California"
  Check: is state_full defined before first use?

### Path 2: state_counties filter
  county_2023 %>% filter(str_detect(NAME, "California"))
  Expected: ~58 rows (CA counties named "X County, California")
  Check: does the regex match the actual tidycensus NAME format?

### Path 3: compare_df state_all filter
  county_2023 %>% filter(str_detect(NAME, "California"))
  Expected: 58 CA counties in the dot plot

### Path 4: az_county_hetero_tbl
  county_name_lookup uses county_2023 filtered to California
  az_tract_2023 (which is now CA tracts) joined to lookup by substr(GEOID,1,5)
  Expected: ~58 counties each with N tracts

### Path 5: target_boundary
  az_tract_2023 %>% filter(str_detect(NAME, "Los Angeles"))
  Expected: ~2,300 LA County tracts → unioned to one polygon

### Path 6: map_bounds
  st_bbox(az_map) on California tracts
  Expected: roughly xmin=-124, ymin=32, xmax=-114, ymax=42

### Path 7: scatter_df county join
  mutate(county_geoid = substr(GEOID, 1, 5))
  left_join(county_name_lookup_scatter, by="county_geoid")
  Expected: all CA tracts with correct county_name

For each path, report PASS or FAIL with the specific issue.
If any FAIL, report exact fix to Agent 4 for immediate correction
before rendering proceeds.

---

## RENDER & VERIFY

After Agent 5 signs off, render with TARGET_STATE="CA":

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
    cut -d= -f2 | tr -d '"')
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
    2>&1 | tee /tmp/render_log.txt | tail -30

  echo "Exit code: $?"
  ls -lh FinalDashboard/StudentExample/Final_Project_Template_student.html

If render fails: Agent 4 fixes error inline, re-render. Loop until clean.

---

## AGENT 6A — Verification: Content Correctness

Read /tmp/render_log.txt and the rendered HTML file.

Verify for TARGET_STATE="CA", TARGET_COUNTY="Los Angeles":

1. National Context tab
   - Does the map show CONUS? Is California yellow-outlined?
   - Does the state county table show California counties (not Arizona)?
   - Is Los Angeles correctly labeled "← your county" and highlighted?
   - Does the dot plot show California counties (labeled ", CA")?

2. State in Focus tab
   - Do both maps show California census tracts (not Arizona)?
   - Is Los Angeles County outlined in yellow on both maps?
   - Does the county table show California counties?
   - Do value boxes show California statewide LISA counts?

3. County Clusters & Trajectories tab
   - Does the Sankey show Los Angeles tract movement (not Maricopa)?
   - Does the trajectory map show Los Angeles County tracts?
   - Do value boxes reference LA County statistics?

4. Policy Implications tab
   - Do the auto-computed stats (n_persist_hh, pct_improved_23, etc.)
     look plausible for a large urban county like LA?
   - Are the TODO placeholders intact (not pre-filled)?

Report: PASS / FAIL per item. Any FAIL → back to Agent 4.

---

## AGENT 6B — Verification: Location-Agnostic Integrity

Modify the county-config in the QMD temporarily:
  TARGET_STATE  <- "TX"
  TARGET_COUNTY <- "Harris"
  TARGET_LABEL  <- "Harris County, TX"

Re-render:
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
    2>&1 | tail -10
  echo "Harris exit: $?"

Verify:
  - State table shows Texas counties
  - Maps show Texas tracts with Harris County outlined in yellow
  - Dot plot shows TX counties
  - No errors, no blank panels

Report: PASS or FAIL with specific issues.

If PASS on both CA and TX: proceed to final commit.
If FAIL: Agent 4 fixes, re-run both verifications.

---

## FINAL COMMIT

Set county-config back to Maricopa defaults:
  TARGET_STATE  <- "AZ"
  TARGET_COUNTY <- "Maricopa"
  TARGET_LABEL  <- "Maricopa County, AZ"

Render final Maricopa version:
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
    2>&1 | tail -10

Clean up and commit:
  rm -rf FinalDashboard/StudentExample/*_files/
  rm -rf FinalDashboard/StudentExample/*_cache/
  git add FinalDashboard/StudentExample/Final_Project_Template_student.qmd \
          FinalDashboard/StudentExample/Final_Project_Template_student.html
  git -c trailer.ifexists=doNothing commit -m \
    "Student template: location-agnostic pipeline verified CA + TX + AZ"
  git push

  echo "Pipeline complete."
  git log --oneline -3
