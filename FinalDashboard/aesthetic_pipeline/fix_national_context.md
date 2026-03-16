# National Context Tab — Three Fixes

Working directory: ~/Claude/Teaching/PAF516/paf-516-labs/

Fix THREE issues in the National Context tab ONLY.
Edit BOTH Final_Project_Template.qmd and Final_Project_Complete.qmd.
Do NOT touch any other tab or file.

---

## FIX 1 — mapgl bounds: force continental US view, not globe/Asia

The mapgl map opens facing Asia because st_bbox() on a global county
dataset returns a bounding box that includes Alaska/Hawaii and confuses
the renderer.

Replace the maplibre() call with explicit CONUS bounds AND set
projection to "mercator" to prevent globe rotation:

BEFORE:
  maplibre(
    style = carto_style("dark-matter"),
    bounds = st_bbox(county_map)
  )

AFTER:
  maplibre(
    style  = carto_style("dark-matter"),
    bounds = list(
      lng1 = -125.0, lat1 = 24.0,
      lng2 = -66.0,  lat2 = 50.0
    ),
    projection = "mercator"
  )

These are hardcoded CONUS bounds. They always show the lower 48 states
plus a small buffer. Alaska and Hawaii will be outside the initial view
but users can scroll to them.

---

## FIX 2 — Add legend to mapgl map + rename all "Hardship" → "Economic Hardship"

After the add_line_layer() pipe, add a legend:

  ) |>
  add_legend(
    "Economic Hardship Index",
    values  = c("More Hardship", "", "Average", "", "Less Hardship"),
    colors  = c("#db2b27", "#ec6a5a", "#f5f5f5", "#73bfe2", "#1696d2"),
    position = "bottom-left"
  )

In BOTH QMDs, replace every occurrence of the word "Hardship" used
alone as a user-visible label or title (not R variable names) with
"Economic Hardship". Specifically:

  - name = "Hardship\nIndex"       →  name = "Economic\nHardship Index"
  - name = "Hardship\nChange"      →  name = "Economic\nHardship Change"
  - title = "Hardship ..."         →  title = "Economic Hardship ..."
  - "Hardship Index: ..."          →  "Economic Hardship Index: ..."

Search for all instances:
  grep -n '"Hardship' FinalDashboard/Dashboard/Final_Project_Template.qmd

Fix ALL user-visible labels. R variable names (hardship_index,
hardship_change, etc.) stay unchanged.

---

## FIX 3 — Expand dot plot to show all 15 AZ counties + add interpretive text

Restructure the right column. Keep Cards 1 and 2 (highest/lowest AZ
hardship) unchanged. Replace Card 3 with an expanded version.

### New Card 3 — replace existing card-dot-compare chunk entirely:

```r
#| label: card-dot-compare
#| fig-height: 7

# Top 5 worst hardship nationally
top5_us <- county_2023 %>%
  st_drop_geometry() %>%
  left_join(us_ranks, by = "GEOID") %>%
  filter(!is.na(hardship_index)) %>%
  slice_min(us_rank, n = 5, with_ties = FALSE) %>%
  mutate(
    state_name   = str_extract(NAME, "(?<=, ).+"),
    state_abb    = state.abb[match(state_name, state.name)],
    county_short = str_remove(NAME, " County.*"),
    group = "Top 5 US (Most Economic Hardship)",
    label = paste0(county_short, ", ", coalesce(state_abb, state_name))
  )

# Bottom 5 lowest hardship nationally
bot5_us <- county_2023 %>%
  st_drop_geometry() %>%
  left_join(us_ranks, by = "GEOID") %>%
  filter(!is.na(hardship_index)) %>%
  slice_max(us_rank, n = 5, with_ties = FALSE) %>%
  mutate(
    state_name   = str_extract(NAME, "(?<=, ).+"),
    state_abb    = state.abb[match(state_name, state.name)],
    county_short = str_remove(NAME, " County.*"),
    group = "Bottom 5 US (Least Economic Hardship)",
    label = paste0(county_short, ", ", coalesce(state_abb, state_name))
  )

# All 15 Arizona counties
az_all <- county_2023 %>%
  st_drop_geometry() %>%
  left_join(us_ranks, by = "GEOID") %>%
  filter(str_detect(NAME, "Arizona")) %>%
  filter(!is.na(hardship_index)) %>%
  mutate(
    group = "Arizona Counties",
    label = paste0(str_remove(NAME, " County, Arizona"), ", AZ")
  )

compare_df <- bind_rows(top5_us, az_all, bot5_us) %>%
  mutate(
    color_group = case_when(
      group == "Arizona Counties"                   ~ "#fdbf11",
      group == "Top 5 US (Most Economic Hardship)"  ~ "#db2b27",
      TRUE                                          ~ "#1696d2"
    ),
    point_size = if_else(group == "Arizona Counties", 4, 3),
    label = fct_reorder(label, hardship_index)
  )

# Reference values for annotations
az_mean <- compare_df %>%
  filter(group == "Arizona Counties") %>%
  summarise(m = mean(hardship_index)) %>% pull(m)

maricopa_val <- compare_df %>%
  filter(str_detect(label, TARGET_COUNTY)) %>%
  pull(hardship_index)

maricopa_y <- compare_df %>%
  filter(str_detect(label, TARGET_COUNTY)) %>%
  pull(label) %>% as.character()

ggplot(compare_df,
       aes(x = hardship_index, y = label,
           color = color_group, size = point_size)) +
  geom_point() +
  scale_size_identity() +
  scale_color_identity() +
  geom_vline(xintercept = az_mean,
             linetype = "dotted", color = "#9d9d9d", linewidth = 0.5) +
  annotate("text", x = maricopa_val + 0.05, y = maricopa_y,
           label = paste0("\u2190 ", TARGET_COUNTY),
           hjust = 0, size = 2.4, color = "#555555") +
  theme_urbn_dash(base_size = 8.5) +
  theme(
    axis.text.y        = element_text(size = 7.5, color = "#333333"),
    axis.text.x        = element_text(size = 7.5, color = "#767676"),
    panel.grid.major.x = element_line(color = "#eeeeee", linewidth = 0.4)
  ) +
  labs(
    title    = "All Arizona Counties vs. U.S. Extremes",
    subtitle = paste0("Yellow = AZ counties | Red = 5 highest US hardship",
                      " | Cyan = 5 lowest | Dotted = AZ mean"),
    x        = "Economic Hardship Index (pooled z-score)",
    y        = NULL,
    caption  = "ACS 2019–2023 5-Year Estimates"
  )
```

