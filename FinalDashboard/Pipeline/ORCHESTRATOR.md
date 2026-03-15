# FinalDashboard Orchestrator — PAF 516

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

This orchestrator builds all Final Project materials in a new FinalDashboard/
folder, completely independent of the existing Lab7/ and Module7/ directories.
Do NOT touch Lab7/ or Module7/ — they will be compressed separately.

---

## Folder structure to create

  FinalDashboard/
    Dashboard/
      Final_Project_Template.qmd      ← parameterized, Maricopa default, answers BLANK
      Final_Project_Template.html     ← rendered Maricopa blank (student reference)
      Final_Project_Complete.qmd      ← same code, Phoenix answers COMPLETED
      Final_Project_Complete.html     ← rendered Phoenix with full answers
      Policy_Brief_Template.qmd       ← parameterized, Maricopa default, answers BLANK
      Policy_Brief_Template.html      ← rendered Maricopa blank
      Policy_Brief_Complete.qmd       ← Phoenix answers COMPLETED
      Policy_Brief_Complete.html      ← rendered completed policy brief
    NoAPI/
      Final_Project_Template_NoAPI.qmd    ← Maricopa, get_acs → readRDS(url(GitHub))
      Final_Project_Template_NoAPI.html   ← rendered
      Policy_Brief_Template_NoAPI.qmd
      Policy_Brief_Template_NoAPI.html
      data/
        county_2023_RAW.rds
        maricopa_local_2023_RAW.rds
        maricopa_tract_2013_RAW.rds
        maricopa_tract_2019_RAW.rds
        maricopa_tract_2016_RAW.rds
    StudentExample/
      Final_Project_SanDiego.qmd      ← San Diego, code complete, answers BLANK
      Final_Project_SanDiego.html     ← rendered San Diego
      Policy_Brief_SanDiego.qmd
      Policy_Brief_SanDiego.html
      data/
        sandiego_county_2023_RAW.rds
        sandiego_local_2023_RAW.rds
        sandiego_tract_2013_RAW.rds
        sandiego_tract_2019_RAW.rds
        sandiego_tract_2016_RAW.rds
    Pipeline/
      ORCHESTRATOR.md      ← this file
      agent1_build.md
      agent2_review.md
      agent3_brief.md
      agent4_sandiego.md
      agent5_answers.md
      agent5a_draft.md
      agent5b_critique.md
      agent5c_revise.md
      agent5d_verify.md

---

## Student workflow (what this produces)

STANDARD PATH (has Census API):
  1. Download Final_Project_Template.qmd
  2. Change TARGET_STATE, TARGET_COUNTY, TARGET_LABEL (3 lines)
  3. Render → full dashboard for their chosen metro
  4. Write 3 policy recommendations in the TODO cards
  5. Submit .qmd + .html

API TROUBLE PATH:
  1. Instructor sends Final_Project_SanDiego.qmd + StudentExample/data/ folder
  2. Student opens it — all code runs from local data/, no API calls
  3. Student writes 3 policy recommendations (code is done, analysis is done)
  4. Submit .qmd + .html

INSTRUCTOR REFERENCE:
  Final_Project_Complete.html — Phoenix model answer (students see this to understand
  what a completed dashboard looks like before writing their own)

---

## Execution order

  STEP 1 → mkdir all folders
  STEP 2 → Execute Pipeline/agent1_build.md
           ⛔ STOP — report + wait for human approval
  STEP 3 → Execute Pipeline/agent2_review.md
           ⛔ STOP — report all issues + wait for human approval
  STEP 4 → Execute Pipeline/agent3_brief.md (fixes + policy brief)
           ⛔ STOP — report + wait for human approval
  STEP 5 → Execute Pipeline/agent4_sandiego.md (auto after Agent 3 approved)
  STEP 6 → Execute Pipeline/agent5_answers.md (Phoenix answer pipeline)
           Uses sub-agents: agent5a → agent5b → agent5c → agent5d
           ⛔ FINAL STOP — human approves before any commit
  STEP 7 → Update docs/ landing page + Module7 guide (instructions at bottom)
  STEP 8 → Commit everything

---

## Non-negotiable rules (every agent enforces these)

### Index: 3 variables only
  poverty_rate  = (C17002_002 + C17002_003) / C17002_001
  unemp_rate    = B23025_005 / B23025_002
  median_income = B19013_001  (reversed: z-score × -1)
  hardship_index = rowMeans(z_pov, z_unemp, z_inc_reversed)
  BANNED: B15003_002, B27010_017, psych::alpha(), Cronbach

### Years
  Current state:   year = 2023
  Temporal change: year = 2013 and year = 2019
  Three-point:     year = 2016
  BANNED: year = 2015 anywhere

### mapgl
  mapgl ONLY on the National Context tab
  All other maps: static ggplot + geom_sf
  Every maplibre() MUST have bounds = st_bbox(data_object)
  All sf → st_transform(4326) before mapgl
  BANNED: crosstalk, SharedData, leaflet, mapboxgl()

### Dashboard YAML — mandatory
  format:
    dashboard:
      theme:
        - darkly
        - ../../assets/dashboard-theme.scss
      orientation: columns
      embed-resources: true
  execute:
    echo: false
    warning: false
    message: false

### County parameter block — mandatory, first non-setup chunk
  # ── STUDENT: change only these 3 lines, then re-render ──────────────────
  TARGET_STATE  <- "AZ"
  TARGET_COUNTY <- "Maricopa"
  TARGET_LABEL  <- "Maricopa County, AZ"
  # ─────────────────────────────────────────────────────────────────────────
  Every get_acs() uses TARGET_STATE / TARGET_COUNTY.
  Every map title / value box label uses TARGET_LABEL.
  No other code changes required.

### 5 tabs only
  # National Context    ← mapgl interactive
  # Local Hardship      ← two static ggplots
  # Hot Spots           ← LISA static ggplot + table
  # Change & Trajectories ← diverging change + trajectory maps
  # Policy              ← DT table + 3 recommendation cards

### Git
  git -c trailer.ifexists=doNothing commit -m "message"
  NEVER Co-authored-by. Only Agent 5d commits.

---

## Landing page + guide updates (execute after Agent 5d commit)

### docs/index.html — Final Project box
Update the 4 button links to:
  View Example    → FinalDashboard/Dashboard/Final_Project_Complete.html
  Download Template → raw GitHub URL to FinalDashboard/Dashboard/Final_Project_Template.qmd
  Policy Brief    → raw GitHub URL to FinalDashboard/Dashboard/Policy_Brief_Template.qmd
  Instructions    → FinalDashboard/Dashboard/ (or a landing page)

### docs/final-project.html — CREATE NEW plain HTML landing page
Same style as lab1-tutorial.html etc. Content:
  - Title: "Final Project | PAF 516"
  - Brief description of the two deliverables
  - 4 download/view buttons
  - Submission instructions summary

### Module7/Module7_Guide.qmd — targeted patches only
  - Tab count: 5 tabs (not 5 pages)
  - Remove crosstalk references
  - Update grading rubric to match new structure
  - Add trajectory analysis to synthesis section
  - Update Lab 07 download link to FinalDashboard path
  - Re-render and copy to docs/Module7_Guide.html

### Commit landing page + guide updates separately:
  git add docs/ Module7/
  git -c trailer.ifexists=doNothing commit -m \
    "Update landing page and Module7 guide to point to FinalDashboard"
  git push
