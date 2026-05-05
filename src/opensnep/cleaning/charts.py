import pandas as pd

COLUMN_MAPPING = {
    "chart_slug": "chart_name",
    "source_week": "week",
    "source_year": "year",
}

TEXT_COLUMNS = [
    "chart_name",
    "artist",
    "title",
    "label_distributor",
]

CHART_NAMES = {
    "top-albums": "Top Albums",
    "top-singles": "Top Singles",
    "top-albums-classique": "Top Albums Classique",
    "top-albums-jazz": "Top Albums Jazz",
    "top-rock-metal": "Top Rock & Metal",
    "top-albums-physiques": "Top Albums Physiques",
}

def clean_charts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.rename(columns=COLUMN_MAPPING)

    for column in TEXT_COLUMNS:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
    df["chart_name"] = (df["chart_name"].map(CHART_NAMES).fillna(df["chart_name"]))
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce").astype("Int64")
    df["week"] = pd.to_numeric(df["week"], errors="coerce").astype("Int64")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    return df[
        [
            "chart_name",
            "rank",
            "artist",
            "title",
            "label_distributor",
            "week",
            "year",
        ]
    ]