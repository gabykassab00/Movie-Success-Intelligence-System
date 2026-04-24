# Movie Data Processing Pipeline

**MSBA 305 — Data Processing Framework — Spring 2025/2026**
Instructor: Dr. Ahmad El-Hajj — Suliman S. Olayan School of Business, AUB

A complete data pipeline that ingests three heterogeneous movie datasets
(TMDB API, Box Office Mojo, Top 200 Movies 2023), integrates them into a
normalized PostgreSQL schema, and exposes a query-ready analytical view.

---

## Overview

**Business problem.** A hypothetical film investment analytics firm needs a
unified, query-ready dataset combining audience reception, commercial
performance, and distribution reference data to benchmark historical signals
against greenlight decisions.

**Pipeline.** Three sources → pandas cleaning + integration →
PostgreSQL 18 (4 normalized tables + `movie_full_view`) → 6 analytical SQL
queries + 3 Matplotlib charts.

**Scale.** 281 integrated films, 1950–2024, 100% complete on all core
analytical fields (revenue, vote_average, popularity, genres).

For the full architecture decisions, see `docs/Report.docx`.

---

## Folder Structure

```
movie_project/
├── README.md                   (this file)
├── requirements.txt            (pinned Python deps)
├── .env.example                (template for TMDB_API_KEY)
├── run_pipeline.py             (one-command orchestrator)
│
├── ingestion/
│   ├── fetch_tmdb.py           (TMDB API puller with retry + back-off)
│   └── load_csv_sources.py     (reads Box Office + Top 200 CSVs)
│
├── cleaning/
│   └── integrate.py            (title normalization, currency regex,
│                                cross-source join, dedup)
│
├── db/
│   ├── schema.sql              (CREATE TABLE + index DDL)
│   └── load.py                 (populate tables from cleaned CSV)
│
├── queries/
│   └── analytics.sql           (6 queries: filter → window → CTE → array)
│
├── viz/
│   └── charts.py               (3 EDA charts from final_dataset.csv)
│
├── data/
│   ├── raw/                    (place downloaded source files here)
│   └── clean/                  (final_dataset.csv is written here)
│
└── docs/
    └── Report.docx             (full architecture report)
```

---

## Requirements

- **Python 3.10+**
- **PostgreSQL 18** running locally (or remote via connection string)
- **pgAdmin 4** (optional but recommended for browsing the database)

Python packages (see `requirements.txt`):

```
pandas>=2.2.0
requests>=2.31.0
psycopg2-binary>=2.9.9
matplotlib>=3.8.0
seaborn>=0.13.0
python-dotenv>=1.0.0
```

---

## Setup

### 1. Clone and install

```bash 
git clone <repo_url> movie_project
cd movie_project
python -m venv .venv
source .venv/bin/activate       # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in:
#   TMDB_API_KEY=<your-v3-api-key-from-themoviedb.org>
#   PG_DSN=postgresql://postgres:<password>@localhost:5432/movie_project
```

Register a free TMDB API key at
[themoviedb.org](https://www.themoviedb.org/settings/api).

### 3. Create the PostgreSQL database

```bash
createdb movie_project
psql -d movie_project -f db/schema.sql
```

Alternatively, restore the included backup to skip the pipeline run:

```bash
pg_restore -d movie_project movie_project.backup
```

---

## Running the Pipeline

### One-command run

```bash
python run_pipeline.py
```

This executes the full chain: fetch TMDB → read CSVs → clean →
integrate → load to PostgreSQL → generate charts.

### Step by step

```bash
# 1. Pull TMDB records (writes data/raw/tmdb_raw.json)
python ingestion/fetch_tmdb.py --pages 25

# 2. Verify the two source CSVs are in data/raw/
#    - data/raw/boxoffice_raw.csv
#    - data/raw/top200_2023.csv
python ingestion/load_csv_sources.py

# 3. Clean, normalize titles, integrate across the three sources
#    (writes data/clean/final_dataset.csv)
python cleaning/integrate.py

# 4. Load the cleaned dataset into PostgreSQL
python db/load.py

# 5. Run the analytical queries
psql -d movie_project -f queries/analytics.sql

# 6. Generate charts (writes viz/chart*.png)
python viz/charts.py
```

---

## Architecture Highlights

- **Storage choice:** PostgreSQL 18. Alternatives evaluated and rejected:
  MongoDB (rejected — denormalization cost, no FK integrity) and flat CSV
  (rejected — no index support, no concurrency). See `docs/Report.docx §5`.
- **Processing:** Local pandas. Alternatives rejected: PySpark (overhead
  exceeds pipeline runtime on sub-MB data) and Polars (no measurable gain
  at our scale). See `docs/Report.docx §7`.
- **Ingestion:** Batch. Streaming (Kafka) and orchestrated batch (Airflow)
  rejected for one-shot project scope. Airflow is the documented production
  scaling path. See `docs/Report.docx §4`.
- **Integration strategy:** Join on `(title_clean, year)`. 56% TMDB
  retention; 4.6% reference match rate (disclosed honestly). See
  `docs/Report.docx §3`.

---

## Known Limitations

1. **Reference data thin.** Only 13 of 281 rows (4.6%) match the Top 200
   2023 reference dataset. Queries using `distributor` are caveated as
   indicative-only.
2. **U.S. domestic revenue only.** Box Office Mojo does not capture
   international gross. Understates global revenue 40–60% on major
   releases.
3. **No inflation adjustment.** Revenue values are nominal.
4. **TMDB selection bias.** Crowd-sourced, English-weighted, recency-biased.

These are disclosed in the report rather than silently tolerated.

---

## AI Usage Disclosure

AI assistants (Claude) were used for code scaffolding, debugging, and
documentation review. Every interaction is documented in
`docs/Report.docx §11` using the format required by the course brief.
No AI-generated code was merged without team review.

---

## License / Academic Use Notice

This repository is an academic deliverable for MSBA 305 at AUB. Source
data belongs to the respective providers (TMDB, Box Office Mojo). See
the report references for attribution.
