# Phase 3 — Sync, Deploy, Commit

Prerequisite: Phase 2 complete. Both Template and Complete render
cleanly with exit 0 and file sizes < 25 MB.

---

## STEP 1: Identify what changed in Phase 1+2

Collect the exact set of changes that were made to Template and
Complete so you can apply the same changes to the remaining files.

Run:
  git diff --name-only HEAD FinalDashboard/ assets/

This shows which files changed since the last commit. For each
changed file, note what was modified:
  - YAML theme line (darkly → flatly)
  - theme function name (theme_dark_dash → theme_urbn_dash)
  - theme function body (new white background version)
  - lisa_colors vector (new Urban Institute palette)
  - traj_colors vector (new Urban Institute palette)
  - diverging map mid color (#f5f5f5)
  - any fig-height / fig-width changes from Phase 2

---

## STEP 2: Apply same changes to remaining QMDs

Apply every change identified in Step 1 to these files:

  FinalDashboard/Dashboard/Policy_Brief_Template.qmd
  FinalDashboard/Dashboard/Policy_Brief_Complete.qmd
  FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd
  FinalDashboard/NoAPI/Policy_Brief_Template_NoAPI.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd

Use sed for simple text replacements:

  for qmd in \
    FinalDashboard/Dashboard/Policy_Brief_Template.qmd \
    FinalDashboard/Dashboard/Policy_Brief_Complete.qmd \
    FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd \
    FinalDashboard/NoAPI/Policy_Brief_Template_NoAPI.qmd \
    FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd \
    FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd; do

    echo "Updating: $qmd"
    sed -i '' 's/- darkly/- flatly/g' "$qmd"
    sed -i '' 's/theme_dark_dash()/theme_urbn_dash()/g' "$qmd"
  done

For the theme function body and color vectors, use Python str_replace
to make targeted substitutions safely. Read the actual updated
Template QMD first to get the exact new text, then apply it to
each file that still has the old version.

---

## STEP 3: Render all NoAPI and StudentExample files

Render with CENSUS_API_KEY=NONE to confirm offline versions still work:

  QUARTO=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto

  for qmd in \
    FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd \
    FinalDashboard/NoAPI/Policy_Brief_Template_NoAPI.qmd \
    FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd; do

    dir=$(dirname $qmd)
    file=$(basename $qmd)
    echo "━━━ $file ━━━"
    cd $dir
    CENSUS_API_KEY=NONE $QUARTO render $file --quiet 2>&1 | tail -3
    echo "Exit: $?"
    cd - > /dev/null
  done

If any fail, fix and re-render before proceeding.

---

## STEP 4: Render live API versions for StudentExample

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
    cut -d= -f2 | tr -d '"')
  QUARTO=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto

  for qmd in \
    FinalDashboard/StudentExample/Final_Project_SanDiego.qmd \
    FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd \
    FinalDashboard/Dashboard/Policy_Brief_Template.qmd \
    FinalDashboard/Dashboard/Policy_Brief_Complete.qmd; do

    dir=$(dirname $qmd)
    file=$(basename $qmd)
    echo "━━━ $file ━━━"
    cd $dir
    CENSUS_API_KEY=$CENSUS_API_KEY $QUARTO render $file --quiet 2>&1 | tail -3
    echo "Exit: $?"
    cd - > /dev/null
  done

---

## STEP 5: Clean up any _files/ folders

  find FinalDashboard -name "*_files" -type d | while read d; do
    echo "Removing: $d"
    rm -rf "$d"
  done
  echo "Cleanup done"

---

## STEP 6: Final size inventory

  python3 << 'EOF'
  import os, glob
  print("=== FinalDashboard HTML sizes ===")
  total_ok = True
  for f in sorted(glob.glob("FinalDashboard/**/*.html", recursive=True)):
      kb = os.path.getsize(f) / 1024
      flag = " ⚠ EXCEEDS 25MB" if kb > 25000 else " OK"
      if kb > 25000:
          total_ok = False
      print(f"  {kb:7.0f} KB  {f}{flag}")
  print()
  print(f"All under 25 MB: {total_ok}")
  EOF

If any file exceeds 25 MB, investigate and fix before committing.

---

## STEP 7: Verify no banned content survived

  echo "=== Banned content check ==="
  for f in $(find FinalDashboard -name "*.qmd"); do
    hits=$(grep -c "darkly\|theme_dark_dash\|#0d1117\|B15003_002\|psych::alpha\|crosstalk\|SharedData\|year.*2015\|72.*Puerto" "$f" 2>/dev/null || echo 0)
    if [ "$hits" -gt 0 ]; then
      echo "ISSUE in $f: $hits hits"
      grep -n "darkly\|theme_dark_dash\|#0d1117\|B15003_002\|psych::alpha\|crosstalk\|SharedData\|year.*2015\|72.*Puerto" "$f"
    fi
  done
  echo "Banned content check complete"

---

## STEP 8: Commit everything

  git add assets/dashboard-theme.scss FinalDashboard/
  git status --short | head -30

  git -c trailer.ifexists=doNothing commit -m \
    "FinalDashboard: Urban Institute theme, eval review fixes, all 10 files synced"
  git push

  echo ""
  echo "=== PIPELINE COMPLETE ==="
  echo "Latest commits:"
  git log --oneline -3
  echo ""
  echo "Live at: https://antjam-howell.github.io/paf-516-labs/"
  echo "Dashboard: https://antjam-howell.github.io/paf-516-labs/FinalDashboard/Dashboard/Final_Project_Complete.html"
