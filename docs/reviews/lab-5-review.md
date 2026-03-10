# Lab 5 — Code Review

## Summary
**NEEDS REVISION** — Lab 5 has no setup chunk, no `#| results: hide` on the data pull chunk, uses the deprecated `sample_n()`, has no `# ──` section headers (uses `# ----` instead), and is missing the standardized Q1/Q2/Q3 questions section entirely. The lab also lacks `options(tigris_use_cache = TRUE)` (though it does not use tidycensus, so this is minor). The overall structure is a well-annotated regression walkthrough but does not conform to the PAF 516 template.

## Deprecated Functions/Packages
**Issues found:**

1. **Line 296: `sample_n( plotd, 5000 )`** — `sample_n()` was deprecated in dplyr 1.0.0 (June 2020) in favor of `slice_sample(n = 5000)`. Lab 6 already uses `slice_sample()` with a comment noting the replacement, so this is inconsistent across labs.

No other deprecated functions found. No use of `spread()`, `gather()`, `summarise_each()`, `funs()`, `do()`, `aes_string()`, or deprecated spatial packages (sp, rgdal, maptools, tmap, mclust).

## Output Suppression
**Issues found:**

1. **No setup chunk exists.** The standard requires a `#| label: setup` / `#| include: false` chunk with `knitr::opts_chunk$set(...)` and `options(tigris_use_cache = TRUE)`. Lab 5 has no setup chunk at all — the first chunk is `packages` (line 26).

2. **Line 26-37 (`packages` chunk): Missing `#| include: false` or `#| results: hide`.** The `library()` calls for dplyr, pander, and stargazer may produce loading messages. The YAML global `message: false` should suppress these, but there is no belt-and-suspenders protection.

3. **Line 98-201 (`load-data` chunk): Missing `#| results: hide`.** This chunk loads three RDS files from GitHub URLs via `readRDS(gzcon(url(...)))`. While RDS loading is typically silent (unlike `get_acs()` progress bars), this is a data pull chunk and should have `#| results: hide` per the standard. More importantly, lines 191-200 compute metro-level summaries with `group_by()` / `mutate()` — if any messages or warnings are produced (e.g., from NA handling), they would be visible.

4. **YAML (lines 14-19):** Has `warning: false` and `message: false` under `execute:`. Has `fig-width: 10` and `fig-height: 6`. Good.

## Code Annotations
**Assessment: ADEQUATE but uses non-standard header format.**

Strengths:
- Every major code block has a 2-3 line comment block explaining WHAT and WHY. Examples: lines 108-112 (LTDB description), lines 141-143 (why convert to percentages), lines 152-164 (inflation adjustment with source citation), lines 166-171 (why filter sub-$1000 values), lines 407-412 (IQR effect size rationale).
- Good inline comments on non-obvious arguments (e.g., line 147: `# unemployment rate (%)`, line 106: `# Set to "html" for rendered output`).
- Functions like `jplot()`, `panel.cor()`, and `panel.smooth()` are well-documented with purpose comments.

Issues:
1. **No `# ──` section headers.** Lab 5 uses `# ---- Section Name ----` format throughout (e.g., line 29: `# ---- Required packages ----`, line 108: `# ---- Load LTDB census data from GitHub ----`). The standard requires `# ── Section Name ──` with box-drawing characters. Lab 6 correctly uses the `# ──` format.
2. **`stargazer()` is not explained on first use** (line 351). Students unfamiliar with stargazer would benefit from a brief note about what it does and why `type = s.type` is set.
3. **`lowess()` / `lowess` referenced but not explained** on first use in the helper functions (line 71). The linearity section (line 313) mentions lowess but assumes students know what it is.

## Package Consistency
**No issues found.** The lab loads `dplyr`, `pander`, and `stargazer`, and all functions used in the code are either from these packages or from base R. Specifically:
- `filter()`, `select()`, `mutate()`, `group_by()`, `sample_n()` — dplyr
- `pander()` — pander
- `stargazer()` — stargazer
- `hist()`, `par()`, `plot()`, `cor()`, `cor.test()`, `lm()`, `quantile()`, `pairs()` — base R

No sf, ggplot2, or other spatial functions are used without corresponding `library()` calls.

## Inline R References

