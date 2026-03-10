# Lab 1 — Code Review

## Summary
**NEEDS REVISION** — Several output suppression gaps, missing `# ──` section headers, missing `toc: true` is present but YAML lacks `toc` on Lab 2 (noted for cross-reference), one data-pull chunk without `#| results: hide`, questions do not follow the standardized Q1/Q2/Q3 format, and `library(sf)` is missing despite implicit use through tidycensus geometry.

## Deprecated Functions/Packages
None found. The code correctly uses `pivot_wider()` instead of `spread()`, `linewidth` instead of `size` for line geoms, and does not load any deprecated spatial packages (sp, rgdal, maptools, tmap, mclust). No use of `aes_string()`, `summarise_each()`, `funs()`, or `do()`.

## Output Suppression

**Issues found:**

1. **Line 49-56 (`browse-variables` chunk):** Uses `#| eval: false` so no runtime issue, but `load_variables()` would produce console output if ever toggled to eval. Acceptable as-is since eval is false.

2. **Line 58-87 (`step.01` chunk):** Calls `get_acs()` but does NOT have `#| results: hide`. This is the primary data pull for the entire lab. When rendered, students will see the full download progress bar output. **This must be fixed.**

3. **Line 96-137 (`step.02` chunk):** No data pull, but no `#| results: hide` needed here. Fine.

4. **Line 152-162 (`step.03` chunk):** Calls `print(alpha_result)` — this is analysis output that SHOULD display. Correct.

5. **Line 170-178 (`alpha-summary` chunk):** Uses `cat()` for inline reporting. Correct.

6. **Line 27-36 (`packages` chunk):** Does NOT have `#| results: hide` or `#| include: false`. Package loading messages from `library()` calls will appear in rendered output. The YAML `message: false` and `knitr::opts_chunk$set(message=F)` should suppress these globally, but belt-and-suspenders would add `#| message: false` or `#| results: hide` here. **Minor risk** — likely suppressed by global settings, but worth verifying.

7. **Setup chunk (line 20-24):** Correctly has `#| include: false`. Good.

8. **YAML (lines 10-14):** Has `warning: false` and `message: false` under `execute:`. Good.

9. **Missing:** `options(tigris_use_cache = TRUE)` is NOT set in the setup chunk. This means Census geometries will re-download on every render, and progress bars may leak through. **Must be added to setup chunk.**

## Code Annotations

**Assessment: SPARSE — needs improvement.**

1. **Missing `# ──` section headers:** The lab uses markdown headers (`# Step 1:`, `# Step 2:`, etc.) but inside code chunks there are no `# ── Section Name ──` comment-style headers as required by the annotation standard. Every major section within code should have this format.

2. **Comment blocks before code:** Some chunks have 1-line comments (e.g., line 63: `# Define our indicator variables...`, line 78: `# Retrieve data with geometry...`), but the standard requires 2-3 line comment blocks explaining WHAT and WHY. Most comments are single-line.

3. **Good inline comments:** Lines 65-75 have good inline comments on the variable definitions. Lines 110-116 have good inline comments on the mutate operations. Line 120-121 explains reverse coding. These are well done.

4. **Missing post-operation comments:** After `get_acs()` (line 87), there is no comment explaining what the resulting data frame looks like (e.g., "The result is a long-format sf data frame with one row per variable per tract"). After `pivot_wider()` (line 104), same gap.

5. **First-use explanations:** `get_acs()` is not explained on first use (what it returns, why we need `geometry=TRUE`). `pivot_wider()` gets a note about not being `spread()` but no explanation of what it does. `psych::alpha()` is not explained. `corrplot()` is not explained. `scale()` is not explained.

## Package Consistency

**Issues found:**

1. **`library(sf)` is missing.** The code uses `geom_sf()` (line 243) which comes from ggplot2's sf integration, and sf geometry operations are used implicitly through tidycensus. While `geom_sf()` works as long as sf is installed (it's loaded by tidycensus behind the scenes), explicit `library(sf)` is best practice and required for transparency. Additionally, line 222 in the compare step uses `sf::st_drop_geometry()` — the `sf::` prefix makes it work without library(sf), but this is inconsistent: either load sf explicitly or use the prefix everywhere.

2. **`library(ggplot2)` on line 35 is redundant** since `library(tidyverse)` on line 30 already loads ggplot2. Not a bug, but unnecessary.

