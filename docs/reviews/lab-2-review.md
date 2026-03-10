# Lab 2 — Code Review

## Summary
**NEEDS REVISION** — Multiple data-pull chunks missing `#| results: hide`, no `# ──` section headers in code, questions do not follow the standardized Q1/Q2/Q3 format, `options(tigris_use_cache = TRUE)` missing from setup, YAML missing `toc: true`, and code annotations are sparse. The lab content itself (house-price-to-income ratio) does not match the curriculum spec (which calls for cartographic design and multi-scale visual analytics using the economic hardship index), but this review focuses on code quality rather than curriculum alignment.

## Deprecated Functions/Packages
None found. The code correctly uses `pivot_wider()` instead of `spread()` (explicitly noted in comments on lines 105 and 186). No use of `aes_string()`, `summarise_each()`, `funs()`, `do()`, or deprecated packages (sp, rgdal, maptools, tmap, mclust).

## Output Suppression

**Issues found:**

1. **Lines 43-63 (`var-search` chunk):** Calls `load_variables()` which downloads the full ACS variable table. Does NOT have `#| results: hide`. This will print download progress and potentially a large data frame. **Must add `#| results: hide`.**

2. **Lines 79-94 (`get-acs-2017` chunk):** Calls `get_acs()` — the primary data pull. Does NOT have `#| results: hide`. Students will see download progress bars. **Must add `#| results: hide`.**

3. **Lines 114-130 (`explore-2017` chunk):** Calls `head()` which is analysis output that should display. This chunk is correctly left without `#| results: hide`. Good.

4. **Lines 134-148 (`map-2017` chunk):** Map output — should display. Correct.

5. **Lines 172-208 (`get-acs-2012` chunk):** Calls `get_acs()` AND produces a map. This chunk does too much — it pulls data AND visualizes it in a single chunk. The data pull portion will show progress bars. **Must either add `#| results: hide` (which would also hide the map) or split into separate chunks: one for data pull (hidden) and one for visualization (shown).** Best practice: split the chunk.

6. **Lines 257-280 (`get-acs-az` chunk):** Calls `get_acs()` — correctly HAS `#| results: hide` on line 261. However, this also calls `summary()` on line 279, whose output will be suppressed by `results: hide`. If the summary should be visible, it needs to be in a separate chunk. **Split into two chunks or accept that summary output is hidden.**

7. **Lines 27-33 (`packages` chunk):** No `#| results: hide`. Package loading messages depend on global `message: false` setting for suppression. Likely fine due to YAML settings.

8. **Setup chunk (lines 21-24):** Correctly has `#| include: false`. Good.

9. **YAML (lines 11-15):** Has `warning: false` and `message: false`. Good.

10. **Missing:** `options(tigris_use_cache = TRUE)` is NOT in the setup chunk. Geometries will re-download every render. **Must be added.**

## Code Annotations

**Assessment: SPARSE — needs significant improvement.**

1. **Missing `# ──` section headers:** No code chunk uses the `# ── Section Name ──` comment style. All section breaks are markdown headers outside code chunks (`# Step 1:`, `# Step 2:`, etc.). Inside code chunks, there are only single-line comments.

2. **Comment quality:** Most comments are single-line and adequate but do not meet the 2-3 line standard:
   - Line 48: `# Search for variable names...` — single line, adequate.
   - Line 84: `# Define variables with readable names...` — single line, adequate.
   - Line 88: `# Retrieve county-level data...` — single line, adequate.
   - Line 104-105: `# Transform from long to wide...` with note about pivot_wider — good, 2 lines.
   - Lines 220-221: `# Prepare 2017 data for joining...` — single line.

3. **Missing explanations for new functions:**
   - `load_variables()` (line 49) — not explained. What does it return? Why do we cache it?
   - `get_acs()` (line 89) — not explained on first use. What do the arguments mean?
   - `geom_sf()` (line 141) — not explained. What makes it different from `geom_polygon()`?
   - `coord_sf(datum = NA)` (line 142) — not explained. What does `datum = NA` do?
   - `scale_fill_viridis()` (line 147) — not explained. Why `direction = -1`?
   - `sf::st_drop_geometry()` (line 222) — not explained. Why do we need to drop geometry?
   - `full_join()` (line 233) — not explained.
   - `grepl()` (line 56) — not explained.

4. **No post-operation comments:** After data pulls, there is no comment explaining the shape/structure of the resulting data frame.

## Package Consistency

**Issues found:**

