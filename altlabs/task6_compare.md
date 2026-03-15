# Task 6 — Compare vs LabSolutions + Commit

Verify AltLabs output matches instructor solutions, then commit to public repo.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 6a — Re-render final AltLabs HTMLs (clean, no offline test artifacts)

The Task 5 offline test used temporary _OFFLINE.qmd files. Now render the
final production QMDs normally (with Census API) to produce the clean HTMLs
that will be committed to the repo:

  QUARTO=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto
  CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
    cut -d= -f2 | tr -d '"' | tr -d "'")

  for n in 1 2 3 4 5 6; do
    echo "━━━ Final render Lab${n} ━━━"
    cd AltLabs/Lab${n}
    CENSUS_API_KEY=$CENSUS_API_KEY \
      $QUARTO render Lab${n}_Assignment.qmd --quiet 2>&1 | tail -5
    echo "Lab${n}: $([ $? -eq 0 ] && echo PASS || echo FAIL)"
    cd ../..
  done

## 6b — Compare AltLabs HTML vs LabSolutions HTML

  python3 << 'EOF'
  import os, re
  from pathlib import Path

  INSTRUCTOR = Path(os.path.expanduser(
    "~/Claude/Teaching/PAF516/paf-516-labs-instructor/LabSolutions"))
  ALTLABS = Path("AltLabs")

  PASS_THRESHOLD_SIZE  = 0.80   # AltLabs HTML must be >= 80% of solution size
  PASS_THRESHOLD_NUMS  = 0.85   # 85% of solution's numeric values must appear
  WARN_THRESHOLD_FIGS  = 1      # Flag if figure count differs by more than 1

  print(f"\n{'Lab':<4} {'Rendered':<10} {'Size %':<10} {'Nums %':<10} "
        f"{'Figs (alt/sol)':<16} {'Status'}")
  print("─" * 65)

  for n in range(1, 7):
      alt_htmls = list((ALTLABS / f"Lab{n}").glob("*.html"))
      sol_htmls = list((INSTRUCTOR / f"lab{n}").glob("*.html"))

      if not alt_htmls:
          print(f"Lab{n:<2} {'NO HTML':<10} {'—':<10} {'—':<10} {'—':<16} ✗ FAIL"); continue
      if not sol_htmls:
          print(f"Lab{n:<2} {'OK':<10} {'—':<10} {'—':<10} {'—':<16} NO SOLUTION"); continue

      alt_txt = alt_htmls[0].read_text(errors="ignore")
      sol_txt = sol_htmls[0].read_text(errors="ignore")

      size_ratio = len(alt_txt) / len(sol_txt)

      alt_nums = set(re.findall(r'\b\d+\.\d{2,4}\b', alt_txt))
      sol_nums = set(re.findall(r'\b\d+\.\d{2,4}\b', sol_txt))
      num_match = len(alt_nums & sol_nums) / len(sol_nums) if sol_nums else 1.0

      alt_figs = alt_txt.count('<img') + alt_txt.count('<svg')
      sol_figs = sol_txt.count('<img') + sol_txt.count('<svg')
      fig_diff = abs(alt_figs - sol_figs)

      ok_size = size_ratio >= PASS_THRESHOLD_SIZE
      ok_nums = num_match  >= PASS_THRESHOLD_NUMS
      ok_figs = fig_diff   <= WARN_THRESHOLD_FIGS

      status = "✓ PASS" if (ok_size and ok_nums and ok_figs) else "✗ REVIEW"
      print(f"Lab{n:<2} {'OK':<10} {size_ratio:<10.0%} {num_match:<10.0%} "
            f"{alt_figs}/{sol_figs:<13} {status}")

      # Print missing numeric values if below threshold
      if not ok_nums:
          missing = sorted(sol_nums - alt_nums)[:10]
          print(f"     Missing values (first 10): {missing}")
      if not ok_figs:
          print(f"     Figure count mismatch: AltLabs={alt_figs} Solution={sol_figs}")

  print()
  EOF

## 6c — Human checkpoint: review the comparison table

Any lab marked "✗ REVIEW" needs investigation:
  - Size < 80%: large section of output is missing — check which steps failed
  - Nums < 85%: key computed values differ — may indicate different data vintage
  - Figs mismatch > 1: a plot chunk failed silently

⛔ STOP HERE if any lab shows ✗ REVIEW. Diagnose and fix before committing.

Acceptable reasons NOT to flag (document these):
  - ACS data may differ slightly from when LabSolutions was generated
    (ACS estimates are updated annually; small numeric differences are OK)
  - LabSolutions used a different random seed for permutation tests

---

## 6d — Commit AltLabs to public repo

After human approves the comparison table:

  # Confirm we are in the public repo
  git remote -v

  # Stage everything in AltLabs/
  git add AltLabs/

  # Verify what is being committed
  git status --short | grep AltLabs

  # Commit
  git -c trailer.ifexists=doNothing commit -m \
    "Add AltLabs offline-ready lab assignments (Labs 1–6)"

  # Push
  git push

  # Confirm
  echo "Pushed. Live at:"
  echo "https://github.com/AntJam-Howell/paf-516-labs/tree/main/AltLabs"

---

## 6e — Final inventory report

  echo "=== AltLabs Final Inventory ==="
  for n in 1 2 3 4 5 6; do
    qmd_count=$(ls AltLabs/Lab${n}/*.qmd 2>/dev/null | wc -l)
    html_count=$(ls AltLabs/Lab${n}/*.html 2>/dev/null | wc -l)
    rds_count=$(ls AltLabs/Lab${n}/data/*.rds 2>/dev/null | wc -l)
    echo "  Lab${n}: ${qmd_count} QMD | ${html_count} HTML | ${rds_count} RDS"
  done

Expected output for each lab: 1 QMD | 1 HTML | N RDS (where N matches get_acs() count)
