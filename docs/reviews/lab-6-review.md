# Lab 6 — Code Review

## Summary
**NEEDS REVISION** — Lab 6 uses `library(mclust)` which is explicitly prohibited by the curriculum spec, has no `#| results: hide` on any data pull chunk, is missing the standardized Q1/Q2/Q3 questions section, has a logic bug where `mhv.change` is computed before the sub-$1,000 filter, and the YAML places `fig-width`/`fig-height` under `format: html:` instead of under `execute:`. The code annotations are strong (good use of `# ──` headers throughout), and the analytical narrative is well-written.

## Deprecated Functions/Packages
**Issues found:**

1. **Line 40: `library( mclust )`** — The CLAUDE.md curriculum spec explicitly states: "No regression. No mclust. No complex clustering." The mclust package is used in Part 4 for model-based clustering (line 578: `fit <- Mclust(...)`). This entire section (Part 4, lines 543-700) uses mclust for Gaussian mixture model clustering, which the curriculum redesign prohibits.

2. **No other deprecated functions found.** Lab 6 correctly uses `slice_sample()` instead of `sample_n()` (lines 336 and 476, with comments noting the replacement). No use of `spread()`, `gather()`, `summarise_each()`, `funs()`, `do()`, `aes_string()`, or deprecated spatial packages (sp, rgdal, maptools, tmap).

## Output Suppression
**Issues found:**

1. **Line 43-49 (`setup` chunk):** Correctly has `#| include: false`. However, it only sets `s.type <- "html"` — it does NOT include `knitr::opts_chunk$set(...)` or `options(tigris_use_cache = TRUE)` as required by the standard.

2. **Line 59-84 (`load-data` chunk): Missing `#| results: hide`.** This chunk loads three RDS files from GitHub URLs via `readRDS(gzcon(url(...)))`. While RDS loading is typically quiet, this is a data pull chunk and should have `#| results: hide` per the standard.

3. **Line 95-121 (`mhv-variables` chunk): No `#| results: hide`.** This is a computation chunk (no data pull), so no issue.

4. **Line 126-141 (`summary-stats` chunk):** Has `#| results: asis` for stargazer output. Correct for this use case.

5. **Line 574-584 (`clustering` chunk): Missing `#| results: hide` or suppression.** Lines 579-583 call `summary( fit )` and `table( d3$cluster.group )`, which will print console output. If this output is intended for the student to see, it should be kept. But if not, it needs suppression.

6. **YAML (lines 14-17):** Has `warning: false` and `message: false` under `execute:`. Good. However, `fig-width: 10` and `fig-height: 6` are placed under `format: html:` (lines 12-13) instead of under `execute:` where the standard places them. In Quarto, `fig-width` under `format: html:` is valid but it is an HTML-specific setting rather than a global execution setting. For consistency with Lab 5 and the standard template, these should be under `execute:`.

7. **Line 24-41 (`packages` chunk): Missing `#| results: hide` or `#| include: false`.** Package loading messages (especially from mclust, which prints a startup banner) will be visible unless suppressed. The YAML global `message: false` may not suppress mclust's `packageStartupMessage()` — mclust is known to print a citation notice via `packageStartupMessage()` which IS suppressed by `message: false`, but it also may print via `cat()` depending on the version. Worth verifying.

## Code Annotations
**Assessment: GOOD — meets the standard well.**

Strengths:
- Consistent use of `# ──` section headers throughout (e.g., line 62: `# ── Load LTDB data files from GitHub ──`, line 98: `# ── CPI inflation adjustment ──`, line 275: `# ── Log-transform to correct right skew ──`). This matches the required format.
- Every major code block has comment blocks explaining WHAT and WHY. Examples: lines 98-101 (CPI multiplier with source), lines 106-110 (dollar change and filtering rationale), lines 409-416 (2010 variable construction), lines 422-424 (change variables with interpretation note).
- Good inline comments on non-obvious arguments (e.g., line 103: `# 2000 values in 2010 dollars`).
- Prose between code chunks is well-written and pedagogically useful, explaining the distinction between prediction and explanation (lines 402-403, 506-511).

Minor issues:
1. **`Mclust()` is not explained on first use** (line 578). Students unfamiliar with model-based clustering would need context about what BIC selection means and how Mclust differs from k-means.
2. **`stargazer()` is not explained on first use** (line 137). A brief note about what it produces and why `type = s.type` is used would help.
3. **The `panel.cor` and `panel.smooth` helper functions** (lines 339-362) are defined inline in Part 2 rather than in a dedicated helper-functions section at the top of the file. Lab 5 places them at the top, which is cleaner.

