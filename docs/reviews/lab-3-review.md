# Lab 3 — Code Review

## Summary
**NEEDS REVISION** — Lab 3 loads multiple deprecated/retired packages (sp, tmap, mclust, geojsonio), lacks a proper `#| include: false` setup chunk, is missing `#| results: hide` on the data-loading chunk, has no inline R references (so no risk there), and does not follow the standardized Q1/Q2/Q3 question format. The question section is a reading-response exercise rather than an analytical modification task with code. Annotations are present and adequate in most sections but missing `# ──` section headers inside code chunks.

## Deprecated Functions/Packages

**Critical issues found:**

1. **Line 32: `library(tmap)`** — tmap is listed as a deprecated/disallowed package per the curriculum spec. The lab uses it extensively for choropleth mapping (lines 156-158, 169-172, 183-184, 253-257). All tmap calls should be replaced with ggplot2 + `geom_sf()` or leaflet.

2. **Line 49: `library(geojsonio)`** — Relies on V8/jsonlite for reading GeoJSON from a URL. This is fragile (V8 installation fails frequently on student machines, as acknowledged in the callout on line 68). Should use `sf::st_read()` instead, which reads GeoJSON natively.

3. **Line 50: `library(sp)`** — The sp package is retired from CRAN. The lab explicitly loads it and then uses sp-specific syntax on line 205 (`phx@data` S4 slot access). Should use `sf::st_drop_geometry()` instead.

4. **Line 55: `library(mclust)`** — mclust (Gaussian mixture model clustering) is explicitly prohibited by the curriculum spec ("No regression. No mclust. No complex clustering. Geospatial focus."). The entire analytical approach of this lab conflicts with the redesigned curriculum.

5. **Line 130: `geojson_read(x = github.url, what = "sp")`** — Reads data into an sp object. Should use `st_read()` to read directly into sf.

6. **Line 205: `d1 <- phx@data`** — S4 slot access is sp syntax. Should use `st_drop_geometry()`.

7. **Lines 169, 175: `tmap_mode("view")`** — Interactive tmap calls. These are set to `eval: false` so they don't break rendering, but they should be replaced with leaflet if interactive mapping is needed.

8. **No use of `aes_string()`** — Good. ggplot2 calls use standard `aes()`.

9. **No use of `spread()`, `gather()`, `summarise_each()`, `funs()`, or `do()`** — Good. Line 321 correctly uses `summarise(across(everything(), mean))` instead of the deprecated `summarise_each(funs(mean))`. This replacement is explicitly noted in the comments (line 317).

## Output Suppression

**Issues found:**

1. **Lines 25-34 (`tmap-reset` chunk):** Has `#| include: false`. Good.

2. **Lines 45-65 (`load-packages` chunk):** Does NOT have `#| include: false` or `#| results: hide`. Package loading messages from `library()` calls will appear in rendered output unless suppressed by the global YAML settings. The YAML does have `message: false` (line 18), which should suppress most `library()` messages. Acceptable but could be more defensive.

3. **Lines 81-117 (`data-dictionary` chunk):** Has `#| echo: false`. Appropriate for a display-only chunk.

4. **Lines 123-134 (`load-shapefile` chunk):** Calls `geojson_read()` which downloads data from GitHub. Does NOT have `#| results: hide`. The `print(plot(phx))` on line 133 is intentional output, but the download itself may produce progress messages. **Should add `#| results: hide` or split into a download chunk (hidden) and a plot chunk (visible).**

5. **Lines 136-158 (`tmap-static` chunk):** No data pull, produces a map. Fine.

6. **Lines 191-232 (`prepare-and-cluster` chunk):** No external data pull, runs Mclust. The `summary(fit)` on line 231 is intentional output. Fine.

7. **Lines 551-559 (`aux-data-dictionary-remote` chunk):** Calls `read.csv()` from a URL. Does NOT have `#| results: hide`. The CSV download may produce output. **Should add `#| results: hide` or suppress.**

8. **YAML (lines 15-19):** Has `warning: false` and `message: false`. Good.

