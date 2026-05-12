
from pathlib import Path
import re

import pandas as pd
from sqlalchemy import text

from opensnep.database.connection import engine


def get_main_artist(artist: str) -> str:
    if artist is None:
        return ""

    artist = str(artist).strip()

    # split on common featuring / collaboration patterns
    pattern = r"\s+(FEAT\.?|FT\.?|AVEC|WITH|X|&|/)\s+|\s*,\s*"

    parts = re.split(pattern, artist, flags=re.IGNORECASE)

    return parts[0].strip()


with engine.begin() as conn:
    print("Reading certifications...")

    df = pd.read_sql(
        text("""
            SELECT id, interprete, interprete_principal
            FROM certifications
        """),
        conn,
    )

    df["new_interprete_principal"] = df["interprete"].apply(get_main_artist)

    changed = df[
        df["interprete_principal"] != df["new_interprete_principal"]
    ]

    print(f"Rows to update: {len(changed)}")

    for _, row in changed.iterrows():
        conn.execute(
            text("""
                UPDATE certifications
                SET interprete_principal = :new_artist
                WHERE id = :id
            """),
            {
                "new_artist": row["new_interprete_principal"],
                "id": int(row["id"]),
            },
        )

    print("Database artist names updated.")


query = """
SELECT
    interprete_principal AS artist,
    categorie AS category,
    certification AS certification,
    COUNT(*) AS count
FROM certifications
GROUP BY interprete_principal, categorie, certification
ORDER BY artist, category, certification
"""

df_export = pd.read_sql(text(query), engine)

output_dir = Path("exports")
output_dir.mkdir(exist_ok=True)

output_path = output_dir / "certifications_summary.csv"
df_export.to_csv(output_path, index=False)

print(f"Exported {len(df_export)} rows to {output_path}")