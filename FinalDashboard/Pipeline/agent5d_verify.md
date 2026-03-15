# Agent 5d — Final Render, Verify, and Commit

Render all Complete files. Verify answers survived rendering.
Update landing page. Commit everything.

---

## Step 1: Render both Complete files

  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Complete.qmd 2>&1 | tail -10
  echo "Complete dashboard: exit $?"

  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Policy_Brief_Complete.qmd 2>&1 | tail -10
  echo "Complete brief: exit $?"
  cd ../..

---

## Step 2: Verify answers appear in rendered HTML

  python3 << 'EOF'
  import re

  for html in ["FinalDashboard/Dashboard/Final_Project_Complete.html",
               "FinalDashboard/Dashboard/Policy_Brief_Complete.html"]:
      txt = open(html).read()
      # Check TODO placeholders are gone
      todos = txt.count("YOUR ANSWER HERE") + txt.count("[Your answer here")
      # Check recommendation cards have content > 100 chars
      cards = re.findall(r'## Recommendation \d', txt)
      print(f"{html}:")
      print(f"  Remaining TODOs: {todos}  (expect: 0)")
      print(f"  Recommendation headers found: {len(cards)}  (expect: 3)")
      print(f"  File size: {len(txt)//1024} KB")
      print()
  EOF

If any TODO placeholders remain, stop and report — Agent 5c missed something.

---

## Step 3: Full inventory of FinalDashboard/

  python3 << 'EOF'
  import os, glob

  print("=== FinalDashboard/ Inventory ===\n")
  for root, dirs, files in os.walk("FinalDashboard"):
      dirs[:] = [d for d in dirs if d not in ["Pipeline"]]
      level = root.replace("FinalDashboard", "").count(os.sep)
      indent = "  " * level
      print(f"{indent}{os.path.basename(root)}/")
      for f in sorted(files):
          fpath = os.path.join(root, f)
          kb = os.path.getsize(fpath)/1024
          flag = " ⚠ LARGE" if kb > 25000 else ""
          print(f"{indent}  {kb:7.0f} KB  {f}{flag}")
  EOF

---

## Step 4: Final verification checklist

Run all checks. Every item must pass before commit.

  # 1. No banned content in any source QMD
  grep -rl "B15003_002\|psych::alpha\|crosstalk\|SharedData\|year.*2015\|leaflet" \
    FinalDashboard/Dashboard/ FinalDashboard/NoAPI/ FinalDashboard/StudentExample/
  # Expect: no output

  # 2. No _files/ folders
  find FinalDashboard -name "*_files" -type d
  # Expect: no output

  # 3. All 8 expected HTML files exist
  ls FinalDashboard/Dashboard/*.html
  ls FinalDashboard/NoAPI/*.html
  ls FinalDashboard/StudentExample/*.html
  # Expect: 4 + 2 + 4 = 10 HTML files

  # 4. All RDS files present
  find FinalDashboard -name "*.rds" | sort
  # Expect: 5 in NoAPI/data/, 5 in StudentExample/data/

  # 5. mapgl only in National Context tab in all source QMDs
  for qmd in FinalDashboard/Dashboard/Final_Project_Template.qmd \
              FinalDashboard/NoAPI/Final_Project_Template_NoAPI.qmd \
              FinalDashboard/StudentExample/Final_Project_SanDiego.qmd; do
    echo "=== $qmd ==="
    grep -n "maplibre\|add_fill_layer" "$qmd"
  done

---

## Step 5: Update Module7 Guide

Read Module7/Module7_Guide.qmd and make ONLY these targeted changes:

  A. Lab 07 overview table — update to 5 tabs:
     National Context | Local Hardship | Hot Spots | Change & Trajectories | Policy

  B. Download link — update to:
     https://raw.githubusercontent.com/AntJam-Howell/paf-516-labs/main/FinalDashboard/Dashboard/Final_Project_Template.qmd

  C. Deliverables section — update to:
     1. Final_Project_Template.qmd — completed with your county and 3 recommendations
     2. Final_Project_Template.html — rendered dashboard HTML

  D. Remove any mention of crosstalk, SharedData, or RPubs publishing requirement
     (RPubs is now optional extra credit, not required)

  E. Grading criteria — update to match ORCHESTRATOR.md rubric:
     Recommendation quality (60%), Dashboard renders (20%), Design (20%)

  F. Render Module7 guide and copy to docs/:
     QUARTO render Module7/Module7_Guide.qmd
     cp Module7/Module7_Guide.html docs/Module7_Guide.html

---

## Step 6: Update docs/index.html Final Project box

Read docs/index.html. Find the Final Project box (last section).
Update the 4 button href values to point to FinalDashboard paths:

  View Example    → FinalDashboard/Dashboard/Final_Project_Complete.html
                    (relative path within GitHub Pages)
  Download Template → https://raw.githubusercontent.com/AntJam-Howell/paf-516-labs/main/FinalDashboard/Dashboard/Final_Project_Template.qmd
  Policy Brief    → https://raw.githubusercontent.com/AntJam-Howell/paf-516-labs/main/FinalDashboard/Dashboard/Policy_Brief_Template.qmd
  Instructions    → Module7_Guide.html

Do NOT change any other content in index.html.

---

## Step 7: Commit everything

  git add FinalDashboard/ docs/ Module7/
  git -c trailer.ifexists=doNothing commit -m \
    "Add FinalDashboard: parameterized dashboard, policy brief, NoAPI versions, San Diego example, Phoenix completed answers"
  git push

  echo "Pushed. Live at:"
  git remote get-url origin
  git log --oneline -1

---

## Step 8: Final report

Print the complete summary table:

  File                                                    | Size KB | Render | API-free |
  --------------------------------------------------------|---------|--------|---------|
  Dashboard/Final_Project_Template.html                   |         | PASS   | no      |
  Dashboard/Final_Project_Complete.html                   |         | PASS   | no      |
  Dashboard/Policy_Brief_Template.html                    |         | PASS   | no      |
  Dashboard/Policy_Brief_Complete.html                    |         | PASS   | no      |
  NoAPI/Final_Project_Template_NoAPI.html                 |         | PASS   | PASS    |
  NoAPI/Policy_Brief_Template_NoAPI.html                  |         | PASS   | PASS    |
  StudentExample/Final_Project_SanDiego.html              |         | PASS   | no      |
  StudentExample/Policy_Brief_SanDiego.html               |         | PASS   | no      |
  StudentExample/Final_Project_SanDiego_NoAPI.html        |         | PASS   | PASS    |
  StudentExample/Policy_Brief_SanDiego_NoAPI.html         |         | PASS   | PASS    |

⛔ FINAL STOP — print table and wait for human approval before Step 7 (commit).
