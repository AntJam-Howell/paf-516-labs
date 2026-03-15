# Task 5 — Offline Render Verification

Confirm every AltLabs QMD renders cleanly with no Census API access.

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

---

## 5a — Activate fallback chunks for offline test

The fallback chunks currently have eval: false. To test offline rendering,
we need to temporarily flip them to eval: true and comment out the
get_acs() chunks above them.

Use Python to create temporary *_OFFLINE.qmd versions of each AltLabs QMD:

  python3 << 'EOF'
  import glob, re, shutil

  GETACS_CHUNK = re.compile(
      r'(```\{r\}(?:(?!```).)*?get_acs\((?:(?!```).)*?```)',
      re.DOTALL
  )
  OFFLINE_CHUNK = re.compile(
      r'(```\{r\}\s*\n#\|\s*label:\s*\S+-offline.*?```)',
      re.DOTALL
  )
  EVAL_FALSE = re.compile(r'(#\|\s*eval:\s*)false')
  INCL_FALSE = re.compile(r'(#\|\s*include:\s*)false')

  for qmd in sorted(glob.glob("AltLabs/Lab*/Lab*_Assignment.qmd")):
      txt = open(qmd).read()

      # Comment out get_acs() lines within live chunks
      def comment_getacs(m):
          chunk = m.group(1)
          lines = chunk.split('\n')
          out = []
          for line in lines:
              if 'get_acs(' in line or (out and out[-1].rstrip().endswith(',')):
                  out.append('# ' + line if not line.startswith('#') else line)
              else:
                  out.append(line)
          return '\n'.join(out)

      # Simpler approach: comment every line between get_acs( and closing )
      def disable_getacs_chunk(chunk_txt):
          lines = chunk_txt.split('\n')
          in_call = False
          result = []
          for line in lines:
              stripped = line.strip()
              if 'get_acs(' in line and not stripped.startswith('#'):
                  in_call = True
              if in_call:
                  result.append('# ' + line if not stripped.startswith('#') else line)
                  if stripped.endswith(')') or stripped == ')':
                      in_call = False
              else:
                  result.append(line)
          return '\n'.join(result)

      # For each get_acs chunk: disable it
      modified = txt
      for m in GETACS_CHUNK.finditer(txt):
          disabled = disable_getacs_chunk(m.group(1))
          modified = modified.replace(m.group(1), disabled, 1)

      # For each offline chunk: activate it (eval: false → true, include: false → true)
      for m in OFFLINE_CHUNK.finditer(modified):
          activated = EVAL_FALSE.sub(r'\1true', m.group(1))
          activated = INCL_FALSE.sub(r'\1true', activated)
          # Also uncomment readRDS lines
          activated = re.sub(r'\n# (<\w+> <- readRDS)', r'\n\1', activated)
          activated = re.sub(r'\n# (\w+ <- readRDS)', r'\n\1', activated)
          modified = modified.replace(m.group(1), activated, 1)

      out_path = qmd.replace('.qmd', '_OFFLINE.qmd')
      open(out_path, 'w').write(modified)
      print(f"Created: {out_path}")
  EOF

## 5b — Render each _OFFLINE.qmd with invalid API key

  QUARTO=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto

  for n in 1 2 3 4 5 6; do
    echo "━━━ Offline render Lab${n} ━━━"
    cd AltLabs/Lab${n}
    CENSUS_API_KEY=OFFLINE_TEST \
      $QUARTO render Lab${n}_Assignment_OFFLINE.qmd --quiet 2>&1 | tail -10
    if [ $? -eq 0 ]; then
      echo "Lab${n}: ✓ PASS — rendered without Census API"
    else
      echo "Lab${n}: ✗ FAIL — full error follows:"
      CENSUS_API_KEY=OFFLINE_TEST \
        $QUARTO render Lab${n}_Assignment_OFFLINE.qmd 2>&1
    fi
    cd ../..
    echo ""
  done

## 5c — File size sanity check on rendered HTMLs

A successful offline render should produce HTML of comparable size to
the original. A near-empty HTML (< 200KB) means something failed silently.

  python3 << 'EOF'
  import os, glob
  for html in sorted(glob.glob("AltLabs/Lab*/*_OFFLINE.html")):
      size_kb = os.path.getsize(html) / 1024
      status = "✓ OK" if size_kb > 200 else "✗ SUSPICIOUSLY SMALL — check render"
      print(f"  {size_kb:6.0f} KB  {html}  {status}")
  EOF

## 5d — Clean up _OFFLINE temporary files

After reviewing results, remove the temporary files:

  find AltLabs/ -name "*_OFFLINE.qmd" -delete
  find AltLabs/ -name "*_OFFLINE.html" -delete
  echo "Offline test files removed"

⛔ STOP HERE. Every lab must show PASS in 5b AND have HTML > 200KB in 5c.
If any lab fails, diagnose and fix before proceeding to Task 6.

Common failure causes:
  - readRDS() path is "data/" but the file is somewhere else → fix path
  - Fallback chunk not activated (still eval: false) → check task 4d output
  - RDS file missing from AltLabs/Lab{N}/data/ → re-run task 3 for that lab
  - get_acs() chunk not fully commented out → check 5a python output
