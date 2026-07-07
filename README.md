# The-Space-Race
70 years of orbital launches visualised in Power BI. 7,500 launches, 7 countries, 3 eras, from Sputnik to the New Space Race.
# The New Space Race
### 70 Years of Orbital Launches — A Power BI Dashboard

![Dashboard Preview](screenshots/page1_overview.png)

---

## About

I came across a space launches dataset while watching a YouTube video about a Power BI competition and got curious enough to explore it myself. No brief, no deadline, no portfolio plan. I just wanted to see whether the story we usually hear about the space race actually matched the numbers.

This is a 3-page interactive Power BI dashboard covering every orbital launch from 1957 to 2024 — 7,500 launches across 7 countries and regions, spanning three distinct eras of spaceflight.

---

## The Story

The dashboard is built around a narrative arc across three eras:

- **Act 1 — Cold War Era (1957–1991):** A bipolar space race. USA and USSR compete for supremacy. Ideology, prestige, and firsts define every launch.
- **Act 2 — Quiet Middle (1992–2010):** The race cools. Collaboration emerges. Fewer dramatic shifts, more players, steady and methodical progress.
- **Act 3 — New Eruption (2011–Present):** A new multipolar race. China rises fast, India enters seriously, and the US surges again.

---

## What the Data Actually Said

A few things that stood out once I started looking at the numbers:

- Russia launched nearly twice as many rockets as the USA during the Cold War (2,107 vs 1,185). And still lost.
- We are now in the busiest period of spaceflight ever — but because the volume is so high, the absolute number of failures has also gone up.
- China went from 10 launches in 2010 to more than 80 in 2023 — the sharpest ramp-up in spaceflight history.
- The US launched 867 times in the New Eruption era alone — more than China and Russia combined in that same period.
- India reached Mars on its first attempt, with one of the smallest space budgets of any spacefaring nation.

---

## Dashboard Pages

### Page 1 — The 70-Year Journey at a Glance
The hero page. Shows the full arc of spaceflight history in one view.

- Stacked area chart: launches per year by country (1957–2024) with era annotations and historical callouts
- KPI cards: Total Launches, Successful, Failed, Success Rate, Countries Involved
- "The Story in Three Acts" narrative panel
- Donut chart: all-time launches by country share
- Orbit types over time
- Crewed vs Uncrewed launches by decade
- Success rate trend across 70 years

### Page 2 — Era Deep Dive
Interactive era toggle (Cold War / Quiet Middle / New Eruption) showing:

- Who launched the most in each era (log scale bar chart)
- Launch frequency over the years (line chart)
- Volume vs Reliability scatter plot (bubble size = total launches)
- Era KPI cards and description
- Static bottom panels comparing all three eras simultaneously

### Page 3 — Country Spotlight
Per-country deep dive with 7 selector buttons (USA, Russia, China, India, Europe, Japan, Others):

- KPI cards: Total Launches, Successful, Failed, Success Rate, First Launch Year, Avg Space Budget
- Launch activity and reliability combo chart (bars + success rate line)
- Launch outcomes donut chart
- Rocket reliability vs usage scatter plot
- Top rockets by launch count
- Launch volume by decade waterfall chart
- Key milestones timeline per country
- "Did You Know?" fact per country

---

## Screenshots

| Page | Preview |
|---|---|
| Page 1 — Overview | ![](screenshots/page1_overview.png) |
| Page 2 — Cold War Era | ![](screenshots/page2_coldwar.png) |
| Page 2 — Quiet Middle | ![](screenshots/page2_quietmiddle.png) |
| Page 2 — New Eruption | ![](screenshots/page2_neweruption.png) |
| Page 3 — USA | ![](screenshots/page3_usa.png) |
| Page 3 — Russia | ![](screenshots/page3_russia.png) |
| Page 3 — China | ![](screenshots/page3_china.png) |
| Page 3 — India | ![](screenshots/page3_india.png) |
| Page 3 — Europe | ![](screenshots/page3_europe.png) |
| Page 3 — Japan | ![](screenshots/page3_japan.png) |
| Page 3 — Others | ![](screenshots/page3_others.png) |

---

## Repo Structure

```
the-new-space-race/
│
├── data/
│   ├── launches_clean.csv       # Cleaned fact table (7,500 rows)
│   ├── countries.csv            # Country dimension with colors
│   └── space_budgets.csv        # Annual space budgets 2000–2024
│
├── screenshots/
│   ├── page1_overview.png
│   ├── page2_coldwar.png
│   ├── page2_quietmiddle.png
│   ├── page2_neweruption.png
│   ├── page3_usa.png
│   ├── page3_russia.png
│   ├── page3_china.png
│   ├── page3_india.png
│   ├── page3_europe.png
│   ├── page3_japan.png
│   └── page3_others.png
│
├── 01_extract.py                # API extraction script (Launch Library 2)
├── 02_clean.py                  # Data cleaning script
├── theme.json                   # Custom Power BI dark theme
├── The New Space Race.pbix      # Power BI dashboard file
└── README.md
```

---

## Data

**Source:** [Kaggle — Space Missions Dataset](https://www.kaggle.com/) via Launch Library 2

**Coverage:** 1957–2024, orbital launches only

**Cleaning decisions:**
- USSR merged into Russia for narrative continuity
- "Other" standardised to "Others"
- Launch success mapped from 0/1 to Success/Failure
- Era column added based on year ranges

---

## Tools

| Tool | Purpose |
|---|---|
| Python (pandas) | Data extraction and cleaning |
| Power BI Desktop | Dashboard and visualisation |
| DAX | Measures, calculated columns, KPIs |
| Custom theme.json | Dark mode, country color palette |
| Bookmarks + Buttons | Era and country interactivity |

---

## Country Colors

| Country | Color | Hex |
|---|---|---|
| USA | Blue | `#2979FF` |
| Russia | Red | `#FF1744` |
| China | Gold | `#FFD600` |
| India | Orange | `#FF6D00` |
| Europe | Purple | `#D500F9` |
| Japan | Cyan | `#00E5FF` |
| Others | Gray | `#90A4AE` |

---

## How to Run

1. Clone this repo
2. Open `The New Space Race.pbix` in Power BI Desktop
3. If data doesn't load, go to **Transform Data → Data Source Settings** and point it to the `data/` folder in this repo
4. To re-run data cleaning: `python 02_clean.py` (requires pandas)

---

## Notes

- Space budget data is sourced from public records (NASA, ESA, OECD) and estimates where official figures are not disclosed (China, Russia)
- USSR and Russia are treated as one continuous entity throughout the dashboard. This is noted in the dashboard footer.
- The "Others" category includes all launches not attributed to USA, Russia, China, India, Europe, or Japan

---

*Built out of curiosity. Not for a portfolio. Just wanted to see what the data said.*
