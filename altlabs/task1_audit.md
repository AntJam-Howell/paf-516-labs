# Task 1 — Audit

Map every get_acs() chunk in Labs 1–6 and inventory all existing RDS files.
This produces the complete data requirements map used in all later tasks.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 1a — Inventory existing RDS in public repo Lab data/ folders

  find Lab{1,2,3,4,5,6}/data/ -name "*.rds" 2>/dev/null | sort

Print the full list. Note which labs have empty or missing data/ folders.

## 1b — Inventory RDS in instructor LabSolutions

  find ~/Claude/Teaching/PAF516/paf-516-labs-instructor/LabSolutions/ \
    -name "*.rds" 2>/dev/null | sort

Print the full list.

## 1c — Map every get_acs() chunk in each assignment QMD

For each Lab{N}/Assignment/Lab{N}_Assignment.qmd, extract:
  - chunk label
  - object name assigned (e.g. tract_raw <- get_acs(...))
  - geography (tract / block group / county)
  - state and county filter
  - year
  - survey (acs5)
  - geometry (TRUE/FALSE)

Use Python:

  python3 << 'EOF'
  import re, glob

  CHUNK_RE  = re.compile(r'```\{r\}.*?```', re.DOTALL)
  LABEL_RE  = re.compile(r'#\|\s*label:\s*(\S+)')
  ASSIGN_RE = re.compile(r'(\w+)\s*<-\s*get_acs\(')
  GETACS_RE = re.compile(r'get_acs\(')
  GEO_RE    = re.compile(r'geography\s*=\s*["\']([^"\']+)["\']')
  YEAR_RE   = re.compile(r'year\s*=\s*(\d+)')
  STATE_RE  = re.compile(r'state\s*=\s*["\']([^"\']+)["\']')
  COUNTY_RE = re.compile(r'county\s*=\s*["\']([^"\']+)["\']')
  GEOM_RE   = re.compile(r'geometry\s*=\s*(TRUE|FALSE)')

  for n in range(1, 7):
      qmd_path = f"Lab{n}/Assignment/Lab{n}_Assignment.qmd"
      try:
          txt = open(qmd_path).read()
      except FileNotFoundError:
          print(f"Lab{n}: QMD NOT FOUND at {qmd_path}"); continue

      chunks = CHUNK_RE.findall(txt)
      found = []
      for chunk in chunks:
          if not GETACS_RE.search(chunk): continue
          label   = LABEL_RE.search(chunk)
          obj     = ASSIGN_RE.search(chunk)
          geo     = GEO_RE.search(chunk)
          year    = YEAR_RE.search(chunk)
          state   = STATE_RE.search(chunk)
          county  = COUNTY_RE.search(chunk)
          geom    = GEOM_RE.search(chunk)
          found.append({
              'label':   label.group(1)  if label  else 'UNKNOWN',
              'object':  obj.group(1)    if obj    else 'UNKNOWN',
              'geo':     geo.group(1)    if geo    else '?',
              'year':    year.group(1)   if year   else '?',
              'state':   state.group(1)  if state  else '?',
              'county':  county.group(1) if county else 'statewide',
              'geom':    geom.group(1)   if geom   else '?',
          })

      print(f"\n=== Lab{n}: {len(found)} get_acs() chunk(s) ===")
      for f in found:
          print(f"  chunk:  {f['label']}")
          print(f"  object: {f['object']}")
          print(f"  pull:   {f['geo']} | {f['state']} | "
                f"{f['county']} | year={f['year']} | geom={f['geom']}")
          print()
  EOF

## 1d — Cross-reference: which get_acs() chunks already have RDS coverage?

For each get_acs() chunk found in 1c, check whether a matching RDS exists
in Lab{N}/data/ or LabSolutions/lab{N}/. Print a coverage table:

  Lab | Chunk label          | Object          | RDS exists? | RDS filename
  ────┼──────────────────────┼─────────────────┼─────────────┼────────────
  1   | step.01-pull         | tract_raw       | NO          | —
  1   | step.01-pull-county  | county_raw      | YES         | county_hardship_2023.rds
  ...

## 1e — Stop and report

Print a final summary:
  - Total get_acs() chunks across all 6 labs: N
  - Chunks with existing RDS coverage: M
  - Chunks needing new RDS generation: N-M
  - Labs with complete RDS coverage: list
  - Labs needing API render to generate missing RDS: list

⛔ STOP HERE. Do not proceed to Task 2 until human reviews this audit.