## Package Consistency
**Minor issues found:**

1. **`library( knitr )` loaded (line 36) but `knitr::kable()` is used with namespace prefix** (line 697: `knitr::kable( group.results, ... )`). The namespace prefix makes the `library(knitr)` call technically unnecessary for that usage, though knitr is also needed for inline R evaluation. This is not a bug but is slightly inconsistent — either use `library(knitr)` and call `kable()` without prefix, or don't load it and keep the prefix.

2. **`library( scales )` loaded (line 39):** The `dollar()` function is used extensively (lines 143, 191, 197, 201, 599, 693). Correctly loaded. Good.

3. **`library( mclust )` loaded (line 40):** Used for `Mclust()` on line 578 and `fit$G` / `fit$classification` on lines 582-586. Correctly loaded, but the package itself is prohibited by the curriculum spec (see Deprecated section).

4. **No missing packages.** All functions used have corresponding library calls or base R availability.

## Inline R References

| Expression | Line | Object Exists? | Status |
|-----------|------|----------------|--------|
| `` `r nrow( d )` `` | 86 | `d` created at line 83 after filtering | OK |
| `` `r dollar( round( median( mhv.00, na.rm = TRUE ), 0 ) )` `` | 143 | `mhv.00` created at line 103 (standalone vector) | OK |
| `` `r dollar( round( median( mhv.10, na.rm = TRUE ), 0 ) )` `` | 143 | `mhv.10` created at line 104 (standalone vector) | OK |
| `` `r dollar( round( median( mhv.change, na.rm = TRUE ), 0 ) )` `` | 143 | `mhv.change` created at line 107 (standalone vector) | OK |
| `` `r round( median( mhv.growth, na.rm = TRUE ), 1 )` `` | 143 | `mhv.growth` created at line 113 (standalone vector) | OK |
| `` `r dollar( round( mean( mhv.change, na.rm = TRUE ), 0 ) )` `` | 201 | `mhv.change` exists as standalone vector | OK |
| `` `r dollar( round( median( mhv.change, na.rm = TRUE ), 0 ) )` `` | 201 | `mhv.change` exists as standalone vector | OK |
| `` `r round( median( mhv.growth, na.rm = TRUE ), 0 )` `` | 229 | `mhv.growth` exists as standalone vector | OK |
| `` `r round( summary( m1 )$adj.r.squared, 3 )` `` | 396 | `m1` created at line 380 | OK |
| `` `r round( summary( m2 )$adj.r.squared, 3 )` `` | 396 | `m2` created at line 381 | OK |
| `` `r nrow( d3 )` `` | 568 | `d3` created at lines 562-565 | OK |
| `` `r fit$G` `` | 586 | `fit` created at line 578 (`Mclust()` output) | OK |

All inline R references resolve to objects that exist at execution time. **However**, note that `mhv.00`, `mhv.10`, `mhv.change`, and `mhv.growth` on lines 143 and 201 reference the standalone vectors (created at lines 103-113), not the data frame columns (`d$mhv.00`, etc.). This works correctly because the standalone vectors remain in the environment, but it is worth noting for clarity — if students modify the code, they might not realize these inline references use the standalone vectors rather than the data frame columns.

## Format Consistency

| Element | Lab 1 (Reference) | Lab 6 | Match? |
|---------|-------------------|-------|--------|
| YAML title | `title: "Lab 01 — ..."` | `title: "Lab 06 -- ..."` | Minor: uses `--` instead of em dash `—` |
| YAML subtitle | `subtitle: "PAF 516"` | `subtitle: "PAF 516"` | Yes |
| YAML format.html | theme, highlight, toc, self-contained | Same, minus toc-title and number-sections | Close match |
| YAML execute | echo, warning, message, fig-width | echo, warning, message (fig-width under html) | NO — fig-width placement differs |
| Setup chunk | `#| label: setup`, `#| include: false`, knitr opts | Has setup chunk but only sets `s.type` | Partial |
| Chunk labels | `step.01`, `step.02`, etc. | `packages`, `load-data`, `mhv-variables`, etc. | Different convention (descriptive) |
| Section headers in code | `# ── Name ──` | `# ── Name ──` | Yes |
| Questions | Q1/Q2/Q3 format | **No questions section** | NO |
| Horizontal rules | `---` between sections | `---` between sections | Yes |
| Session info | Not in Lab 1 | Present at end (line 720-724) | Extra (acceptable) |

