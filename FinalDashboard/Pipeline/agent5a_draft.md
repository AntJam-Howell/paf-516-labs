# Agent 5a — Draft Phoenix Answers

Read FinalDashboard/Dashboard/Final_Project_Template.html to extract
all computed statistics. Then write substantive answers for all 6
TODO sections (3 dashboard recommendations + 3 policy brief answers
+ executive summary + 3 finding paragraphs).

---

## Step 1: Extract statistics from rendered HTML

Run this script to get the key numbers:

  python3 << 'EOF'
  import re
  txt = open("FinalDashboard/Dashboard/Final_Project_Template.html").read()

  # Value box values
  vboxes = re.findall(r'class="value-box-value[^"]*"[^>]*>([^<]+)<', txt)
  print("Value box values:", vboxes[:20])

  # Find HH, LL counts
  hh = re.findall(r'Hot Spot Tracts.*?(\d+)', txt[:5000])
  ll = re.findall(r'Cold Spot Tracts.*?(\d+)', txt[:5000])
  print("HH:", hh, "LL:", ll)

  # Find % improved, % worsened, % persistent HH
  pcts = re.findall(r'(\d+\.?\d*)%', txt)
  print("Percentages found:", sorted(set(pcts)))
  EOF

Also read the RENDERED HTML visually — note:
  - Number of HH hot spot tracts
  - Number of LL cold spot tracts
  - Global Moran's I statistic
  - % tracts improved 2013→2019
  - % persistent HH tracts
  - % emerging HH tracts
  - Highest-hardship tracts (from DT table)
  - Space-time Moran's I

---

## Step 2: Write dashboard Policy tab answers

Replace the 3 TODO cards in Final_Project_Complete.qmd with completed
substantive answers. Format:

```
::: {.card}
## Recommendation 1 — [Specific title based on Persistent HH finding]
[3-4 sentence substantive recommendation that:]
  1. Names a specific geographic area (e.g., "the N High-High cluster tracts
     in the south-central Phoenix corridor, centered around ZIP codes...")
  2. Cites specific statistics from the dashboard
     (hardship index value, % improved, Moran's I, etc.)
  3. Proposes a concrete intervention with a named responsible entity
     (not "the city should" but "Maricopa County Human Services + City of
     Phoenix Office of Housing should...")
  4. Is specific enough that a policymaker could act on it
:::
```

Use actual Phoenix geography — south Phoenix, west Phoenix, central Phoenix,
Laveen, Maryvale, etc. Use actual values from the rendered HTML.

---

## Step 3: Write policy brief answers

In Policy_Brief_Complete.qmd, replace every *YOUR ANSWER HERE* with
substantive text. For each:

### Executive Summary (3-4 sentences)
  State Maricopa County's rank relative to national average.
  Name the spatial pattern (significant clustering, Moran's I value).
  Identify the most urgent finding (persistent HH tracts or emerging HH tracts).
  State the top recommendation in one sentence.

### Finding 1 paragraph (spatial concentration)
  Cite: n_hh hot spot tracts, Moran's I value, what the clustering means
  for structural vs. individual hardship. Name the general geographic
  location of the hot spot cluster (south/central Phoenix).

### Finding 2 paragraph (trajectories)
  Cite: % persistent HH, % emerging HH, % dissolving HH.
  Identify where emerging hot spots are appearing.
  Connect to the displacement paradox (dissolving HH may signal gentrification).

### Finding 3 paragraph (hardship profile)
  Cite: mean hardship index for Persistent HH vs. Dissolving HH.
  Argue which trajectory type deserves the most urgent attention.
  Note whether consistent improvement or worsening dominates.

### 3 Recommendation callouts
  Each must:
  - Have a specific policy title (not "Recommendation 1")
  - Name a target geography with approximate tract count
  - Cite a specific statistic
  - Name a responsible entity
  - Propose a concrete intervention type
  - Reference one course reading where appropriate (Module 5 or 6)
    (e.g., Freeman 2005 on displacement, Ding et al. 2016, Landis 2016)

---

## Step 4: Report draft to Agent 5b

Print the full text of all 6 written answers.
Do NOT render yet — Agent 5b reviews the text first.

⛔ STOP after printing answers — Agent 5b critiques before any file changes.