9. **Missing: `options(tigris_use_cache = TRUE)` is NOT set anywhere.** While this lab doesn't use tidycensus directly, the standard requires it in every setup chunk.

10. **Missing: No proper setup chunk.** The curriculum standard requires a chunk labeled `setup` with `#| include: false` that sets `knitr::opts_chunk$set(...)` and `options(tigris_use_cache = TRUE)`. The `tmap-reset` chunk (line 25) partially serves this role but is tmap-specific, not a general setup chunk.

## Code Annotations

**Assessment: ADEQUATE but missing standard formatting.**

**Strengths:**
- Most major code blocks have 2-3 line comment blocks explaining what and why (e.g., lines 127-129 before `geojson_read()`, lines 210-213 before `apply(d2, 2, scale)`, lines 216-220 before `Mclust()`)
- Inline comments on non-obvious arguments are present (e.g., line 147 on `st_transform`, line 176 on `k = 0.05`)
- The `summarise(across(...))` replacement is explicitly noted as replacing the deprecated `summarise_each(funs(mean))` (lines 317, 506-507)
- Post-operation comments explain what outputs look like (e.g., lines 228-230 after `summary(fit)`)
- Callout boxes provide helpful context (lines 234-240 on why 8 groups, lines 380-385 on reading percentile charts)

**Weaknesses:**
1. **No `# ──` section headers inside code chunks.** The standard requires `# ── Section Name ──` comment headers. The lab uses markdown headers outside chunks but not the standard comment-header format inside chunks.
2. **Some chunks lack pre-block comments.** Lines 265-278 (density-hispanic chunk) have a one-line comment assigning labels but no explanation of what the density plot will show or why it's useful before the `ggplot()` call.
3. **The `view_cluster_data()` function (lines 495-537)** has adequate inline comments but could benefit from a more detailed header block explaining when/why a student would use this reusable function.

## Package Consistency

**All packages used have corresponding `library()` calls.** Specifically:

- `geojsonio` loaded (line 49), used at line 130 (`geojson_read`)
- `sp` loaded (line 50), used implicitly via `phx@data` (line 205) and `plot(phx)` (line 133)
- `sf` loaded (line 51), used for `st_as_sf()`, `st_transform()`, `st_bbox()`, `st_crs()`
- `mclust` loaded (line 55), used for `Mclust()` (line 221)
- `tmap` loaded (line 32, 58), used extensively for mapping
- `ggplot2` loaded (line 59), used for density plots
- `ggthemes` loaded (line 60) — **NOT actually used anywhere in the code.** No `theme_*()` from ggthemes appears. `theme_minimal()` on lines 278, 293 is from ggplot2, not ggthemes. **Remove unused library call.**
- `dplyr` loaded (line 62), used for `select()`, `group_by()`, `summarise()`
- `pander` loaded (line 63), used for `pander()` (lines 116, 559)
- No missing library calls detected.

## Inline R References

**No inline R expressions found in Lab 3.** The lab uses no backtick-r references anywhere in the document. All text is static. This is acceptable but means the solutions won't auto-update if the data or clustering results change.

## Format Consistency

| Element | Lab 1 Standard | Lab 3 Actual | Match? |
|---------|----------------|--------------|--------|
| YAML title | `title: "Lab 01 — ..."` | `title: "Lab 03 — Solutions: ..."` | Yes |
| YAML subtitle | `subtitle: "PAF 516"` | `subtitle: "PAF 516"` | Yes |
| YAML format | html with theme, toc, self-contained | html with theme, toc, self-contained | Yes |
| YAML execute | echo, warning, message, fig-width | echo, warning, message, fig-width, fig-height | Close (extra fig-height) |
| Setup chunk | `#| label: setup`, `#| include: false` | `#| label: tmap-reset`, `#| include: false` | No — wrong label, tmap-specific |
| Chunk labels | `step.01`, `step.02`, etc. | `load-packages`, `load-shapefile`, etc. | No — different convention (kebab-case vs dot-separated) |
| Question format | Q1/Q2/Q3 (interpret/modify/interpret-modified) | Part 01 (cluster labels table) + Part 02 (reading response Q1/Q2/Q3) | No — does not follow standardized format |
| Self-contained flag | `self-contained: true` | `self-contained: true` | Yes |
| Code-fold | Not in Lab 1 | `code-fold: true`, `code-tools: true` | Inconsistent |

