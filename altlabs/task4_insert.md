# Task 4 — Insert Inline Offline Fallback Chunks

For each AltLabs QMD, insert a commented-out fallback chunk immediately
after every get_acs() chunk. Then remove the saveRDS() lines from Task 3.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 4a — Process Lab 1 ONLY first (human approves format before Labs 2–6)

Read AltLabs/Lab1/Lab1_Assignment.qmd.

For each get_acs() chunk, insert the following fallback chunk immediately
after the closing backticks of the get_acs() chunk:

```
```{r}
#| label: <original-label>-offline
#| eval: false
#| include: false
# ── Offline fallback — use this chunk instead if the Census API is down ───
# <object_name>: <specific description>
#   - Geography:  <tract / block group / county>
#   - Coverage:   <Maricopa County AZ / Arizona statewide / National>
#   - Vintage:    <e.g. 2015–2019 ACS 5-year (year = 2019)>
#   - Shape:      <e.g. ~5,700 rows × 8 cols (950 tracts × 6 variables, long format)>
#   - Used in:    <downstream steps that depend on this object>
#
# Local:
# <object_name> <- readRDS("data/<filename>.rds")
#
# GitHub (if data/ folder not available):
# <object_name> <- readRDS(url("https://raw.githubusercontent.com/AntJam-Howell/paf-516-labs/main/Lab1/data/<filename>.rds"))
```
```

Rules — strictly enforced:
- label = original chunk label + "-offline"
- eval: false AND include: false — both required, no exceptions
- Description must be SPECIFIC. Bad: "tract data". Good: "Maricopa County
  census tracts, 2009–2013 ACS 5-year, 6 hardship variables in long format
  before pivot_wider(). 5,700 rows (950 tracts × 6 variables)."
- RDS filename must match exactly what is in AltLabs/Lab1/data/
- "Used in" must name actual downstream step labels or variable names
- data/ path (NOT ../data/) — AltLabs QMDs are not in a subdirectory
- GitHub URL uses Lab1 (not Lab{N} — use the actual lab number)
- One blank line between the get_acs() chunk closing ``` and the fallback ```{r}

After inserting Lab 1 fallbacks, print the FULL modified packages + first
get_acs() chunk + first fallback chunk so the human can review formatting.

⛔ STOP HERE after Lab 1. Wait for human approval of the fallback format
before continuing to Labs 2–6.

---

## 4b — Apply same pattern to Labs 2–6 (after approval)

Repeat 4a for each remaining lab. Use the same fallback format exactly.
For each lab print: "Lab N: X fallback chunks inserted"

---

## 4c — Remove saveRDS() lines inserted in Task 3

These were for data generation only — students should not see them.

  python3 << 'EOF'
  import glob, re

  for qmd in sorted(glob.glob("AltLabs/Lab*/Lab*_Assignment.qmd")):
      txt = open(qmd).read()
      # Remove saveRDS() lines (whole line, including leading whitespace)
      cleaned = re.sub(r'\n[ \t]*saveRDS\([^\n]+\)', '', txt)
      if cleaned != txt:
          count = txt.count('saveRDS(') - cleaned.count('saveRDS(')
          open(qmd, 'w').write(cleaned)
          print(f"Removed {count} saveRDS() line(s): {qmd}")
      else:
          print(f"No saveRDS() found: {qmd}")
  EOF

After cleanup, verify no saveRDS() lines remain:
  grep -rn "saveRDS" AltLabs/Lab*/Lab*_Assignment.qmd
  (expect: no output)

---

## 4d — Verify fallback chunk structure

  python3 << 'EOF'
  import glob, re

  OFFLINE_RE = re.compile(r'#\|\s*label:\s*(\S+-offline)')
  EVAL_RE    = re.compile(r'#\|\s*eval:\s*false')
  INCL_RE    = re.compile(r'#\|\s*include:\s*false')
  RDS_RE     = re.compile(r'readRDS\(')

  for qmd in sorted(glob.glob("AltLabs/Lab*/Lab*_Assignment.qmd")):
      txt = open(qmd).read()
      chunks = re.findall(r'```\{r\}.*?```', txt, re.DOTALL)
      offline = [c for c in chunks if OFFLINE_RE.search(c)]

      issues = []
      for c in offline:
          label = OFFLINE_RE.search(c).group(1)
          if not EVAL_RE.search(c):   issues.append(f"{label}: missing eval: false")
          if not INCL_RE.search(c):   issues.append(f"{label}: missing include: false")
          if not RDS_RE.search(c):    issues.append(f"{label}: missing readRDS()")

      lab = qmd.split('/')[1]
      if issues:
          print(f"{lab}: {len(offline)} offline chunks — ISSUES:")
          for i in issues: print(f"  ✗ {i}")
      else:
          print(f"{lab}: {len(offline)} offline chunks — all valid ✓")
  EOF