1. **`library(sf)` is missing.** The code uses `sf::st_drop_geometry()` on lines 222 and 229 with explicit namespace prefix, and `geom_sf()` on lines 141, 201, which works through ggplot2. While the `sf::` prefix and ggplot2 integration avoid runtime errors, the sf package should be loaded explicitly since it is a core dependency for spatial operations. The curriculum spec lists sf as a required package for all labs.

2. **All loaded packages are used:**
   - `tidycensus` — used for `get_acs()`, `load_variables()`. OK.
   - `tidyverse` — used for dplyr verbs, ggplot2, tidyr. OK.
   - `viridis` — used for `scale_fill_viridis()`. OK.

3. **No unnecessary packages loaded.** Good.

## Inline R References

| Expression | Location | Object Exists? | Status |
|-----------|----------|----------------|--------|
| `` `r CenDF.hl$NAME[1]` `` | Line 157 | `CenDF.hl` created at line 127 | OK |
| `` `r CenDF.lh$NAME[1]` `` | Line 157 | `CenDF.lh` created at line 121 | OK |
| `` `r round(mean(CenDF$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 157 | `CenDF` created at line 106 | OK |
| `` `r which(CenDF.hl$NAME == "Maricopa County, Arizona")` `` | Line 161 | `CenDF.hl` created at line 127 | **CAUTION** — `which()` returns an integer index. If Maricopa County is not in the data (name mismatch), this returns `integer(0)`, which will render as blank. Should add error handling or verify exact NAME string. |
| `` `r round(CenDF$HHInc_HousePrice_Ratio[CenDF$NAME == "Maricopa County, Arizona"], 2)` `` | Line 161 | `CenDF` exists | **CAUTION** — Same name-matching risk. Also, `CenDF` is an sf object; subsetting by NAME may return multiple rows if geometry creates duplicates. Likely fine but fragile. |
| `` `r which(CenDF.hl$NAME == "Los Angeles County, California")` `` | Line 165 | `CenDF.hl` exists | **CAUTION** — Same `which()` fragility as above. |
| `` `r CenDF.12.hl$NAME[1]` `` | Line 210 | `CenDF.12.hl` created at line 197 | OK |
| `` `r CenDF.12.lh$NAME[1]` `` | Line 210 | `CenDF.12.lh` created at line 192 | OK |
| `` `r round(both.year$HHInc_HousePrice_Ratio.d[both.year$NAME == "Maricopa County, Arizona"][1], 2)` `` | Line 251 | `both.year` created at line 233 | **CAUTION** — `NAME` column only comes from `df.17` (the left side of the join). If the NAME column is present and the county exists, this works. The `[1]` indexing is good defensive coding. OK but fragile. |
| `` `r round(both.year$HHInc_HousePrice_Ratio.d[both.year$NAME == "Los Angeles County, California"][1], 2)` `` | Line 251 | `both.year` exists | Same as above. OK but fragile. |
| `` `r round(min(CenDF.az$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 283 | `CenDF.az` created at line 273 | OK |
| `` `r round(max(CenDF.az$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 283 | `CenDF.az` exists | OK |
| `` `r round(median(CenDF.az$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 283 | `CenDF.az` exists | OK |
| `` `r round(mean(CenDF.az$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 283 | `CenDF.az` exists | OK |
| `` `r round(sd(CenDF.az$HHInc_HousePrice_Ratio, na.rm=TRUE), 2)` `` | Line 283 | `CenDF.az` exists | OK |

All inline R references resolve to objects that exist. Several use `which()` or name-matching subsetting that could silently fail if county names don't match exactly — these are fragile but technically functional.

## Format Consistency

Comparing Lab 2 against Lab 1 (the reference):

| Element | Lab 1 | Lab 2 | Match? |
|---------|-------|-------|--------|
| YAML title format | `"Lab 01 — Solutions: ..."` | `"Lab 02 — Solutions: ..."` | Yes |
| YAML subtitle | `"PAF 516"` | `"PAF 516"` | Yes |
| YAML theme | `readable` | `readable` | Yes |
| YAML highlight-style | `tango` | `tango` | Yes |
| YAML toc | `true` | **MISSING** | **NO** |
| YAML self-contained | `true` | `true` | Yes |
| YAML execute block | Present with all 4 fields | Present with all 4 fields | Yes |
| Setup chunk | `#| include: false` with knitr opts | Same | Yes |
| Packages chunk | Separate `#| label: packages` chunk | Same | Yes |
| API key chunk | Separate `#| label: api-key` chunk | Same | Yes |
| Chunk label convention | `step.01`, `step.02`, etc. | Mixed: `var-search`, `get-acs-2017`, `step.01` style absent | **NO** |
| Question format | Q1 (1a,1b,1c), Q2 (2a,2b,2c), Q3 (3a,3b) | Q1 (1a,1b,1c), Q2 (2a,2b), Q3 (3a,3b) | Partial |
| Standardized Q format | Not followed (no modify+code Q) | Not followed | Both non-compliant |
| Stray `---` after YAML | Present (line 18) | Present (line 19) | Yes (both have it) |
| Revision comment header | Not present | Present (lines 1-2) | Lab 2 has extra metadata |

**Key format differences:**
1. Lab 2 is missing `toc: true` in the YAML — Lab 1 has it.
2. Lab 2 uses descriptive chunk labels (`var-search`, `get-acs-2017`, `explore-2017`) instead of Lab 1's `step.XX` convention. This is actually more readable, but inconsistent.
3. Neither lab follows the standardized Q1 (interpret) / Q2 (modify with full code) / Q3 (interpret modification) format.

## Specific Issues

1. **Lines 43-63, `var-search` chunk: Missing `#| results: hide`** — `load_variables()` downloads the full ACS variable list and will produce console output. Add `#| results: hide`.

2. **Lines 79-94, `get-acs-2017` chunk: Missing `#| results: hide`** — `get_acs()` will print download progress bars. Add `#| results: hide`.

3. **Lines 172-208, `get-acs-2012` chunk: Data pull and map in same chunk** — This chunk pulls ACS data (which needs `results: hide`) AND creates a map (which should display). Must be split into two chunks: one for the data pull with `#| results: hide`, one for the map without.

4. **Lines 257-280, `get-acs-az` chunk: `summary()` output hidden** — The `#| results: hide` on this chunk correctly suppresses the `get_acs()` progress bars, but also suppresses the `summary()` output on line 279. Either move the summary to a separate chunk or accept that students won't see it in the rendered HTML.

5. **Line 24, setup chunk: Missing `options(tigris_use_cache = TRUE)`** — Census geometries will re-download on every render. Add to setup.

6. **YAML missing `toc: true`** — Lab 1 has it; Lab 2 should match for consistency.

7. **Lines 152-165, Question 1: Non-standard format** — Currently has sub-questions 1a, 1b, 1c asking about specific counties and rankings. The standardized format requires Q1 to be a general interpretation question. The county-specific questions are good content but should be restructured.

8. **Lines 169-251, Question 2: Close to standard but not quite** — Q2 asks students to change the year (temporal analysis) and includes full code, which is close to the "modify" pattern. However, the structure mixes instructions with answers and sub-questions in a way that doesn't cleanly separate the modification prompt from the interpretation.

9. **Lines 253-308, Question 3: Close to standard but not quite** — Q3 asks students to change geography (county to tract), which is a good modification. But under the standardized format, Q3 should be interpreting Q2's modification, not a new modification. This is effectively a second modification question.

10. **Lines 85-86: Variable name mismatch** — The variable is named `HHIncome` but it pulls `B19049_001` which is "Median Household Income by Age of Householder" (total), not `B19013_001` which is the standard "Median Household Income." The `B19049_001` variable is slightly different — it's the total row from the income-by-age table. While it usually gives similar values, `B19013_001` is the canonical median household income variable. This may cause subtle discrepancies.

11. **Line 49: ACS year 2017** — The `load_variables()` call uses year 2017, and the entire lab is built around 2017 data. The CLAUDE.md spec calls for `year = 2023` (most recent ACS). This is a curriculum alignment issue rather than a code bug.

12. **Lines 288-306, `compare-geography` chunk: Fragile comparison table construction** — The `rbind()` call on lines 293-300 creates a comparison table by binding `summary()` outputs. The county-level row has `c(summary(...), 0)` which manually appends a 0 for NAs. This is fragile — if `summary()` output format changes (e.g., no NAs column), the dimensions won't match. The `[7]` column rename on line 303 is also brittle.

13. **Line 1-2: Revision metadata comments** — Lab 2 has HTML comment metadata (`<!-- REVISED: ... -->`) that Lab 1 does not. Not a problem, but inconsistent.

## Verdict
**NEEDS REVISION**

Priority fixes:
1. Add `#| results: hide` to `var-search` and `get-acs-2017` chunks
2. Split `get-acs-2012` chunk into data-pull chunk (with `#| results: hide`) and map chunk (without)
3. Split `get-acs-az` chunk so `summary()` output displays separately from the hidden data pull
4. Add `options(tigris_use_cache = TRUE)` to setup chunk
5. Add `toc: true` to YAML header
6. Add `library(sf)` to packages chunk
7. Add `# ──` section headers and expand code annotations to 2-3 lines per standard
8. Restructure questions to standardized Q1 (interpret) / Q2 (modify with full code) / Q3 (interpret modification) format
