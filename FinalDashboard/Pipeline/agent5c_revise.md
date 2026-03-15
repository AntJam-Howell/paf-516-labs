# Agent 5c — Revise and Write Final Answers

Read Agent 5b's critique. Revise every section that failed.
Then write the final answers into both Complete QMD files.

---

## Step 1: Revise based on critique

For each failing section identified by Agent 5b:
  - Address every specific required change
  - Do not re-introduce vagueness to fix a different problem
  - If a geography was too vague, use the DT table from the rendered HTML
    to identify specific tract GEOIDs and their general location

---

## Step 2: Write answers into Final_Project_Complete.qmd

Open FinalDashboard/Dashboard/Final_Project_Complete.qmd.

Replace the 3 Policy tab TODO card blocks. The format for each completed card:

```
::: {.card}
## Recommendation 1 — [Specific Policy Title]
[Full substantive answer — 3-4 sentences, specific geography,
specific statistic, named entity, concrete intervention]
:::
```

Also update the YAML title in the Complete file:
  title: "Economic Hardship Dashboard — Maricopa County Example"
  subtitle: "Instructor Reference | Completed Analysis"

---

## Step 3: Write answers into Policy_Brief_Complete.qmd

Open FinalDashboard/Dashboard/Policy_Brief_Complete.qmd.

Replace every *YOUR ANSWER HERE* placeholder with the revised text.
Replace the Executive Summary TODO with the completed summary.

Update the YAML:
  title: "Economic Hardship in Maricopa County"
  subtitle: "Policy Brief — Instructor Reference"
  author: "PAF 516 | Arizona State University"

Add a note at the very top (before the callout):
```
::: {.callout-warning}
## Instructor Reference
This is the completed example for Maricopa County. Students should
view this as a model for what a strong submission looks like —
not as a template to copy. Your analysis will use a different county
and must reflect your own interpretation of the results.
:::
```

---

## Step 4: Pass to Agent 5d for rendering and verification

Print a summary of all changes made.
⛔ STOP — do not render. Agent 5d renders and verifies.
