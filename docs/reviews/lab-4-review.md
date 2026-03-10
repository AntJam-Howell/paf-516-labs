# Lab 4 — Code Review

## Summary
**NEEDS REVISION** — Lab 4 loads two deprecated/retired packages (tmap, mclust), lacks a proper `#| include: false` setup chunk, is missing `#| results: hide` on one data pull chunk (the crosswalk CSV), and does not follow the standardized Q1/Q2/Q3 question format (no Q2 modification includes full code output, no Q3 comparison of modified results). Annotations are generally adequate. The lab correctly modernizes several sp-era patterns (uses `st_drop_geometry()` instead of `@data`, `st_write()` instead of `geojson_write()`, `st_make_valid()`, `st_transform()`) but still relies on tmap for all mapping and mclust for clustering — both prohibited by the curriculum spec.

## Deprecated Functions/Packages

**Issues found:**

1. **Line 27: `library(tmap)` (in tmap-reset chunk) and Line 50: `library(tmap)` (in packages chunk)** — tmap is flagged as deprecated in the curriculum review checklist. The lab uses tmap extensively for all maps: lines 187-191, 248-253, 400-414, 440-453. Should be replaced with ggplot2 + `geom_sf()`.

2. **Line 46: `library(mclust)`** — mclust is explicitly prohibited by the curriculum spec ("No regression. No mclust. No complex clustering."). Used at lines 233, 391, 429. The entire clustering methodology conflicts with the redesigned curriculum.

3. **No `library(sp)` loaded** — Good. The lab explicitly documents the retirement of sp/rgdal/maptools in lines 64-78 and provides a migration table. This is a notable improvement over Lab 3.

4. **No use of `spread()`, `gather()`, `summarise_each()`, `funs()`, or `do()`** — Good. Line 300 correctly uses `summarise(across(where(is.numeric), mean), .groups = "drop")`.

5. **No use of `aes_string()`** — Good. No ggplot aesthetic calls use string-based column references.

6. **No `library(rgdal)` or `library(maptools)`** — Good. Explicitly listed as retired in comments (lines 64-67).

7. **Line 219: `select(d1, all_of(keep.these))`** — Uses `all_of()` which is the modern tidyselect approach. Good.

## Output Suppression

**Issues found:**

1. **Lines 23-28 (`tmap-reset` chunk):** Has `#| include: false`. Good.

2. **Lines 38-68 (`packages` chunk):** Does NOT have `#| include: false` or `#| results: hide`. Package loading messages rely on the global YAML `message: false` (line 17) for suppression. Acceptable but could be more defensive.

3. **Lines 88-106 (`crosswalk` chunk):** Calls `read.csv()` from a GitHub URL. Does NOT have `#| results: hide`. The `grep()` on line 96 and `pander()` on line 105 produce intentional output, but the CSV download itself may produce progress messages. **Should split into a download chunk (hidden) and display chunk (visible), or add `#| results: hide` and move display calls to a separate chunk.**

4. **Lines 112-134 (`population` chunk):** Calls `get_acs()`. Has `#| results: hide`. **Correctly suppressed.**

5. **Lines 140-150 (`merge-census` chunk):** Calls `readRDS(gzcon(url(...)))` which downloads from GitHub. Does NOT have `#| results: hide`. The download may produce progress output. **Should add `#| results: hide`.**

6. **Lines 156-178 (`build-cartogram` chunk):** No external data pull; processes existing objects. Output is a plot. Fine.

7. **YAML (lines 15-19):** Has `warning: false` and `message: false`. Good.

8. **Missing: `options(tigris_use_cache = TRUE)` is NOT set anywhere.** The lab uses `get_acs()` with `geometry = TRUE`, so Census geometries will re-download every render without this setting. **Must be added.**

9. **Missing: No standard setup chunk.** The `tmap-reset` chunk (lines 23-28) only loads tmap and sets the mode. It does not include `knitr::opts_chunk$set(...)` or `options(tigris_use_cache = TRUE)`.

