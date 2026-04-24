import pandas as pd
import json
from pathlib import Path

RAW_DIR = Path("data/raw")


def load_boxoffice():
    path = RAW_DIR / "boxoffice_raw.csv"
    df = pd.read_csv(path)
    print(f"Loaded box office data: {df.shape}")
    return df


def load_reference():
    path = RAW_DIR / "Top_200_Movies_Dataset_2023.csv"
    df = pd.read_csv(path)
    print(f"Loaded reference data: {df.shape}")
    return df


def load_tmdb():
    path = RAW_DIR / "tmdb_raw.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded TMDB data: {len(data)} records")
    return data


def main():
    print("Starting data ingestion...")

    boxoffice = load_boxoffice()
    reference = load_reference()
    tmdb = load_tmdb()

    print("Data ingestion completed successfully.")


if __name__ == "__main__":
    main()