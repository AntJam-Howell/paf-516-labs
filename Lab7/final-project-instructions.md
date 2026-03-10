# Final Project: Interactive Economic Hardship Dashboard

## Assignment Overview

In this final project, you will transform your Lab 6 static policy brief into an **interactive Quarto Dashboard**. The dashboard uses `format: dashboard` (not `format: html`) and relies on `crosstalk` for linked interactivity between maps and tables — no Shiny server required. The result is a self-contained HTML file that you will publish to RPubs so anyone with the URL can explore your analysis.

This project synthesizes everything you have learned across Labs 1-6: index construction, choropleth mapping, spatial joins, LISA hot spot analysis, temporal change analysis, and policy communication. The new skills are **dashboard layout** (tabs, columns, value boxes) and **crosstalk interactivity** (clicking a polygon on a mapgl map highlights the corresponding row in a DT table, and vice versa).

---

## Requirements

### Dashboard Structure: 5 Tabs

Your dashboard must contain exactly **5 tabs**, each defined by a level-1 heading (`# Tab Name`) in your `.qmd` file:

| Tab | Content | Key Visualization |
|-----|---------|-------------------|
| **National Context** | US county-level hardship choropleth with value boxes summarizing scope | Static ggplot map + 2-3 value boxes |
| **Local Patterns** | Block group hardship map linked to a detail table via crosstalk | mapgl map + DT table (linked) |
| **Hot Spots** | LISA cluster map with hot/cold spot counts | Static ggplot LISA map + value boxes + cluster table |
| **Change Over Time** | Diverging change map (2015 vs 2023) with improvement/worsening stats | Static ggplot diverging map + value boxes |
| **Policy** | Priority areas table + 3 written policy recommendations | DT table + narrative text |

### Technical Requirements

- **At least 1 crosstalk-linked mapgl map + DT table**: The Local Patterns tab must use `crosstalk::SharedData` to link a `mapgl` map to a `DT::datatable`. Selecting rows in the table should highlight polygons on the map, and clicking polygons on the map should select table rows.
- **At least 2 value boxes** with meaningful metrics (e.g., number of hot spots, percent of CBGs where hardship worsened, max hardship score). You will likely have more than 2 across all tabs.
- **Published to RPubs** (preferred), Quarto Pub, or GitHub Pages. You must submit a live URL.
- **Self-contained HTML under 25 MB**. Use static `ggplot` maps (not mapgl) for the national choropleth and LISA map to keep file size manageable. Reserve mapgl for the one interactive crosstalk panel.

### Code Quality

- All code chunks must have `#| label:` tags
- `echo: false` in the YAML header (dashboard viewers should not see code)
- `warning: false` and `message: false` to suppress console output
- `options(tigris_use_cache = TRUE)` in setup chunk
- Annotated code with section headers and comments explaining your approach

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| Dashboard renders without errors | 10 |
| 5 tabs with appropriate content | 20 |
| Crosstalk interactivity (map <-> table) | 15 |
| Value boxes with meaningful metrics | 10 |
| Visual design and readability | 10 |
| Published to RPubs (live URL) | 10 |
| .qmd source code quality | 10 |
| Reflection questions (3 questions) | 15 |
| **Total** | **100** |

### Rubric Details

- **Dashboard renders without errors (10 pts)**: The `.html` file opens in a browser and all tabs, maps, tables, and value boxes display correctly. Partial credit for minor rendering issues; zero credit if the file does not open.
- **5 tabs with appropriate content (20 pts)**: Each tab is present and contains the visualization and narrative described above (4 pts per tab).
- **Crosstalk interactivity (15 pts)**: Clicking a polygon on the mapgl map selects the corresponding row in the DT table, and selecting a row highlights the polygon. Both directions must work.
- **Value boxes with meaningful metrics (10 pts)**: At least 2 value boxes across the dashboard that display computed statistics (not hardcoded numbers). Metrics should be relevant and clearly labeled.
- **Visual design and readability (10 pts)**: Consistent color palettes, readable text, appropriate legends, clean layout. Maps have titles/captions. Tables are scrollable and well-formatted.
- **Published to RPubs (10 pts)**: A working URL is submitted. The dashboard loads and is interactive at the published URL.
- **Source code quality (10 pts)**: Labeled chunks, section comments, no unnecessary code duplication, `build_hardship_index()` used as a reusable function.
- **Reflection questions (15 pts)**: Thoughtful, specific answers that reference your actual dashboard (5 pts each).

