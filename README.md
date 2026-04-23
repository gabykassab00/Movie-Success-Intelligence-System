# Movie Success Intelligence System

## Project Summary
This project builds a data pipeline to analyze what makes movies successful at the box office.
It collects data from multiple sources, cleans and integrates them, stores the result in PostgreSQL,
and runs analytical queries to uncover patterns in movie performance.

## Data Sources
| Source | Type | What it provides |
|---|---|---|
| TMDB API | REST API | Movie metadata, genres, ratings, release dates |
| Box Office Mojo | Web scraping | Revenue, opening weekend, budget |
| Reference CSV | Static file | Additional movie attributes and identifiers |

## Repository Structure
Movie-Success-Intelligence-System/
├── data/
│   ├── sample/        # Small sample CSV files for testing
│   └── processed/     # Final cleaned dataset output
├── ingestion/         # Scripts to collect data from TMDB API and Box Office Mojo
├── cleaning/          # Data cleaning scripts and notebooks
├── storage/           # SQL schema, ER diagram, PostgreSQL setup notes
├── queries/           # Analytical SQL queries
├── notebooks/         # Jupyter notebooks for cleaning and analysis
├── docs/              # Source appraisal, storage decision, integration docs
├── visuals/           # Charts, diagrams, screenshots
└── ai_usage/          # AI tool usage documentation

## Setup

1. Install Python 3.11+
2. Install PostgreSQL and create a database named `movie_project`
3. Clone this repository
4. Install dependencies:
pip install -r requirements.txt
5. Add your TMDB API key to a `.env` file:
TMDB_API_KEY=your_key_here

## Run Order

1. Run ingestion scripts in `ingestion/` to collect raw data
2. Run the cleaning notebook in `cleaning/` to process and merge data
3. Output is saved as `data/processed/final_dataset.csv`
4. Import `final_dataset.csv` into PostgreSQL as `final_dataset_stage`
5. Run `storage/schema_and_load.sql` to create tables and load data
6. Run analytical queries from `queries/queries.sql`

## Database Info

- **Database name:** `movie_project`
- **Main tables:**

| Table | Description |
|---|---|
| `movies` | Core movie metadata (title, genre, release date) |
| `ratings` | Audience and critic ratings |
| `revenue` | Box office performance data |
| `reference_info` | Additional attributes from reference CSV |

## Reproducibility

You can rerun this project using the sample data in `data/sample/` without needing
full API access. Sample files include `sample_tmdb.csv`, `sample_boxoffice.csv`,
and `sample_reference.csv`. Follow the run order above starting from the cleaning step.

## AI Usage

This project used AI tools to assist with development.
Full documentation of AI usage, including prompts and outputs, is available in the `ai_usage/` folder.
See `ai_usage/AI_USAGE.md` for details.
