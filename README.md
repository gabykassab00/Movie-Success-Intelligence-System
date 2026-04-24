# 🎬 Movie Success Intelligence System

**MSBA 305 — Data Processing Framework — Spring 2025/2026**
Instructor: Dr. Ahmad El-Hajj — AUB

---

## 🚀 Overview

A complete **end-to-end data pipeline** that integrates three heterogeneous movie datasets:

* TMDB API (metadata, ratings, popularity)
* Box Office Mojo (revenue)
* Top 200 Movies 2023 (reference data)

➡️ Cleaned with pandas → stored in PostgreSQL → analyzed via SQL → visualized with charts

---

## 🎯 Business Problem

A film analytics firm needs a **unified dataset** to answer:

* Which movies generate the highest revenue?
* Do higher ratings lead to higher profits?
* Which distributors dominate the market?
* What trends exist across years?

---

## 📊 Pipeline Summary

```text
Raw Data → Cleaning (pandas) → Integration → PostgreSQL → SQL Queries → Charts
```

---

## 📁 Project Structure

```
movie_project/
├── ingestion/        # Data collection (API + CSV)
├── cleaning/         # Data cleaning & integration
├── db/               # Database schema + loading
├── queries/          # Analytical SQL queries
├── viz/              # Visualizations
├── data/             # Raw & cleaned data
├── docs/             # Report & documentation
└── run_pipeline.py   # Full pipeline runner
```

---

## ⚙️ Requirements

* Python 3.10+
* PostgreSQL 18
* Optional: pgAdmin

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone <repo_url>
cd movie_project
```

### 2. Create environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Configure `.env`

```bash
TMDB_API_KEY=your_api_key
PG_DSN=postgresql://postgres:<password>@localhost:5432/movie_project
```

---

## ▶️ Run the Pipeline

### One command

```bash
python run_pipeline.py
```

### Step-by-step

```bash
python ingestion/fetch_tmdb.py
python ingestion/load_csv_sources.py
python cleaning/integrate.py
python db/load.py
psql -d movie_project -f queries/analytics.sql
python viz/charts.py
```

---

## 📈 Key Features

* ✔ Multi-source data integration
* ✔ Cleaned and normalized dataset
* ✔ PostgreSQL relational schema
* ✔ Indexed query-ready view
* ✔ Analytical SQL queries
* ✔ Visual insights with charts

---

## 🧠 Architecture Highlights

* **Database:** PostgreSQL (chosen over MongoDB, Neo4j)
* **Processing:** pandas (lightweight vs Spark)
* **Pipeline:** Batch processing (simple + reproducible)
* **Integration:** `(title_clean + year)` matching

---

## ⚠️ Known Limitations

* Only **4.6% match** with reference dataset
* Revenue = **US domestic only**
* No inflation adjustment
* TMDB bias (recency + popularity skew)

---

## 🤖 AI Usage

AI tools were used for:

* Code scaffolding
* Debugging
* Documentation

All usage is documented in the report.

---

## 📌 Conclusion

This project demonstrates a **complete, reproducible data pipeline** that transforms raw movie data into structured insights for decision-making.
