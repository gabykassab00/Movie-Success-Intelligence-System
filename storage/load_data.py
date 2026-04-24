import pandas as pd
import psycopg2
from pathlib import Path


PROCESSED_DIR = Path("data/processed")
FINAL_DATASET_PATH = PROCESSED_DIR / "final_dataset.csv"


DB_NAME = "your_database_name"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"


def connect_to_db():
    """
    Creates a connection to the PostgreSQL database.
    Update DB_NAME, DB_USER, and DB_PASSWORD before running.
    """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_tables(cursor):
    """
    Creates simplified database tables for the movie pipeline.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title TEXT,
            title_clean TEXT,
            year INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER REFERENCES movies(id),
            vote_average NUMERIC,
            popularity NUMERIC
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revenue (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER REFERENCES movies(id),
            revenue NUMERIC
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference_info (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER REFERENCES movies(id),
            distributor TEXT,
            rank_ref NUMERIC,
            total_gross_ref NUMERIC,
            theaters_ref NUMERIC,
            release_date_ref TEXT
        );
    """)


def load_data(cursor, df):
    """
    Loads the final dataset into PostgreSQL tables.
    """
    for _, row in df.iterrows():
        title = row.get("title", row.get("title_tmdb", None))
        title_clean = row.get("title_clean", None)
        year = row.get("year", None)

        cursor.execute(
            """
            INSERT INTO movies (title, title_clean, year)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (title, title_clean, year)
        )

        movie_id = cursor.fetchone()[0]

        vote_average = row.get("vote_average", None)
        popularity = row.get("popularity", None)
        revenue_value = row.get("revenue", None)

        cursor.execute(
            """
            INSERT INTO ratings (movie_id, vote_average, popularity)
            VALUES (%s, %s, %s);
            """,
            (movie_id, vote_average, popularity)
        )

        cursor.execute(
            """
            INSERT INTO revenue (movie_id, revenue)
            VALUES (%s, %s);
            """,
            (movie_id, revenue_value)
        )

        cursor.execute(
            """
            INSERT INTO reference_info (
                movie_id,
                distributor,
                rank_ref,
                total_gross_ref,
                theaters_ref,
                release_date_ref
            )
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (
                movie_id,
                row.get("distributor", None),
                row.get("rank_ref", None),
                row.get("total_gross_ref", None),
                row.get("theaters_ref", None),
                row.get("release_date_ref", None)
            )
        )


def main():
    print("Loading final dataset...")

    df = pd.read_csv(FINAL_DATASET_PATH)

    print(f"Rows to load: {len(df)}")

    conn = connect_to_db()
    cursor = conn.cursor()

    create_tables(cursor)
    load_data(cursor, df)

    conn.commit()

    cursor.close()
    conn.close()

    print("Data loaded successfully into PostgreSQL.")


if __name__ == "__main__":
    main()