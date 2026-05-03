import re
import time
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

    response = session.get(url, timeout=50)
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


#parse html code
def parse_certifications_from_html(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for block in soup.select("div.certification"):
        def get_text(selector: str) -> str | None:
            element = block.select_one(selector)
            return element.get_text(" ", strip=True) if element else None

        dates = {}

        for date_block in block.select("div.block_dates div.date"):
            label = date_block.select_one("span")

            if label:
                label_text = label.get_text(" ", strip=True)
                label.extract()
                dates[label_text] = date_block.get_text(" ", strip=True)

        records.append(
            {
                "Interprete": get_text(".artiste"),
                "Titre": get_text(".titre"),
                "Éditeur / Distributeur": get_text(".editeur"),
                "Catégorie": get_text(".categorie"),
                "Certification": get_text(".certif"),
                "Date de sortie": dates.get("Date de sortie"),
                "Date de constat": dates.get("Date de constat"),
            }
        )

    return pd.DataFrame(records)

 
# crawl certifications page 
def crawl_certifications(
    year: int,
    category: str = "Singles",
    sleep_seconds: float = 1,
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

        page_response = page_session.get(url, timeout=50)
        page_response.raise_for_status()

        df_page = parse_certifications_from_html(page_response.text)

        if df_page.empty:
            raise ValueError(f"No certifications found on page {page}")

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