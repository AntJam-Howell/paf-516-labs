# Task 2 — Setup AltLabs Folder Structure

Create AltLabs/ and populate with assignment QMDs and existing RDS files.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 2a — Create folder structure

  mkdir -p AltLabs/Lab{1,2,3,4,5,6}/data

## 2b — Copy assignment QMDs into AltLabs

  for n in 1 2 3 4 5 6; do
    cp Lab${n}/Assignment/Lab${n}_Assignment.qmd \
       AltLabs/Lab${n}/Lab${n}_Assignment.qmd \
    && echo "Copied: Lab${n}_Assignment.qmd" \
    || echo "ERROR: Lab${n} assignment QMD not found"
  done

## 2c — Copy existing RDS from Lab data/ folders into AltLabs

  for n in 1 2 3 4 5 6; do
    count=$(ls Lab${n}/data/*.rds 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
      cp Lab${n}/data/*.rds AltLabs/Lab${n}/data/
      echo "Copied $count RDS files → AltLabs/Lab${n}/data/"
    else
      echo "Lab${n}: no existing RDS to copy"
    fi
  done

## 2d — Copy LabSolutions RDS where Lab data/ was empty

For any lab where AltLabs/Lab{N}/data/ is still empty after 2c,
copy from the instructor LabSolutions:

  for n in 1 2 3 4 5 6; do
    count=$(ls AltLabs/Lab${n}/data/*.rds 2>/dev/null | wc -l)
    if [ "$count" -eq 0 ]; then
      src=~/Claude/Teaching/PAF516/paf-516-labs-instructor/LabSolutions/lab${n}
      sol_count=$(ls ${src}/*.rds 2>/dev/null | wc -l)
      if [ "$sol_count" -gt 0 ]; then
        cp ${src}/*.rds AltLabs/Lab${n}/data/
        echo "Lab${n}: copied $sol_count RDS from LabSolutions"
      else
        echo "Lab${n}: NO RDS available anywhere — needs API render in Task 3"
      fi
    fi
  done

## 2e — Verify structure

  find AltLabs/ -name "*.qmd" | sort
  echo "---"
  find AltLabs/ -name "*.rds" | sort

## 2f — Update packages chunk in each AltLabs QMD

The copied QMDs already have the canonical ~/.paf516_ready sentinel.
Verify this is the case — if any still have .renv_done, fix them:

  grep -l "renv_done" AltLabs/Lab*/Lab*_Assignment.qmd

If any files are returned, apply the canonical block to them now
(same replacement pattern as the main renv consolidation task).

Print "All AltLabs QMDs use correct renv sentinel" if grep returns nothing.

## 2g — Note the data/ path difference for AltLabs

AltLabs QMDs live at AltLabs/Lab{N}/Lab{N}_Assignment.qmd
(NOT in a Tutorial/ or Assignment/ subdirectory)
Therefore fallback paths are "data/filename.rds" (NOT "../data/filename.rds")

This will be important in Task 4. Record this fact in a note:
  echo "AltLabs data path: data/ (not ../data/)" > AltLabs/PATH_NOTE.txt