## Code Annotations

**Assessment: ADEQUATE — good quality but missing standard format.**

**Strengths:**
- Most major code blocks have substantive comment blocks before them (e.g., lines 160-162 before `st_make_valid()`, lines 169-171 before population weight calculation, lines 231-232 before `Mclust()`)
- Inline comments explain non-obvious operations (e.g., line 176 on `k = 0.05`, lines 129-133 on GEOID alignment)
- The sp-to-sf migration is well-documented with a comparison table (lines 70-78) and contextual notes (line 180)
- Post-operation notes explain results (e.g., line 240 describes what Mclust returns)
- The `summarise(across(...))` replacement of deprecated `summarise_each(funs(mean))` is explicitly noted (line 299)
- Index construction comments (lines 357-358, 367-368, 372-373) explain what each composite measures

**Weaknesses:**
1. **No `# ──` section headers inside code chunks.** The standard requires `# ── Section Name ──` comment headers within code chunks. The lab uses markdown headers outside chunks and `# ---` separators inside (e.g., line 41) but not the required format.
2. **Lines 312-325 (percentile profile loop):** The loop generating profile charts has minimal annotation. The plotting code uses base R with many magic numbers (e.g., `xlim = c(-75, 100)`, `ytop = (num.vars + 1)`) that are not explained for students seeing base R plotting for the first time.
3. **Lines 354-382 (index construction):** Good explanatory comments on what each index measures, but no explanation of WHY sign-flipping is necessary (what does it mean conceptually to flip a variable's sign in an index?).

## Package Consistency

**All packages used have corresponding `library()` calls.** Specifically:

- `sf` loaded (line 42), used for `st_make_valid()`, `st_transform()`, `st_drop_geometry()`, `st_is_empty()`, `st_geometry()`, `st_write()`
- `geojsonio` loaded (line 43) — **NOT actually used anywhere in the code.** No `geojson_read()` or `geojson_write()` calls appear. The lab uses `st_write()` instead (line 199). **Remove unused library call.**
- `mclust` loaded (line 46), used for `Mclust()` at lines 233, 391, 429
- `corrplot` loaded (line 47) — **NOT actually used anywhere in the code.** No `corrplot()` call appears. **Remove unused library call.**
- `tmap` loaded (lines 27, 50), used extensively for mapping
- `ggplot2` loaded (line 51) — **NOT actually used for any plotting.** All maps use tmap; no `ggplot()` calls appear in the code. **Remove unused library call, or replace tmap calls with ggplot2.**
- `ggthemes` loaded (line 52) — **NOT actually used anywhere in the code.** No ggthemes functions appear. **Remove unused library call.**
- `dplyr` loaded (line 55), used for `select()`, `group_by()`, `summarise()`, `rename()`, `bind_rows()`
- `pander` loaded (line 56), used for `pander()` at lines 105, 223, 458
- `tidycensus` loaded (line 59), used for `get_acs()` at line 118
- `cartogram` loaded (line 62), used for `cartogram_dorling()` at line 176

**Summary: Four packages loaded but never used** — `geojsonio`, `corrplot`, `ggplot2`, `ggthemes`. These should be removed to avoid confusing students about what's actually needed.

## Inline R References

| Expression | Location (Line) | Object Exists? | Status |
|-----------|-----------------|----------------|--------|
| `` `r length(unique(fit$classification))` `` | Line 240 | `fit` created at line 233 (cluster-analysis chunk) | OK |
| `` `r length(unique(fit2$classification))` `` | Line 395 | `fit2` created at line 391 (model2 chunk) | OK |
| `` `r length(unique(fit$classification))` `` | Line 395 | `fit` created at line 233 | OK |
| `` `r length(unique(fit$classification))` `` | Line 473 | `fit` created at line 233 | OK |
| `` `r length(unique(fit2$classification))` `` | Line 473 | `fit2` created at line 391 | OK |
| `` `r length(unique(fit3$classification))` `` | Line 481 | `fit3` created at line 429 (model3 chunk) | OK |

All six inline R expressions reference objects (`fit`, `fit2`, `fit3`) that are created in earlier chunks. All references are valid. The usage is appropriate — reporting the number of clusters found by each model dynamically so the text auto-updates if the data or seed changes.

## Format Consistency

| Element | Lab 1 Standard | Lab 4 Actual | Match? |
|---------|----------------|--------------|--------|
| YAML title | `title: "Lab 01 — ..."` | `title: "Lab 04 -- Solutions: ..."` | Close (uses `--` instead of em-dash `—`) |
| YAML subtitle | `subtitle: "PAF 516"` | `subtitle: "PAF 516"` | Yes |
| YAML format | html with theme, toc, self-contained | html with theme, toc, embed-resources | Close (`embed-resources` replaces deprecated `self-contained`) |
| YAML execute | echo, warning, message, fig-width | echo, warning, message, fig-width, fig-height | Close (extra fig-height) |
| Setup chunk | `#| label: setup`, `#| include: false` | `#| label: tmap-reset`, `#| include: false` | No — wrong label, tmap-specific |
| Chunk labels | `step.01`, `step.02`, etc. | `crosswalk`, `population`, `merge-census`, etc. | No — kebab-case descriptive names vs dot-separated steps |
| Question format | Q1 (interpret) / Q2 (modify with FULL CODE) / Q3 (interpret modified) | Q1 (compare full vs index model, prose only) / Q2 (custom 3-var model with code) | Partial — Q2 has code but no formal Q3 interpret-the-modification section |
| Self-contained | `self-contained: true` | `embed-resources: true` | Functionally equivalent (embed-resources is the modern Quarto replacement) |
| Code-fold | Not in Lab 1 | `code-fold: false` | Consistent (both show code) |

**Notable:** Lab 4 uses `embed-resources: true` (line 13) instead of `self-contained: true`. This is actually the correct modern Quarto syntax — `self-contained` is a Pandoc legacy option. Lab 1 and Lab 3 should be updated to match Lab 4 on this point.

**Question format discrepancy:** The lab has Part 01 (cluster labels, similar to Lab 3) and Part 02 with two questions. Q1 is a prose comparison of the full model vs index model (no code modification). Q2 presents a custom 3-variable model with code — this resembles the Q2 modification pattern, but there is no explicit Q3 asking students to interpret the modification relative to the original. The prose in Q2 blends interpretation with description. This does not cleanly follow the Q1/Q2/Q3 standard.

## Specific Issues

1. **Lines 46, 50: Prohibited packages loaded.** `library(mclust)` (line 46) and `library(tmap)` (lines 27, 50) conflict with the curriculum spec. mclust is explicitly excluded; tmap is deprecated per the review checklist.

2. **Lines 43, 47, 51, 52: Four unused packages loaded.** `geojsonio`, `corrplot`, `ggplot2`, and `ggthemes` are loaded but never called. This wastes student install time and creates confusion about dependencies.

3. **No standard setup chunk.** The tmap-reset chunk (lines 23-28) does not include `knitr::opts_chunk$set(...)` or `options(tigris_use_cache = TRUE)`.

4. **Line 140-150 (`merge-census` chunk): Missing `#| results: hide`.** `readRDS(gzcon(url(...)))` downloads data from GitHub and may produce messages.

5. **Line 88-106 (`crosswalk` chunk): Data download not suppressed.** `read.csv()` from a URL may produce progress output. The chunk also has intentional display output (`grep()`, `pander()`), so splitting into download + display chunks would be cleaner.

6. **Missing `options(tigris_use_cache = TRUE)`.** The lab calls `get_acs()` with `geometry = TRUE` but does not cache geometries. Every render re-downloads Census shapefiles.

7. **Line 1: Title uses `--` instead of `—`.** Minor inconsistency with other labs that use em-dashes. Should standardize to `—` across all labs.

8. **Lines 330-345 (Part 01 cluster labels): Not standardized question format.** This is a labeling exercise, not a Q1-style "interpret the main analytical output." The redesigned Lab 4 should have Q1 (interpret Moran's I and hot spots), Q2 (rerun LISA on a different variable, with full code), Q3 (compare hot spot patterns).

9. **Lines 465-483 (Part 02 Q2): Missing explicit Q3.** The Q2 response includes both code AND interpretation blended together. The standard requires a separate Q3 section specifically for interpreting how the modified results differ from the original.

10. **Duplicate chunk label `cluster-map`.** The label `cluster-map` appears on both line 245 (Step 7 cluster map) and potentially conflicts with rendering. Quarto requires unique chunk labels — though in this file, only one instance is present (line 245 only), so this is not actually a problem. Confirmed: no duplicate.

11. **Line 310: `par(mfrow = c(2, 3))` assumes exactly 6 clusters.** If Mclust finds a different number of clusters (which it can, since the result depends on the data), the grid layout will be wrong. Should dynamically set `mfrow` based on `num.groups`:
    ```r
    ncols <- min(num.groups, 3)
    nrows <- ceiling(num.groups / ncols)
    par(mfrow = c(nrows, ncols))
    ```

12. **Entire lab concept conflicts with redesigned curriculum.** The CLAUDE.md spec redesigns Lab 4 as "Spatial Autocorrelation & Hot Spots" (spatial weights, Global Moran's I, LISA). The current Lab 4 is a San Diego clustering exercise using mclust — essentially a repeat of Lab 3 for a different city. This is a complete thematic mismatch requiring a full rewrite.

13. **Line 117: `census_api_key("YOUR KEY HERE")` commented out.** Students need guidance on how to set their API key. The setup chunk should include `tidycensus::census_api_key()` or reference an `.Renviron` file approach.

14. **Lines 193-204 (`save-cartogram` chunk): `eval: false`.** This is dead code that will never execute during rendering. If the cartogram export is important for downstream use, it should be documented as a manual step. As a solutions file, leaving `eval: false` code is acceptable but should be clearly marked as optional/manual.

## Verdict
**NEEDS REVISION — FULL REWRITE REQUIRED**

The current Lab 4 is fundamentally misaligned with the redesigned curriculum. It repeats the same clustering exercise as Lab 3 (now for San Diego instead of Phoenix), uses prohibited packages (mclust, tmap), and does not teach the intended new skill (spatial autocorrelation / hot spots with spdep). The lab is a thematic duplicate of Lab 3 — which was specifically identified as a problem in the curriculum review ("Lab 4: Essentially redoes Lab 3 for a different city — no new skill").

Credit where due: Lab 4 does a better job than Lab 3 at modernizing the spatial pipeline (uses `st_drop_geometry()` instead of `@data`, documents sp retirement, uses `embed-resources` instead of `self-contained`, uses `cartogram_dorling()` with sf objects). These modernization patterns should be preserved and applied to the rewritten lab.

If the lab were to be retained as-is (not recommended), the minimum fixes would be:
1. Replace mclust with an appropriate non-clustering analytical method
2. Replace all tmap calls with ggplot2 + geom_sf()
3. Remove four unused library calls (geojsonio, corrplot, ggplot2, ggthemes)
4. Add proper setup chunk with knitr opts and tigris cache
5. Add `#| results: hide` to the merge-census and crosswalk data download chunks
6. Add `# ──` section headers inside code chunks
7. Restructure questions to Q1 (interpret) / Q2 (modify with FULL CODE) / Q3 (interpret modification)
8. Dynamically set `par(mfrow)` based on actual cluster count