## Specific Issues

1. **Line 40: `library( mclust )` is prohibited.** The CLAUDE.md curriculum spec states: "No regression. No mclust. No complex clustering. Geospatial focus." Part 4 (lines 543-700) uses mclust for Gaussian mixture model clustering and must be redesigned or removed entirely. If clustering is needed, the curriculum spec for Lab 4 specifies spatial autocorrelation via spdep instead.

2. **Lines 59-84 (`load-data` chunk): Missing `#| results: hide`.** Data pull from GitHub URLs should suppress output per the standard.

3. **No standardized questions section.** The lab has a "Conclusion" section (lines 703-715) but no Q1/Q2/Q3 questions. It must have:
   - Q1: Interpret the key difference between the levels-based and changes-based regression results
   - Q2: Modify the analysis (with FULL CODE AND OUTPUT) — e.g., add a 4th predictor to all models, or rerun for a different metro area
   - Q3: Interpret how the modification changed the results

4. **Lines 106-113: Logic bug in mhv.change vs filter order.** `mhv.change` is computed on line 107 BEFORE `mhv.00` values under $1,000 are set to NA on line 110. This means tracts with sub-$1,000 home values retain their computed `mhv.change` but get NA for `mhv.growth`. Lab 5 documents this issue explicitly and notes it as an intentional deviation from the original code, but Lab 6 does not document it. For consistency, either (a) filter first and then compute both `mhv.change` and `mhv.growth`, or (b) add a comment explaining the ordering choice.

5. **YAML lines 12-13: `fig-width` and `fig-height` under `format: html:`** — The standard places these under `execute:` (as Lab 5 does). While valid in Quarto under either location, this is inconsistent with the template. Move to `execute:` block.

6. **YAML line 2: `--` instead of `—`** — The title uses two ASCII hyphens (`Lab 06 -- Solutions`) instead of an em dash (`Lab 06 — Solutions`) as used in Lab 5. Minor typographic inconsistency.

7. **Setup chunk (lines 43-49) is incomplete.** It has `#| include: false` (good) but only sets `s.type <- "html"`. It is missing:
   - `knitr::opts_chunk$set(echo=TRUE, message=FALSE, warning=FALSE, fig.width=10)`
   - `options(tigris_use_cache = TRUE)`

8. **Line 578: `Mclust()` with no seed comment.** A `set.seed(1234)` is set on line 577, which is good. However, there is no comment explaining WHY a seed is needed for Mclust (it uses EM algorithm with random initialization). Minor.

9. **Lines 618-621: Hardcoded group renaming.** The group labels ("Low Distress", "High Poverty", "High Vacancy") are hardcoded based on a specific Mclust output. If the number of clusters changes (Mclust auto-selects), these lines will either miss groups or mislabel them. The comment on line 621 acknowledges this ("Add more lines if your model produces more groups") but a more robust approach would be programmatic labeling.

10. **Part 4 regression uses a no-intercept model** (line 635: `mhv.change ~ cluster.group - 1`). This is a valid modeling choice and is explained in the text, but it is not standard practice and may confuse students who have not seen the `-1` syntax before. A brief comment explaining why the intercept is suppressed would help.

11. **The lab is primarily a regression lab**, with Parts 2-3 running OLS regression and Part 4 combining clustering with regression. The CLAUDE.md spec says "No regression" for the redesigned curriculum. While this is the current/old version being reviewed (not the redesigned version), it is worth flagging that the entire analytical framework conflicts with the redesign direction.

## Verdict
**NEEDS REVISION**

Priority fixes:
1. Remove `library(mclust)` and redesign or remove Part 4 (clustering section) — mclust is explicitly prohibited
2. Add `#| results: hide` to the `load-data` chunk
3. Add standardized Q1/Q2/Q3 questions section with full modification code in Q2
4. Complete the setup chunk: add `knitr::opts_chunk$set(...)` and `options(tigris_use_cache = TRUE)`
5. Move `fig-width` and `fig-height` from `format: html:` to `execute:` in the YAML
6. Fix or document the `mhv.change` computation order relative to the sub-$1,000 filter
7. Fix the em dash inconsistency in the YAML title