**Major format discrepancy:** The question format does not follow the Q1 (interpret results) / Q2 (modify analysis with FULL CODE) / Q3 (interpret modified results) pattern. Part 01 asks students to label clusters (a table exercise, not interpretation of analytical output). Part 02 is a reading-response exercise about external papers, not a modification of the lab's own analysis. There is no Q2-style modification task and no Q3 comparison.

## Specific Issues

1. **Lines 50, 55: Retired/prohibited packages loaded.** `library(sp)` and `library(mclust)` directly conflict with the curriculum spec. sp is retired; mclust is explicitly excluded ("No mclust. No complex clustering.").

2. **Line 32: `library(tmap)` loaded.** tmap is flagged as deprecated in the curriculum spec's checklist. Should use ggplot2 + geom_sf() for static maps and leaflet for interactive.

3. **Lines 25-34: No standard setup chunk.** The `tmap-reset` chunk serves a tmap-specific purpose but does not include `knitr::opts_chunk$set(...)` or `options(tigris_use_cache = TRUE)` as required.

4. **Lines 123-134: Missing `#| results: hide` on data download chunk.** `geojson_read()` downloads from GitHub and may produce progress output.

5. **Line 60: `library(ggthemes)` loaded but never used.** No ggthemes functions appear anywhere in the code. Remove.

6. **Line 205: `phx@data` uses sp S4 slot access.** Should use `st_drop_geometry()` on the sf-converted object instead.

7. **Lines 374-402: Questions do not follow standardized format.** Part 01 is a labeling exercise; Part 02 is reading-response. Neither includes a Q2-style analytical modification with full code, nor a Q3-style comparison of modified vs original results.

8. **No `options(tigris_use_cache = TRUE)` anywhere.** Required per curriculum standard in every lab's setup chunk.

9. **Line 133: `print(plot(phx))`** — Wrapping `plot()` in `print()` is unnecessary and produces extraneous `NULL` output in the console. Use `plot(phx)` alone.

10. **Lines 161-185: Two `eval: false` chunks for interactive tmap.** These will never render, creating dead code in the solutions file. If interactive mapping is desired, replace with a leaflet implementation that renders in HTML. Otherwise, remove entirely.

11. **Entire lab concept conflicts with redesigned curriculum.** The CLAUDE.md spec redesigns Lab 3 as "Spatial Data Integration & Overlay Analysis" (spatial joins, buffer analysis, external data integration). The current Lab 3 is a Phoenix clustering exercise using mclust. This is a complete thematic mismatch — the lab needs a full rewrite, not just code fixes.

## Verdict
**NEEDS REVISION — FULL REWRITE REQUIRED**

The current Lab 3 is fundamentally misaligned with the redesigned curriculum. It uses three prohibited/retired packages (sp, mclust, tmap), teaches clustering rather than spatial data integration, uses pre-built GeoJSON from GitHub rather than tidycensus API data, and does not follow the standardized question format. Individual code fixes are insufficient; the lab requires a complete redesign to match the "Spatial Data Integration & Overlay Analysis" specification in the curriculum plan.

If the lab were to be retained as-is (which is not recommended), the minimum fixes would be:
1. Replace sp/geojsonio pipeline with sf::st_read()
2. Replace all tmap calls with ggplot2 + geom_sf()
3. Add proper setup chunk with knitr opts and tigris cache
4. Add `#| results: hide` to data download chunks
5. Remove unused `library(ggthemes)`
6. Restructure questions to Q1 (interpret clusters) / Q2 (re-run clustering with different variables, FULL CODE) / Q3 (interpret how results changed)
