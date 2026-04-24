import pandas as pd
import re
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_title(title):
    """
    Standardizes movie titles so datasets can be matched more reliably.
    """
    if pd.isna(title):
        return None

    title = str(title).lower().strip()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)

    return title


def clean_revenue(value):
    """
    Converts revenue values such as '$1,234,567' into numeric values.
    """
    if pd.isna(value):
        return None

    value = str(value)
    value = re.sub(r"[^0-9.]", "", value)

    if value == "":
        return None

    return float(value)


def extract_year(value):
    """
    Extracts year from date-like values.
    """
    if pd.isna(value):
        return None

    date = pd.to_datetime(value, errors="coerce")

    if pd.isna(date):
        return None

    return int(date.year)


def clean_tmdb():
    """
    Cleans TMDB raw JSON data.
    """
    tmdb_path = RAW_DIR / "tmdb_raw.json"

    tmdb = pd.read_json(tmdb_path)

    tmdb["title_clean"] = tmdb["title"].apply(clean_title)
    tmdb["year"] = tmdb["release_date"].apply(extract_year)

    tmdb = tmdb.drop_duplicates(subset=["title_clean", "year"])

    tmdb.to_csv(PROCESSED_DIR / "tmdb_clean.csv", index=False)

    return tmdb


def clean_boxoffice():
    """
    Cleans raw box office revenue data.
    """
    boxoffice_path = RAW_DIR / "boxoffice_raw.csv"

    boxoffice = pd.read_csv(boxoffice_path)

    boxoffice["title_clean"] = boxoffice["title"].apply(clean_title)

    if "revenue" in boxoffice.columns:
        boxoffice["revenue"] = boxoffice["revenue"].apply(clean_revenue)

    if "year" in boxoffice.columns:
        boxoffice["year"] = pd.to_numeric(boxoffice["year"], errors="coerce")
    elif "release_date" in boxoffice.columns:
        boxoffice["year"] = boxoffice["release_date"].apply(extract_year)

    boxoffice = boxoffice.drop_duplicates(subset=["title_clean", "year"])

    boxoffice.to_csv(PROCESSED_DIR / "boxoffice_clean.csv", index=False)

    return boxoffice


def clean_reference():
    """
    Cleans the reference movie dataset.
    """
    reference_path = RAW_DIR / "Top_200_Movies_Dataset_2023.csv"

    reference = pd.read_csv(reference_path)

    title_column = "title" if "title" in reference.columns else reference.columns[0]
    reference["title_clean"] = reference[title_column].apply(clean_title)

    if "year" in reference.columns:
        reference["year"] = pd.to_numeric(reference["year"], errors="coerce")
    elif "release_date" in reference.columns:
        reference["year"] = reference["release_date"].apply(extract_year)

    reference = reference.drop_duplicates(subset=["title_clean", "year"])

    reference.to_csv(PROCESSED_DIR / "movies_reference_clean.csv", index=False)

    return reference


def create_final_dataset(tmdb, boxoffice, reference):
    """
    Integrates the cleaned datasets into one final dataset.
    """
    final = tmdb.merge(
        boxoffice,
        on=["title_clean", "year"],
        how="left",
        suffixes=("_tmdb", "_boxoffice")
    )

    final = final.merge(
        reference,
        on=["title_clean", "year"],
        how="left",
        suffixes=("", "_ref")
    )

    final.to_csv(PROCESSED_DIR / "final_dataset.csv", index=False)

    return final


def main():
    print("Starting cleaning and transformation process...")

    tmdb = clean_tmdb()
    boxoffice = clean_boxoffice()
    reference = clean_reference()

    final = create_final_dataset(tmdb, boxoffice, reference)

    print("Cleaning complete.")
    print(f"TMDB rows: {len(tmdb)}")
    print(f"Box office rows: {len(boxoffice)}")
    print(f"Reference rows: {len(reference)}")
    print(f"Final dataset rows: {len(final)}")
    print("Files saved in data/processed/")


if __name__ == "__main__":
    main()