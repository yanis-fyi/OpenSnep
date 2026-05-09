# scripts/backfill_certifications.py
from opensnep.ingestion.certifications import crawl_certifications
from opensnep.cleaning.certifications import clean_certifications
from opensnep.database.load import load_certifications

CATEGORIES = ["Singles", "Albums"]

for year in range(1994, 2027):
    for category in CATEGORIES:
        print(f"Backfilling certifications {category} {year}")

        df_raw = crawl_certifications(year=year, category=category)
        df_clean = clean_certifications(df_raw)
        load_certifications(df_clean)