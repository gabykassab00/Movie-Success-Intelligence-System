# 🎬 Movie Success Intelligence System

## 📌 Project Overview
This project builds an end-to-end data pipeline to analyze movie success using multiple data sources. It integrates movie metadata, ratings, popularity, and revenue data to generate meaningful insights about factors that drive both commercial and critical success.

---

## 🎯 Business Problem
Movie studios and analysts want to understand:
- What drives high box office revenue?
- Do higher-rated movies generate more profit?
- Which genres or distributors perform best?
- How do movie trends change over time?

This project answers these questions using structured data and SQL-based analysis.

---

## 📊 Data Sources

| Source | Format | Description |
|-------|--------|------------|
| TMDB API | JSON | Movie metadata, ratings, popularity |
| Box Office Dataset | CSV | Revenue data |
| Top Movies Dataset | CSV | Ranking, distributor, reference data |

---

## ⚙️ Pipeline Architecture

1. **Data Acquisition**
   - Fetch data from TMDB API
   - Load CSV datasets

2. **Data Cleaning**
   - Standardize titles (lowercase, remove symbols)
   - Convert revenue to numeric format
   - Extract year from dates
   - Handle missing values
   - Remove duplicates

3. **Data Integration**
   - Merge datasets using `title_clean` and `year`
   - Generate a unified dataset

4. **Storage**
   - PostgreSQL database
   - Tables: movies, ratings, revenue, reference_info
   - Indexing for performance optimization

5. **Analysis**
   - SQL queries to extract insights

6. **Reporting**
   - Query explanations and business insights

---

## 📁 Project Structure

Movie-Success-Intelligence-System/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ingestion/
│   └── ingest_data.py
│
├── cleaning/
│   └── clean_transform.py
│
├── storage/
│   ├── load_data.py
│   └── indexes_and_view.sql
│
├── queries/
│   ├── analytical_queries.sql
│   └── query_results.md
│
├── notebooks/
│
├── docs/
│   ├── data_source_appraisal.csv
│   └── data_quality_report.md
│
├── ai_usage/
│   └── AI_USAGE.md
│
├── README.md
├── requirements.txt
└── .gitignore

---

## 🚀 Setup Instructions

### 1. Clone the repository
git clone https://github.com/gabykassab00/Movie-Success-Intelligence-System.git
cd Movie-Success-Intelligence-System

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

---

## ▶️ How to Run the Project

### Step 1: Data Ingestion
python ingestion/ingest_data.py

### Step 2: Data Cleaning
python cleaning/clean_transform.py

### Step 3: Load to PostgreSQL
python storage/load_data.py

### Step 4: Create indexes and analytical view
psql -d your_database_name -f storage/indexes_and_view.sql

### Step 5: Run analytical queries
psql -d your_database_name -f queries/analytical_queries.sql

---

## 📈 SQL Analysis

The project includes:
- Top revenue movies
- Highest-rated movies
- Average rating by year
- Movie count trends
- Popularity rankings
- Distributor analysis
- Revenue trends over time

See:
queries/analytical_queries.sql  
queries/query_results.md

---

## 📊 Data Quality

Checks performed:
- Missing values analysis
- Duplicate detection
- Table row validation
- Join validation through views

Some missing values exist due to unmatched records across datasets.

See:
docs/data_quality_report.md

---

## 🤖 AI Usage

AI tools were used for:
- Code assistance
- SQL structuring
- Documentation support

Full details:
ai_usage/AI_USAGE.md

---

## 🔒 Governance & Ethics

- No personal data used
- Public datasets only
- Possible bias from popularity-based data
- Incomplete matches between sources acknowledged

---

## 👥 Team Responsibilities

| Person | Role |
|------|------|
| Person 1 | Data Acquisition |
| Person 2 | Data Cleaning |
| Person 3 | Integration & Database |
| Person 4 | SQL Analysis |
| Person 5 | Visualization & Governance |

---

## 📌 Conclusion

This project demonstrates a complete data pipeline from raw data ingestion to structured analysis, providing insights into the key drivers of movie success.
