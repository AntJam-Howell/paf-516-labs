# AltLabs Pipeline — Offline-Ready Lab Assignments

Builds offline-ready versions of Labs 1–6 assignments in AltLabs/.
Students can render these with no Census API access using pre-built RDS files.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## What AltLabs Is

AltLabs/ contains assignment QMDs that are structurally identical to the
public Lab{N}/Assignment/Lab{N}_Assignment.qmd files, with one addition:
immediately after each get_acs() chunk, a commented-out fallback chunk
loads the equivalent pre-built RDS from data/. Students uncomment the
fallback when the Census API is unavailable.

AltLabs/ lives in the PUBLIC repo. It is not in the instructor repo.

---

## Subtask Files

  altlabs/task1_audit.md       ← inventory RDS files + get_acs() chunks
  altlabs/task2_setup.md       ← create folder structure, copy files
  altlabs/task3_api_run.md     ← render with API, save RDS, verify
  altlabs/task4_insert.md      ← insert fallback chunks, clean saveRDS()
  altlabs/task5_verify.md      ← offline render, confirm no API needed
  altlabs/task6_compare.md     ← compare vs LabSolutions HTML

---

## Execution Order + Human Checkpoints

Run each task file in order. STOP for human approval at these gates:

  GATE 1 — After task1: Review the RDS inventory and get_acs() chunk map.
            Confirm coverage is complete before creating any files.

  GATE 2 — After task3: Review the generated RDS file list.
            Every get_acs() chunk must have a corresponding RDS.
            If any lab is missing RDS files, fix before proceeding.

  GATE 3 — After task4: Review the fallback chunk format in Lab 1 only.
            Confirm label, annotation, path, and eval: false are correct.
            Approve before applying to Labs 2–6.

  GATE 4 — After task5: Every lab must show PASS for offline render.
            A FAIL here means a missing RDS or broken path — fix before
            comparing against solutions.

  GATE 5 — After task6: Review the comparison table.
            Flag any lab below 85% numeric match or figure count mismatch.
            Human decides whether to promote AltLabs to public repo.

---

## Final Output

After all tasks complete and human approves:

  AltLabs/
    Lab{1-6}/
      Lab{N}_Assignment.qmd    ← offline-ready QMD
      Lab{N}_Assignment.html   ← rendered without Census API
      data/
        *.rds                  ← all datasets needed to render

Commit to public repo:
  git add AltLabs/
  git -c trailer.ifexists=doNothing commit -m \
    "Add AltLabs offline-ready lab assignments (Labs 1–6)"
  git push

---

## Key Rules for AltLabs QMDs

  - Fallback chunk label = original label + "-offline"
  - eval: false and include: false on every fallback chunk
  - ../data/ paths (NOT data/) — QMDs live in AltLabs/Lab{N}/ not a subdir
    WAIT: AltLabs QMDs are at AltLabs/Lab{N}/Lab{N}_Assignment.qmd,
    so data/ (not ../data/) is correct for AltLabs specifically
  - Fallback annotation must be specific (geography, vintage, dimensions)
  - Both local readRDS() and GitHub raw URL provided as comments
  - saveRDS() lines used for generation only — removed before final render
  - Do NOT alter any existing code chunks — only add fallback chunks after
