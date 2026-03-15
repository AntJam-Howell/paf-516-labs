# Agent 2 — Adversarial Review

Read FinalDashboard/Dashboard/Final_Project_Template.qmd.
Find every problem. Be exhaustive. Do NOT fix anything — only report.
Agent 3 applies fixes.

---

## Checks to run

### A. Rules compliance (run grep for each)
  grep -n "B15003_002"         Final_Project_Template.qmd  # expect: nothing
  grep -n "psych::alpha"       Final_Project_Template.qmd  # expect: nothing
  grep -n "crosstalk"          Final_Project_Template.qmd  # expect: nothing
  grep -n "SharedData"         Final_Project_Template.qmd  # expect: nothing
  grep -n "leaflet"            Final_Project_Template.qmd  # expect: nothing
  grep -n "year.*=.*2015"      Final_Project_Template.qmd  # expect: nothing
  grep -n "mapboxgl"           Final_Project_Template.qmd  # expect: nothing
  grep -n "maplibre\|add_fill" Final_Project_Template.qmd  # expect: ONLY inside National Context tab

### B. Index correctness
  Trace the build_hardship_index() function:
  - Does it compute poverty_rate = (C17002_002 + C17002_003) / C17002_001? ✓/✗
  - Does it compute unemp_rate = B23025_005 / B23025_002? ✓/✗
  - Does it reverse-code median_income (multiply z by -1)? ✓/✗
  - Does it use rowMeans of exactly 3 z-scores? ✓/✗
  - Does it handle sf geometry correctly (preserve before drop, restore after)? ✓/✗

### C. Pooled standardization
  Trace the pooled_stats and apply_pooled_z() pattern:
  - Are both r2013 and r2019 used to compute pooled mean/SD? ✓/✗
  - Does apply_pooled_z() reverse-code z_median_income? ✓/✗
  - Does change_df = hardship_2019 - hardship_2013 (not reversed)? ✓/✗
  - Is winsorization applied before change_plot? ✓/✗

### D. Trajectory classification
  Check every case_when label against the Lab 6 canonical list:
  - Persistent HH: lisa_2013=="HH" & lisa_2019=="HH" ✓/✗
  - Emerging HH:   lisa_2013!="HH" & lisa_2019=="HH" ✓/✗
  - Dissolving HH: lisa_2013=="HH" & lisa_2019!="HH" ✓/✗
  - Persistent LL: lisa_2013=="LL" & lisa_2019=="LL" ✓/✗
  - Emerging LL:   lisa_2013!="LL" & lisa_2019=="LL" ✓/✗
  - HL Outlier:    lisa_2013=="HL" | lisa_2019=="HL" ✓/✗
  - Stable NS:     TRUE (catch-all) ✓/✗

  Check V-shaped trend label:
  - hardship_2013 > hardship_2016 & hardship_2016 < hardship_2019
    should be "V-shaped (improved mid)" — 2016 is the TROUGH ✓/✗
  - hardship_2013 < hardship_2016 & hardship_2016 > hardship_2019
    should be "Inverted-V (worsened mid)" — 2016 is the PEAK ✓/✗

### E. mapgl compliance
  - Is maplibre() called ONLY inside the # National Context section? ✓/✗
  - Does every maplibre() have bounds = st_bbox(...)? ✓/✗
  - Is county data transformed to 4326 before maplibre? ✓/✗

### F. Tab count and naming
  Count all level-1 headings that are actual tabs (not inside code blocks):
  Expected exactly 5: National Context, Local Hardship, Hot Spots,
  Change & Trajectories, Policy ✓/✗

### G. County parameter
  - Is the TARGET_* block present as the FIRST non-setup R chunk? ✓/✗
  - Does every get_acs() use TARGET_STATE / TARGET_COUNTY? ✓/✗
  - Is any county name hardcoded in R code (not in TARGET_LABEL)? ✓/✗
    grep -n '"Maricopa"\|"Arizona"\|"AZ"' Final_Project_Template.qmd
    — only the TARGET_* chunk should contain these

### H. YAML
  - embed-resources: true? ✓/✗
  - echo: false? ✓/✗
  - warning: false? ✓/✗
  - theme includes ../../assets/dashboard-theme.scss? ✓/✗

### I. Student experience
  - Are there exactly 3 recommendation TODO cards on the Policy tab? ✓/✗
  - Does each card have a *[Your answer here]* placeholder? ✓/✗
  - Are all chunk labels present (#| label:)? ✓/✗
  - Are at least 5 example counties listed in the county-config comment? ✓/✗

### J. Render artifact check
  - Is FinalDashboard/Dashboard/Final_Project_Template.html present? ✓/✗
  - No _files/ folder? ✓/✗
  - File size < 25 MB? ✓/✗

---

## Report format

  === AGENT 2 REVIEW REPORT ===

  CHECKS PASSED: N/30
  CRITICALS (must fix): N
  WARNINGS (should fix): N

  CRITICAL ISSUES:
  [C1] Check X — description
       Location: line N
       Required fix: exact text of what must change

  WARNING ISSUES:
  [W1] Check Y — description
       Suggested fix: ...

  GREP RESULTS (paste full output):
  ...

  VERDICT: PASS (no criticals) / FAIL (N criticals)

⛔ STOP. Do not modify files. Agent 3 reads this report.