---

## Submission

Submit the following **three items** on Canvas:

1. **Rendered HTML file** (`.html`) — the self-contained dashboard file (< 25 MB)
2. **Source code** (`.qmd`) — your Quarto source file
3. **Published URL** — paste the RPubs (or Quarto Pub / GitHub Pages) link in the submission comments

---

## Publishing to RPubs: Step-by-Step

RPubs is a free hosting service from RStudio/Posit for publishing HTML documents. Follow these steps:

### Step 1: Render Your Dashboard

In RStudio, open your `.qmd` file and click the **Render** button (or run `quarto render your_file.qmd` in the Terminal). Confirm that the HTML file opens correctly in your browser.

### Step 2: Create an RPubs Account

Go to [https://rpubs.com](https://rpubs.com) and create a free account if you do not already have one.

### Step 3: Publish from RStudio

1. After rendering, the HTML preview will appear in the RStudio Viewer pane (or your browser).
2. In the RStudio Viewer pane, click the **Publish** button (blue icon in the top-right corner of the viewer).
3. Select **RPubs** as the publishing destination.
4. If prompted, log in with your RPubs credentials.
5. Give your document a title and a brief description.
6. Click **Publish**.

### Step 4: Verify

1. RPubs will open your published dashboard in a browser.
2. Copy the URL (it will look like `https://rpubs.com/your_username/your_document`).
3. Test the URL in an incognito/private browser window to confirm it loads for others.
4. Verify that the crosstalk interactivity works at the published URL.

### Troubleshooting

- **File too large**: If your HTML exceeds 25 MB, switch the national map from mapgl to a static ggplot. Use `geom_sf()` with `color = NA` to avoid rendering individual county borders (which inflates file size).
- **Crosstalk not working on RPubs**: Ensure you are using `crosstalk::SharedData$new()` with a `key` argument (e.g., `key = ~GEOID`). Both the mapgl map and the DT table must reference the **same** SharedData object.
- **Publish button not visible**: Make sure you rendered the file first. The Publish button only appears after a successful render. Alternatively, you can publish manually by uploading the HTML file directly at [https://rpubs.com/publish](https://rpubs.com/publish).
- **Maps not displaying**: Confirm that `sf` geometries are transformed to WGS84 (`st_transform(data, 4326)`) before passing to mapgl.

### Alternative: Quarto Pub

If you prefer Quarto Pub over RPubs:

1. Create a free account at [https://quartopub.com](https://quartopub.com).
2. In the Terminal, run: `quarto publish quarto-pub your_file.qmd`
3. Follow the prompts to authenticate and publish.

### Alternative: GitHub Pages

If you have a GitHub account:

1. Create a repository for your project.
2. Render the `.qmd` to HTML.
3. Push the HTML file to the repository.
4. Enable GitHub Pages in the repository Settings (Source: main branch, folder: root or /docs).
5. Your dashboard will be available at `https://your_username.github.io/repo_name/your_file.html`.

---

## Reflection Questions

Include your responses to the following three questions in your Canvas submission (either in the submission comments or as a separate document). Each question is worth 5 points.

**Question 1: Key Analytical Finding**

What analytical finding from your dashboard is most important for policymakers? How did you highlight it in the dashboard design (e.g., which tab, value box, map, or table draws attention to it)?

**Question 2: Interactive vs. Static Format**

How does the interactive dashboard format differ from the static policy brief you created in Lab 6? What can users discover through interactivity (clicking, filtering, hovering) that they could not see in the static document?

**Question 3: Future Improvements**

If you had another week to work on this dashboard, what would you add or change? Consider additional data sources, new tabs, different visualizations, or improved interactivity.

---

## Getting Started

1. Download the `Final_Project_Template.qmd` file from Canvas.
2. Open it in RStudio.
3. Update the title with your name.
4. Follow the TODO comments in each section.
5. Reuse code from your Labs 4, 5, and 6 solutions — most of the analytical code is the same.
6. Render frequently to catch errors early.
7. Publish to RPubs when you are satisfied with the result.

The instructor example dashboard (`Final_Project_Example.qmd`) is available as a reference. Your dashboard does not need to match it exactly, but it demonstrates the expected structure and level of detail.
