# Task 3 — API Render to Generate Missing RDS Files

For any get_acs() chunks that don't yet have matching RDS files,
render the AltLabs QMD with the Census API to produce them.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 3a — Add saveRDS() calls to AltLabs QMDs

For each AltLabs/Lab{N}/Lab{N}_Assignment.qmd:

Read the QMD and identify every get_acs() chunk (using the audit from Task 1).
For each get_acs() chunk where the RDS does NOT already exist in
AltLabs/Lab{N}/data/, insert a saveRDS() call as the LAST line of that chunk.

Naming convention for RDS files:
  <geography>_<coverage>_<year>_<descriptor>.rds

Examples:
  tract_maricopa_2019_hardship_vars.rds
  cbg_maricopa_2019_raw.rds
  tract_az_2013_hardship_vars.rds
  county_us_2023_hardship_index.rds

Insert pattern (last line inside the chunk, before closing backticks):
  saveRDS(<object_name>, "data/<descriptive_name>.rds")

If a get_acs() chunk already has RDS coverage (from Task 2), skip it —
no saveRDS() needed.

After inserting, print a summary:
  Lab 1: 2 saveRDS() calls added (chunks: step.01-pull, step.01-county)
  Lab 2: 1 saveRDS() call added (chunk: step.01-cbg)
  ...

## 3b — Render each AltLabs QMD with Census API

  QUARTO=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto
  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
    cut -d= -f2 | tr -d '"' | tr -d "'")

Render labs sequentially (not parallel — avoids API rate limits):

  for n in 1 2 3 4 5 6; do
    echo "━━━ Rendering AltLabs/Lab${n} (Census API) ━━━"
    cd AltLabs/Lab${n}
    CENSUS_API_KEY=$CENSUS_API_KEY $QUARTO render Lab${n}_Assignment.qmd \
      --quiet 2>&1 | tail -5
    if [ $? -eq 0 ]; then
      echo "Lab${n}: RENDER OK"
    else
      echo "Lab${n}: RENDER FAILED — stopping"
      cd ../..
      exit 1
    fi
    cd ../..
    echo ""
  done

If any lab fails, print the FULL quarto error output for that lab and stop.
Do not attempt to render subsequent labs after a failure.

## 3c — Verify all RDS files were created

  find AltLabs/Lab{1,2,3,4,5,6}/data/ -name "*.rds" | sort

For each lab, cross-check against the get_acs() chunk map from Task 1.
Print a verification table:

  Lab | get_acs() chunks | RDS files in data/ | Missing
  ────┼──────────────────┼────────────────────┼────────
  1   | 3                | 3                  | none
  2   | 2                | 2                  | none
  ...

If any lab has fewer RDS files than get_acs() chunks:
  1. Print which chunk is missing its RDS
  2. Check whether saveRDS() was inserted for that chunk
  3. Check whether the render actually executed that chunk
  4. Do NOT proceed to Task 4 until resolved

## 3d — Quality gate: file size check

Every RDS file should be > 50KB (a near-empty object indicates a failed pull).

  python3 << 'EOF'
  import os, glob
  for rds in sorted(glob.glob("AltLabs/Lab*/data/*.rds")):
      size_kb = os.path.getsize(rds) / 1024
      status = "OK" if size_kb > 50 else "⚠ SMALL — check this file"
      print(f"  {size_kb:6.0f} KB  {rds}  {status}")
  EOF

Flag any file under 50KB for manual inspection before proceeding.

⛔ STOP HERE. Human must review the RDS inventory (3c) and size check (3d)
before Task 4 begins inserting fallback chunks.
