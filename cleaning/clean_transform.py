import pandas as pd
import re
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_title(title):
    if pd.isna(title):
        return None

    title = str(title).lower().strip()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)

    return title


def clean_revenue(value):
    if pd.isna(value):
        return None

    value = str(value)
    value = re.sub(r"[^0-9.]", "", value)

    if value == "":
        return None

    return float(value)


def extract_year(value):
    if pd.isna(value):
        return None

    date = pd.to_datetime(value, errors="coerce")

    if pd.isna(date):
        return None

    return int(date.year)


def clean_tmdb():
    tmdb_path = RAW_DIR / "tmdb_raw.json"
    tmdb = pd.read_json(tmdb_path)

    tmdb["title_clean"] = tmdb["title"].apply(clean_title)
    tmdb["year"] = tmdb["release_date"].apply(extract_year)

    tmdb = tmdb.drop_duplicates(subset=["title_clean", "year"])

    tmdb.to_csv(PROCESSED_DIR / "tmdb_clean.csv", index=False)
    return tmdb


def clean_boxoffice():
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
    reference_path = RAW_DIR / "Top_200_Movies_Dataset_2023.csv"
    reference = pd.read_csv(reference_path)

    title_column = "title" if "title" in reference.columns else reference.columns[0]
    reference["title_clean"] = reference[title_column].apply(clean_title)

    if "year" in reference.columns:
        reference["year"] = pd.to_numeric(reference["year"], errors="coerce")
    elif "release_date" in reference.columns:
        reference["year"] = reference["release_date"].apply(extract_year)

    if "year" in reference.columns:
        reference = reference.drop_duplicates(subset=["title_clean", "year"])
    else:
        reference = reference.drop_duplicates(subset=["title_clean"])

    reference.to_csv(PROCESSED_DIR / "movies_reference_clean.csv", index=False)
    return reference


def create_final_dataset(tmdb, boxoffice, reference):
    """
    Integrates TMDB and Box Office as the primary matched dataset,
    then adds reference data as supplementary enrichment.
    """
    print("Creating final dataset...")

    # Main merge: keep only movies matched between TMDB and Box Office
    main_df = pd.merge(
        tmdb,
        boxoffice,
        on=["title_clean", "year"],
        how="inner",
        suffixes=("_tmdb", "_box")
    )

    print("Matched TMDB + Box Office:", len(main_df))

    # Add reference dataset as optional enrichment
    if "year" in reference.columns:
        final_df = pd.merge(
            main_df,
            reference,
            on=["title_clean", "year"],
            how="left"
        )
    else:
        final_df = pd.merge(
            main_df,
            reference,
            on=["title_clean"],
            how="left"
        )

    final_dataset = pd.DataFrame()

    if "title_box" in final_df.columns:
        final_dataset["title"] = final_df["title_box"]
    elif "title_tmdb" in final_df.columns:
        final_dataset["title"] = final_df["title_tmdb"]
    elif "title" in final_df.columns:
        final_dataset["title"] = final_df["title"]

    final_dataset["title_clean"] = final_df["title_clean"]
    final_dataset["year"] = final_df["year"]

    if "revenue" in final_df.columns:
        final_dataset["revenue"] = final_df["revenue"]

    if "vote_average" in final_df.columns:
        final_dataset["vote_average"] = final_df["vote_average"]

    if "popularity" in final_df.columns:
        final_dataset["popularity"] = final_df["popularity"]

    if "genres" in final_df.columns:
        final_dataset["genres"] = final_df["genres"]

    if "Rank" in final_df.columns:
        final_dataset["rank_ref"] = final_df["Rank"]

    if "Distributor" in final_df.columns:
        final_dataset["distributor"] = final_df["Distributor"]

    if "Total Gross" in final_df.columns:
        final_dataset["total_gross_ref"] = final_df["Total Gross"]

    if "Theaters" in final_df.columns:
        final_dataset["theaters_ref"] = final_df["Theaters"]

    if "Release Date" in final_df.columns:
        final_dataset["release_date_ref"] = final_df["Release Date"]

    output_path = PROCESSED_DIR / "final_dataset.csv"
    final_dataset.to_csv(output_path, index=False)

    print(f"Final dataset saved at: {output_path}")
    print("Final dataset rows:", len(final_dataset))

    return final_dataset

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