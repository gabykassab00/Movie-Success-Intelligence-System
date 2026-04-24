# 🎬 Movie Success Intelligence System

**MSBA 305 — Data Processing Framework — Spring 2025/2026**  
Instructor: Dr. Ahmad El-Hajj — AUB

---

## 🚀 Overview

A complete end-to-end data pipeline that integrates three heterogeneous movie datasets:

- **TMDB API data:** metadata, ratings, and popularity
- **Box Office data:** movie revenue
- **Top 200 Movies dataset:** reference ranking and distributor information

The pipeline cleans the data with Python and pandas, integrates the datasets, stores the result in PostgreSQL, and analyzes the final dataset using SQL queries.

---

## 🎯 Business Problem

A film analytics firm needs a unified dataset to answer:

- Which movies generate the highest revenue?
- Do higher-rated movies also generate more revenue?
- Which movies are most popular?
- Which distributors appear most often?
- What trends exist across years?

---

## 📊 Pipeline Summary

```text
Raw Data → Cleaning → Integration → PostgreSQL Storage → SQL Queries → Business Insights
```

---

## 📁 Project Structure

```
Movie-Success-Intelligence-System/
├── ai_usage/
│   └── AI_USAGE.md
├── cleaning/
│   └── clean_transform.py
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── architecture_decisions.md
│   ├── data_quality_report.md
│   ├── data_source_appraisal.csv
│   └── governance.md
├── ingestion/
│   └── ingest_data.py
├── notebooks/
├── queries/
│   ├── analytical_queries.sql
│   └── query_results.md
├── storage/
│   ├── indexes_and_view.sql
│   └── load_data.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Requirements

- Python 3.8+
- PostgreSQL
- Python packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/gabykassab00/Movie-Success-Intelligence-System.git
cd Movie-Success-Intelligence-System
```

### 2. Create environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Pipeline

### Step 1: Ingest raw data
```bash
python ingestion/ingest_data.py
```

### Step 2: Clean and integrate data
```bash
python cleaning/clean_transform.py
```

This creates:
```
data/processed/final_dataset.csv
```

### Step 3: Load data into PostgreSQL
```bash
python storage/load_data.py
```

### Step 4: Create indexes and analytical view
```bash
psql -d your_database_name -f storage/indexes_and_view.sql
```

### Step 5: Run analytical queries
```bash
psql -d your_database_name -f queries/analytical_queries.sql
```

---

## 📈 SQL Analysis

The SQL analysis includes:

- Top highest-revenue movies
- Top highest-rated movies
- Average rating by year
- Number of movies by year
- Most popular movies
- Top distributors
- Average revenue by year

Query explanations are available in `queries/query_results.md`

---

## 🧠 Architecture Highlights

| Decision | Choice | Reason |
|----------|--------|--------|
| Database | PostgreSQL | Relational structure, joins, views, and indexing |
| Processing | Python + pandas | Suitable for the project's dataset size |
| Pipeline type | Batch processing | Sources do not require real-time streaming |
| Integration key | `title_clean` + `year` | Consistent across all 3 datasets |
| Primary merge | TMDB + Box Office | Best overlap for main analysis |
| Supplementary | Reference CSV | Added as optional enrichment |

Full decisions documented in `docs/architecture_decisions.md`

---

## 📊 Data Quality

Data quality checks include:

- Title standardization
- Revenue cleaning
- Year standardization
- Duplicate checks
- Missing value checks
- Final dataset validation

The current final dataset is created in `data/processed/final_dataset.csv`

Detailed notes available in `docs/data_quality_report.md`

---

## ⚠️ Known Limitations

- The reference dataset has limited overlap with the main TMDB and Box Office matched dataset
- Revenue data may not represent worldwide box office performance
- Revenue values are not inflation-adjusted
- TMDB popularity may be biased toward recent or trending movies
- Some distributor/reference fields may be missing because not all movies match across all sources

---

## 🔒 Governance and Ethics

This project uses public movie data only. No personal or sensitive user data is included.

Governance notes available in `docs/governance.md`

---

## 🤖 AI Usage

AI tools were used to support code organization, debugging, SQL structuring, and documentation.

AI usage documented in `ai_usage/AI_USAGE.md`

---

## 👥 Team Responsibilities

| Person | Responsibility |
|--------|---------------|
| Person 1 | Data Acquisition |
| Person 2 | Data Cleaning |
| Person 3 | Integration and Database |
| Person 4 | SQL Analysis |
| Person 5 | Visualization and Governance |