### Below the plot — add interpretive text chunk

FOR Final_Project_Template.qmd (placeholder text):

```r
#| label: card-dot-text
#| output: asis
cat('<p style="font-size:0.82rem;color:#333;margin-top:8px;line-height:1.5">
<strong>[Your interpretation here]</strong> Apache County is Arizona\'s
most economically distressed county, facing barriers including [describe].
Maricopa County has the lowest measured economic hardship among Arizona
counties, driven by [describe factors]. However, there is significant
variation <em>within</em> Maricopa County — the spatial concentration
of that hardship is what we examine in the following panels.
</p>')
```

FOR Final_Project_Complete.qmd (filled-in text):

```r
#| label: card-dot-text
#| output: asis
cat('<p style="font-size:0.82rem;color:#333;margin-top:8px;line-height:1.5">
<strong>Apache County</strong> is Arizona\'s most economically distressed
county (Economic Hardship Index: 1.77, US Rank #47 of 3,142), reflecting
persistent rural poverty, limited non-agricultural employment, and the
compounding effects of federal underinvestment in tribal lands spanning
the Navajo and White Mountain Apache reservations. At the other end,
<strong>Maricopa County</strong> posts the lowest hardship score among
Arizona counties (\u22120.57, US Rank #2,386), a product of its
diversified metro economy, sustained population growth, and broad-based
labor market access across the Phoenix metropolitan area. But this
county-level aggregate obscures deep internal variation: within Maricopa,
census tracts in south and west Phoenix show hardship levels comparable
to the state\'s most distressed rural counties. The panels below
decompose that within-county pattern using LISA hot spot analysis and
temporal change scores across the 2013\u20132019 post-recession window.
</p>')
```

---

## IMPORTANT NOTES

1. library(glue) — check if it is already in the packages chunk:
     grep -n "library(glue" FinalDashboard/Dashboard/Final_Project_Template.qmd
   If not present, add it to the packages line.

2. After all edits, render Template first:
     CENSUS_API_KEY=$(grep CENSUS_API_KEY ~/.Renviron | head -1 | \
       cut -d= -f2 | tr -d '"')
     CENSUS_API_KEY=$CENSUS_API_KEY \
       /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto \
       render FinalDashboard/Dashboard/Final_Project_Template.qmd \
       2>&1 | tail -20
   
   Check size: ls -lh FinalDashboard/Dashboard/Final_Project_Template.html
   Must be < 25 MB.

3. If Template renders cleanly, render Complete with same command.

4. Clean up and deploy:
     rm -rf FinalDashboard/Dashboard/*_files/
     cp FinalDashboard/Dashboard/Final_Project_Complete.html \
        docs/Final_Project_Complete.html
     
     git add FinalDashboard/Dashboard/ docs/Final_Project_Complete.html
     git -c trailer.ifexists=doNothing commit -m \
       "National Context: CONUS bounds, Economic Hardship labels, 15-county dot plot"
     git push
