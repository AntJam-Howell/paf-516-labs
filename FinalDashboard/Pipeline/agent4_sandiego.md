# Agent 4 — San Diego Student Simulation + NoAPI Versions

Prerequisite: Agent 3 approved. Both Dashboard + Policy Brief render cleanly.

Two deliverables:
  A. San Diego student versions (StudentExample/) — code complete, answers BLANK
  B. Maricopa NoAPI versions (NoAPI/) — no Census API, data from GitHub

---

## PART A: San Diego Student Example

### A1. Copy templates

  cp FinalDashboard/Dashboard/Final_Project_Template.qmd \
     FinalDashboard/StudentExample/Final_Project_SanDiego.qmd

  cp FinalDashboard/Dashboard/Policy_Brief_Template.qmd \
     FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd

### A2. Update county parameters in BOTH files (ONLY these 3 lines)

  sed -i '' \
    's/TARGET_STATE  <- "AZ"/TARGET_STATE  <- "CA"/' \
    FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd

  sed -i '' \
    's/TARGET_COUNTY <- "Maricopa"/TARGET_COUNTY <- "San Diego"/' \
    FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd

  sed -i '' \
    's/TARGET_LABEL  <- "Maricopa County, AZ"/TARGET_LABEL  <- "San Diego County, CA"/' \
    FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd

  # Verify — should show "San Diego" in both
  grep "TARGET_" FinalDashboard/StudentExample/Final_Project_SanDiego.qmd | head -3

### A3. Render San Diego with live Census API

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/StudentExample

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_SanDiego.qmd 2>&1 | tail -15
  echo "SD dashboard: exit $?"

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Policy_Brief_SanDiego.qmd 2>&1 | tail -10
  echo "SD brief: exit $?"
  cd ../..

If either fails, print the FULL error and STOP — do not proceed.

### A4. Save San Diego RDS files

  Insert temporary saveRDS() after each get_acs() in a temp copy:
  cp FinalDashboard/StudentExample/Final_Project_SanDiego.qmd /tmp/SD_saves.qmd

  After pull-national chunk:
    saveRDS(county_raw, "../../StudentExample/data/sandiego_county_2023_RAW.rds")

  After pull-local-current chunk:
    saveRDS(local_combined_raw, "../../StudentExample/data/sandiego_local_2023_RAW.rds")

  After pull-temporal chunk (after each of the 3 pulls):
    saveRDS(local_2013_raw, "../../StudentExample/data/sandiego_tract_2013_RAW.rds")
    saveRDS(local_2019_raw, "../../StudentExample/data/sandiego_tract_2019_RAW.rds")
    saveRDS(local_2016_raw, "../../StudentExample/data/sandiego_tract_2016_RAW.rds")

  Render temp file to generate RDS:
  cd FinalDashboard/StudentExample
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render /tmp/SD_saves.qmd --quiet 2>&1 | tail -5
  cd ../..

  Verify all 5 RDS files present and > 50 KB:
  python3 -c "
  import os, glob
  for f in sorted(glob.glob('FinalDashboard/StudentExample/data/*.rds')):
      kb = os.path.getsize(f)/1024
      flag = 'OK' if kb > 50 else 'SMALL'
      print(f'  {kb:6.0f} KB  {flag}  {f}')
  "

### A5. Build San Diego NoAPI dashboard

  cp FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
     FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd

  cp FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd \
     FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd

  For each NoAPI file, replace every get_acs() chunk with readRDS(url(...)):
  GitHub URL base:
    https://raw.githubusercontent.com/AntJam-Howell/paf-516-labs/main/FinalDashboard/StudentExample/data/

  Replacements:
    county_raw           → readRDS(url(".../sandiego_county_2023_RAW.rds"))
    local_combined_raw   → readRDS(url(".../sandiego_local_2023_RAW.rds"))
    local_2013_raw       → readRDS(url(".../sandiego_tract_2013_RAW.rds"))
    local_2019_raw       → readRDS(url(".../sandiego_tract_2019_RAW.rds"))
    local_2016_raw       → readRDS(url(".../sandiego_tract_2016_RAW.rds"))

  Update api-key chunk in both:
    # No Census API key required — data loads from GitHub.

  Add info callout after county-config in both:
  ::: {.callout-tip}
  ## Offline Version — San Diego County
  This version loads pre-built data from GitHub. No Census API key needed.
  All analysis is complete. Your task: write the three policy recommendations
  on the Policy tab. Submit your completed .qmd and .html to Canvas.
  :::

  Render both NoAPI files with CENSUS_API_KEY=NONE:
  cd FinalDashboard/StudentExample
  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_SanDiego_NoAPI.qmd --quiet 2>&1 | tail -8
  echo "SD NoAPI dashboard: $?"

  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Policy_Brief_SanDiego_NoAPI.qmd --quiet 2>&1 | tail -5
  echo "SD NoAPI brief: $?"
  cd ../..

---

## PART B: Maricopa NoAPI Versions

### B1. Generate Maricopa RDS files

  cp FinalDashboard/Dashboard/Final_Project_Template.qmd /tmp/MC_saves.qmd

  Insert saveRDS() after each get_acs() in /tmp/MC_saves.qmd:
    county_raw         → saveRDS(county_raw, "../../NoAPI/data/county_2023_RAW.rds")
    local_combined_raw → saveRDS(local_combined_raw, "../../NoAPI/data/maricopa_local_2023_RAW.rds")
    local_2013_raw     → saveRDS(local_2013_raw, "../../NoAPI/data/maricopa_tract_2013_RAW.rds")
    local_2019_raw     → saveRDS(local_2019_raw, "../../NoAPI/data/maricopa_tract_2019_RAW.rds")
    local_2016_raw     → saveRDS(local_2016_raw, "../../NoAPI/data/maricopa_tract_2016_RAW.rds")

  cd FinalDashboard/Dashboard
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render /tmp/MC_saves.qmd --quiet 2>&1 | tail -5
  cd ../..

### B2. Build Maricopa NoAPI dashboard + brief

  Same replacement pattern as San Diego but:
  - Source QMD: FinalDashboard/Dashboard/Final_Project_Template.qmd
  - Output:     FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd
  - GitHub URL base: .../FinalDashboard/NoAPI/data/
  - RDS filenames: county_2023_RAW.rds, maricopa_local_2023_RAW.rds,
                   maricopa_tract_2013_RAW.rds, maricopa_tract_2019_RAW.rds,
                   maricopa_tract_2016_RAW.rds

  Same for policy brief → NoAPI/Policy_Brief_Template_NoAPI.qmd

  Render both with CENSUS_API_KEY=NONE:
  cd FinalDashboard/NoAPI
  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Template_NoAPI.qmd --quiet 2>&1 | tail -5
  echo "MC NoAPI dashboard: $?"

  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Policy_Brief_Template_NoAPI.qmd --quiet 2>&1 | tail -5
  echo "MC NoAPI brief: $?"
  cd ../..

---

## Final size report

  python3 -c "
  import os, glob
  files = sorted(glob.glob('FinalDashboard/**/*.html', recursive=True) +
                 glob.glob('FinalDashboard/**/*.rds',  recursive=True))
  for f in files:
      kb = os.path.getsize(f)/1024
      flag = ' ⚠ LARGE' if kb > 25000 else ''
      print(f'  {kb:7.0f} KB  {f}{flag}')
  "

If any HTML exceeds 25,000 KB, report it and stop before Agent 5.
Agent 4 auto-continues to Agent 5 if all render with exit 0.
