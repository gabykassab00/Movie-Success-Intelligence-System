# Architecture Decisions

## Decision 1: Batch Processing

**Chosen option:** Batch processing

**Why we chose it:**  
Our data sources are mostly static files and API pulls. The project does not require real-time updates, so batch processing is simpler, reproducible, and appropriate.

**Alternatives considered:**
1. Streaming pipeline
2. Hybrid batch-streaming pipeline

**Why rejected:**
- Streaming was rejected because movie revenue and metadata do not need second-by-second processing.
- Hybrid processing was rejected because it adds unnecessary complexity for this project scope.

**Trade-offs accepted:**  
Batch processing is not real-time, but it is easier to implement, debug, and explain.

---

## Decision 2: PostgreSQL for Storage

**Chosen option:** PostgreSQL

**Why we chose it:**  
The final dataset is structured and relational. PostgreSQL supports joins, indexing, views, and SQL analytics, which match our project needs.

**Alternatives considered:**
1. MongoDB
2. Neo4j

**Why rejected:**
- MongoDB was rejected because our analysis requires joins between movies, ratings, revenue, and reference information.
- Neo4j was rejected because the project is not relationship-heavy or graph-based.

**Trade-offs accepted:**  
PostgreSQL requires schema design, but it provides strong query performance and clear data structure.

---

## Decision 3: Python and Pandas for Cleaning

**Chosen option:** Python with pandas

**Why we chose it:**  
The datasets are small enough to process locally, and pandas is suitable for CSV, JSON, cleaning, merging, and transformation tasks.

**Alternatives considered:**
1. Apache Spark
2. dbt

**Why rejected:**
- Spark was rejected because the dataset size does not require distributed processing.
- dbt was rejected because most cleaning occurs before database loading.

**Trade-offs accepted:**  
Pandas is less scalable than Spark, but it is faster to implement and easier to understand for this project.

---

## Decision 4: SQL for Analysis

**Chosen option:** SQL queries in PostgreSQL

**Why we chose it:**  
SQL is appropriate for structured analysis, aggregation, filtering, and joining tables.

**Alternatives considered:**
1. Python-only analysis
2. NoSQL aggregation

**Why rejected:**
- Python-only analysis was rejected because the project requires query-ready storage and analytical queries.
- NoSQL aggregation was rejected because the data is relational.

**Trade-offs accepted:**  
SQL requires database setup, but it produces clear, reproducible analytical results.