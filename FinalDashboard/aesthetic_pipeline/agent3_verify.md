# Agent 3 — Verify, Sync, Commit

Prerequisite: Agent 2 approved. Template renders cleanly.

---

## STEP 1: Render Final_Project_Complete.qmd

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Complete.qmd 2>&1 | tail -10
  cd ../..

---

## STEP 2: Verify checklist

  python3 << 'EOF'
  import re, os

  files = [
    "FinalDashboard/Dashboard/Final_Project_Template.qmd",
    "FinalDashboard/Dashboard/Final_Project_Complete.qmd",
    "assets/dashboard-theme.scss"
  ]

  for f in files:
    txt = open(f).read()
    print(f"=== {f} ===")
    print(f"  darkly present:         {'darkly' in txt} (expect False)")
    print(f"  flatly present:         {'flatly' in txt} (expect True)")
    print(f"  theme_dark_dash:        {'theme_dark_dash' in txt} (expect False)")
    print(f"  theme_urbn_dash:        {'theme_urbn_dash' in txt} (expect True for QMDs)")
    print(f"  #0d1117 (old bg):       {'0d1117' in txt} (expect False)")
    print(f"  Lato font:              {'Lato' in txt} (expect True)")
    print(f"  #1696d2 (Urban cyan):   {'1696d2' in txt} (expect True)")
    print(f"  mapgl/maplibre:         {'maplibre' in txt or 'mapgl(' in txt} (expect False)")
    print()

  # Check HTML sizes
  for html in ["FinalDashboard/Dashboard/Final_Project_Template.html",
               "FinalDashboard/Dashboard/Final_Project_Complete.html"]:
    if os.path.exists(html):
      kb = os.path.getsize(html) / 1024
      flag = "⚠ LARGE" if kb > 25000 else "OK"
      print(f"{html}: {kb:.0f} KB — {flag}")
  EOF

---

## STEP 3: Sync theme changes to NoAPI and StudentExample QMDs

The NoAPI and StudentExample files need the same YAML theme change
(darkly → flatly) and theme function rename.

For each file in the list below, apply:
  A. YAML: darkly → flatly
  B. theme_dark_dash() → theme_urbn_dash()
  C. Update lisa_colors and traj_colors to Urban Institute palette
  D. Update diverging map mid color to #f5f5f5

Files to update:
  FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd
  FinalDashboard/NoAPI/Policy_Brief_Template_NoAPI.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego.qmd
  FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd
  FinalDashboard/StudentExample/Policy_Brief_SanDiego_NoAPI.qmd

Also update FinalDashboard/Dashboard/Policy_Brief_Template.qmd and
FinalDashboard/Dashboard/Policy_Brief_Complete.qmd — same changes.

Use sed for the simple replacements:
  for qmd in [list]; do
    sed -i '' 's/- darkly/- flatly/' "$qmd"
    sed -i '' 's/theme_dark_dash()/theme_urbn_dash()/g' "$qmd"
  done

For color values, use Python str_replace to be safe.

---

## STEP 4: Render NoAPI and SanDiego spot-check

  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd --quiet 2>&1 | tail -5
  echo "NoAPI: $?"

  CENSUS_API_KEY=NONE \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render FinalDashboard/StudentExample/Final_Project_SanDiego_NoAPI.qmd --quiet 2>&1 | tail -5
  echo "SanDiego NoAPI: $?"

---

## STEP 5: Final size inventory

  python3 -c "
  import os, glob
  for f in sorted(glob.glob('FinalDashboard/**/*.html', recursive=True)):
      kb = os.path.getsize(f)/1024
      flag = ' ⚠' if kb > 25000 else ''
      print(f'  {kb:7.0f} KB  {f}{flag}')
  "

---

## STEP 6: Commit

  git add assets/dashboard-theme.scss FinalDashboard/
  git -c trailer.ifexists=doNothing commit -m \
    "FinalDashboard: Urban Institute aesthetic — flatly theme, Lato font, UI color palette"
  git push

  echo "Pushed: $(git log --oneline -1)"