| Expression | Line | Object Exists? | Status |
|-----------|------|----------------|--------|
| `` `r round( cor( d$log.p.unemp, d$log.pov.rate, use = "complete.obs" ), 1 )` `` | 303 | `d$log.p.unemp` created at line 248, `d$log.pov.rate` created at line 250 | OK |
| `` `r round( cor( df$MHV.Change.00.to.10, df$MHV.Growth.00.to.10, use = "complete.obs" ), 2 )` `` | 373 | `df` created at lines 341-349 with both columns | OK |
| `` `r round( summary( m1 )$adj.r.squared, 3 )` `` | 398 | `m1` created at line 387 | OK |
| `` `r round( summary( m2 )$adj.r.squared, 3 )` `` | 398 | `m2` created at line 388 | OK |

All inline R references resolve to objects that exist at execution time. No issues found.

## Format Consistency

| Element | Lab 1 (Reference) | Lab 5 | Match? |
|---------|-------------------|-------|--------|
| YAML title | `title: "Lab 01 — ..."` | `title: "Lab 05 — ..."` | Yes |
| YAML subtitle | `subtitle: "PAF 516"` | `subtitle: "PAF 516"` | Yes |
| YAML format.html | theme, highlight, toc, self-contained | Same + toc-title, number-sections | Minor extras |
| YAML execute | echo, warning, message, fig-width | Same + fig-height | Yes (minor addition) |
| Setup chunk | `#| label: setup`, `#| include: false` | **Missing entirely** | NO |
| Chunk labels | `step.01`, `step.02`, etc. | `packages`, `helper-functions`, `load-data`, `skew-raw`, etc. | Different convention (descriptive vs numbered) |
| Section headers | `# ── Name ──` | `# ---- Name ----` | NO — wrong format |
| Questions | Q1/Q2/Q3 format (interpret/modify/interpret) | **No questions section at all** | NO |
| Horizontal rules | `---` between sections | `---` between sections | Yes |

## Specific Issues

1. **Line 296: Deprecated `sample_n()`** — Replace with `slice_sample(n = 5000)` for consistency with dplyr 1.0+ and with Lab 6 which already uses the modern function.

2. **No setup chunk** — Add a setup chunk after the YAML and before the packages chunk with `#| label: setup`, `#| include: false`, `knitr::opts_chunk$set(echo=TRUE, message=FALSE, warning=FALSE, fig.width=10)`.

3. **Lines 98-201 (`load-data` chunk): Missing `#| results: hide`** — Data pull from GitHub URLs should suppress output per the standard.

4. **No standardized questions section** — The lab ends abruptly after Part 07 (Effect Sizes) at line 445. It must have:
   - Q1: Interpret the regression results and effect sizes
   - Q2: Modify the analysis (with FULL CODE AND OUTPUT in solutions) — e.g., add a 4th predictor, rerun models, recompute effect sizes
   - Q3: Interpret how the modification changed the results

5. **All section headers use `# ----` instead of `# ──`** — 30+ occurrences throughout the file. Should be converted to `# ── Section Name ──` format for consistency with the annotation standard and with Lab 6.

6. **Line 107, mhv.change calculation order** — `mhv.change` is computed (line 176) BEFORE `mhv.00` values under $1,000 are set to NA (line 173). This means `mhv.change` retains computed values for tracts where `mhv.00` was sub-$1,000. Lab 5 documents this explicitly (lines 166-171), noting it was an intentional fix over the original code. However, the fix is incomplete: `mhv.change` should also be recomputed after filtering, or those tracts should have `mhv.change` set to NA as well. Currently, those tracts have a valid `mhv.change` but NA `mhv.growth`, which is inconsistent.

7. **Line 198: `metro.mhv.growth` double-percentage** — Line 198 computes `metro.mhv.growth = 100 * median( mhv.growth, ... )`. But `mhv.growth` is already in percentage terms (computed on line 177 as `100 * ( mhv.change / mhv.00 )`). This multiplies by 100 twice, so `metro.mhv.growth` is 100x too large. Should be `metro.mhv.growth = median( mhv.growth, na.rm = TRUE )` without the `100 *`.

8. **No `options(tigris_use_cache = TRUE)` in any chunk** — While Lab 5 does not use tidycensus, the standard requires this in the setup chunk as a global setting. Minor issue but worth including for consistency.

## Verdict
**NEEDS REVISION**

Priority fixes:
1. Add a `#| label: setup` / `#| include: false` chunk with `knitr::opts_chunk$set(...)` and `options(tigris_use_cache = TRUE)`
2. Add `#| results: hide` to the `load-data` chunk
3. Replace `sample_n()` with `slice_sample()` on line 296
4. Convert all `# ----` section headers to `# ──` format
5. Add standardized Q1/Q2/Q3 questions section with full modification code in Q2
6. Fix the double-percentage bug on line 198 (`metro.mhv.growth`)
7. Consider recomputing `mhv.change` after the sub-$1,000 filter for consistency with `mhv.growth`
