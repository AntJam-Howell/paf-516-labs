# Agent 5 — Phoenix Answer-Writing Pipeline

Build the completed Phoenix example dashboard and policy brief.
This uses a 4-sub-agent internal loop: draft → critique → revise → verify.

Prerequisite: Agent 4 completed. All renders passing.

---

## What this produces

  FinalDashboard/Dashboard/Final_Project_Complete.qmd   ← Maricopa + full answers
  FinalDashboard/Dashboard/Final_Project_Complete.html  ← rendered completed
  FinalDashboard/Dashboard/Policy_Brief_Complete.qmd    ← Maricopa + full answers
  FinalDashboard/Dashboard/Policy_Brief_Complete.html   ← rendered completed

These are the instructor model answers. Students view Final_Project_Complete.html
as a reference before writing their own answers.

---

## Setup

  # Copy templates as starting point for complete versions
  cp FinalDashboard/Dashboard/Final_Project_Template.qmd \
     FinalDashboard/Dashboard/Final_Project_Complete.qmd

  cp FinalDashboard/Dashboard/Policy_Brief_Template.qmd \
     FinalDashboard/Dashboard/Policy_Brief_Complete.qmd

  # Render the TEMPLATE (blank) to get actual computed values for Phoenix
  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | cut -d= -f2 | tr -d '"')
  cd FinalDashboard/Dashboard
  CENSUS_API_KEY=$CENSUS_API_KEY \
    /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
    render Final_Project_Template.qmd --quiet 2>&1 | tail -5
  cd ../..

  # Extract key statistics from the rendered HTML for use by sub-agents
  python3 -c "
  import re
  txt = open('FinalDashboard/Dashboard/Final_Project_Template.html').read()
  nums = re.findall(r'\b\d+\.?\d*\b', txt)
  print('HTML present:', len(txt) > 10000)
  " 

---

## Sub-agent sequence

Execute in order:
  STEP 5a → Pipeline/agent5a_draft.md    (draft answers from rendered HTML)
  STEP 5b → Pipeline/agent5b_critique.md (scrutinize — are answers good enough?)
  STEP 5c → Pipeline/agent5c_revise.md   (revise based on critique)
  STEP 5d → Pipeline/agent5d_verify.md   (render final, verify, commit)

⛔ STOP after 5d — human approves final commit
