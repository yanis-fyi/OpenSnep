import pandas as pd
import re

COLUMN_MAPPING = {
    "Interprete": "interprete",
    "Titre": "titre",
    "Éditeur / Distributeur": "editeur_distributeur",
    "Catégorie": "categorie",
    "Certification": "certification",
    "Date de sortie": "date_sortie",
    "Date de constat": "date_constat",
    "source_page": "source_page",
    "source_year": "source_year",
    "source_category": "source_category",
}


TEXT_COLUMNS = [
    "interprete",
    "titre",
    "editeur_distributeur",
    "categorie",
    "certification",
    "source_category",
]


DATE_COLUMNS = [
    "date_sortie",
    "date_constat",
]

COLLAB_PATTERN = re.compile(
    r"(?:\s+(?:FEAT\.?|FT\.?|FEATURING|AVEC|WITH|X|&|/)\s+|\s*,\s*)",
    flags=re.IGNORECASE,
)


def get_main_artist(artist: str) -> str:
    if pd.isna(artist):
        return ""
    
    artist = str(artist).strip()
    parts = COLLAB_PATTERN.split(artist)

    return parts[0].strip()

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column in TEXT_COLUMNS:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

    return df


def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                dayfirst=True,
                errors="coerce",
            )

    return df


def clean_certifications(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.rename(columns=COLUMN_MAPPING)

    df = clean_text_columns(df)
    df = clean_date_columns(df)
    

    if "interprete" in df.columns:
        df["interprete_principal"] = df["interprete"].apply(get_main_artist)
    

    ordered_columns = [
        "interprete",
        "interprete_principal",
        "titre",
        "editeur_distributeur",
        "categorie",
        "certification",
        "date_sortie",
        "date_constat",
        "source_page",
        "source_year",
        "source_category",
    ]

    existing_columns = [column for column in ordered_columns if column in df.columns]

    df = df[existing_columns]

    return df