3. **`library(patchwork)` is missing** — the CLAUDE.md spec lists patchwork as a Lab 1 package, but it is not loaded or used. If multi-scale maps are added (as specified in the lab arc), patchwork will be needed.

## Inline R References

| Expression | Location | Object Exists? | Status |
|-----------|----------|----------------|--------|
| `` `r round(alpha_value, 2)` `` | Line 261 | `alpha_value` created at line 176 | OK |
| `` `r ifelse(alpha_value > 0.7, ...)` `` | Line 261 | `alpha_value` created at line 176 | OK |
| `` `r "south Phoenix and parts of central Mesa/Tempe"` `` | Line 300 | Hardcoded string, not a variable reference | OK (but lazy — not dynamically generated) |

All inline R references resolve to objects that exist at execution time. The hardcoded string on line 300 is technically valid but defeats the purpose of inline R.

## Format Consistency

This IS Lab 1, so it serves as the reference. Noting the format for cross-comparison:

- **YAML:** title, subtitle, format (html with theme/highlight/toc/self-contained), execute block. Good structure.
- **Setup chunk:** `#| label: setup`, `#| include: false`, sets knitr opts. Good.
- **Chunk labels:** Uses `step.01`, `step.02`, `step.04a`, `step.04b`, `step.04c`. Dot-separated convention.
- **Questions:** Uses Q1 (1a, 1b, 1c), Q2 (2a, 2b, 2c), Q3 (3a, 3b) format. **This does NOT match the standardized format.** The standard requires: Q1 = interpret results, Q2 = modify the analysis (with FULL CODE AND OUTPUT), Q3 = interpret modified results. Current Lab 1 has no modification question with code — Q2 asks about variable selection (no code), and Q3 asks forward-looking conceptual questions (no modification).
- **Redundant `---`:** Line 18 has a bare `---` horizontal rule between the YAML and first chunk. Harmless but unnecessary.

## Specific Issues

1. **Line 59, `step.01` chunk: Missing `#| results: hide`** — The `get_acs()` call will print download progress bars in rendered HTML. Add `#| results: hide` to this chunk.

2. **Line 23, setup chunk: Missing `options(tigris_use_cache = TRUE)`** — Without this, Census geometries re-download every render and progress bars may leak. Add to setup chunk.

3. **Lines 255-301, Questions section: Non-standard format** — Questions do not follow the Q1 (interpret) / Q2 (modify with FULL CODE) / Q3 (interpret modification) pattern. Q2 should ask students to modify the analysis (e.g., add a 6th variable, recompute alpha) and include complete solution code. Q3 should ask them to interpret the modification.

4. **Line 35: Redundant `library(ggplot2)`** — Already loaded by `library(tidyverse)`. Remove for cleanliness.

5. **Line 54: ACS year 2021 in `load_variables()` but line 83 uses `year = 2021` in `get_acs()`** — The CLAUDE.md spec says to use `year = 2023` (the most recent ACS 5-year estimates, 2019-2023). Currently hardcoded to 2021. This may be intentional for the existing version, but conflicts with the curriculum spec.

6. **Line 73: Variable `B27010_017`** — This appears to be "no health insurance, ages 18-34" which is only a subset of the uninsured population. The comment says "Population without health insurance (18-34)" which is accurate, but this means the insurance variable only captures one age group, potentially underestimating uninsurance. Worth noting whether this is intentional or if a broader variable like B27010 aggregates should be used.

7. **No multi-scale mapping** — The CLAUDE.md spec requires Lab 1 to include US county-level and Maricopa CBG-level maps in addition to the existing tract-level map. These are not present.

8. **Line 300: Hardcoded geographic interpretation** — The inline R expression `r "south Phoenix and parts of central Mesa/Tempe"` is just a hardcoded string wrapped in inline R for no reason. Should either be plain text or actually computed.

## Verdict
**NEEDS REVISION**

Priority fixes:
1. Add `#| results: hide` to the `step.01` data pull chunk
2. Add `options(tigris_use_cache = TRUE)` to setup chunk
3. Restructure questions to standardized Q1/Q2/Q3 format (Q2 must include full modification code)
4. Add `# ──` section headers inside code chunks per annotation standard
5. Add `library(sf)` to the packages chunk
6. Expand comment blocks to 2-3 lines where currently single-line
