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

    # Drop duplicates safely depending on whether year exists
    if "year" in reference.columns:
        reference = reference.drop_duplicates(subset=["title_clean", "year"])
    else:
        reference = reference.drop_duplicates(subset=["title_clean"])

    reference.to_csv(PROCESSED_DIR / "movies_reference_clean.csv", index=False)

    return reference