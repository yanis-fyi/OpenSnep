import re
import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests 
from bs4 import BeautifulSoup

#URL Constant
BASE_URL = "https://snepmusique.com/les-certifications"

#Column fields
DATA_COLUMNS = [
    "Interprete",
    "Titre",
    "Éditeur / Distributeur",
    "Catégorie",
    "Certification",
    "Date de sortie",
    "Date de constat",

]
#build the page url
def build_page_url(year: int, category: str, page: int) -> str:
    return f"{BASE_URL}/page/{page}/?categorie={category}&annee={year}"

#discover number of pages
def get_total_pages(session: requests.Session, year: int, category: str) -> int:
    url = build_page_url(year=year, category=category, page=1)

    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        label = link.get_text(" ", strip=True)
        href = link["href"]

        if "Dernière" in label:
            match = re.search(r"/page/(\d+)", href)

            if match:
                return int(match.group(1))

    return 1

#download csv file
def extract_csv_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a", href=True):
        label = link.get_text(" ", strip=True)
        if "CSV" in label.upper():
            return link["href"]
    raise ValueError("CSV link not found on page")

#read csv file
def read_csv_from_url(
    session: requests.Session,
    csv_url: str,
    referer: str,
) -> pd.DataFrame:
    response = session.get(
        csv_url,
        headers={"Referer": referer},
        timeout=30,
    )
    response.raise_for_status()
    decoded_text = response.content.decode("utf-8-sig")

    return pd.read_csv(StringIO(decoded_text), sep=";")

#TODO make it possible to crawl other pages 
# crawl certifications page 
def crawl_certifications(
    year: int,
    category: str = "Singles",
    sleep_seconds: float = 0.5,
) -> pd.DataFrame:
    base_session = requests.Session()
    base_session.headers.update({"User-Agent": "Mozilla/5.0"})

    total_pages = get_total_pages(
        session=base_session,
        year=year,
        category=category,
    )

    print(f"Found {total_pages} pages for {category} {year}")

    all_pages = []

    for page in range(1, total_pages + 1):
        page_session = requests.Session()
        page_session.headers.update({"User-Agent": "Mozilla/5.0"}) #use a fresh session per page

        url = build_page_url(year=year, category=category, page=page)

        print(f"Downloading {category} {year} - page {page}/{total_pages}")

        page_response = page_session.get(url, timeout=30)
        page_response.raise_for_status()

        csv_url = extract_csv_url(page_response.text)

        time.sleep(2) # wait for server-side export/cache

        df_page = read_csv_from_url(
            session=page_session,
            csv_url=csv_url,
            referer=page_response.url,
        )

        print(page, df_page.shape)

        df_page["source_page"] = page
        df_page["source_year"] = year
        df_page["source_category"] = category

        all_pages.append(df_page)

        time.sleep(sleep_seconds)

    df_raw = pd.concat(all_pages, ignore_index=True)

    df_unique = (
        df_raw
        .drop_duplicates(subset=DATA_COLUMNS)
        .reset_index(drop=True)
    )

    print("RAW SHAPE:", df_raw.shape)
    print("UNIQUE SHAPE:", df_unique.shape)

    return df_unique

#save file in processed data
def save_certifications(
    df: pd.DataFrame,
    year: int,
    category: str,
    output_dir: str = "data/processed",
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"certif_{category.lower()}_{year}_clean.csv"
    file_path = output_path / filename
    df.to_csv(file_path, index=False, encoding="utf-8-sig")

    return file_path