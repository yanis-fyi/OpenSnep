import requests 
import pandas as pd
from bs4 import BeautifulSoup

BASE_CHART_URL = "https://snepmusique.com/les-tops/le-top-de-la-semaine"

CHART_SLUGS = {
    "top_albums": "top-albums",
    "top_singles": "top-singles",
    "top_albums_classique": "top-albums-classique",
    "top_albums_jazz": "top-albums-jazz",
    "top_rock_metal": "top-rock-metal",
    "top_albums_physiques": "top-albums-physiques",
}


def build_chart_url(chart_slug: str, year: int, week: int) -> str:
    return f"{BASE_CHART_URL}/{chart_slug}/?annee={year}&semaine={week}"


def parse_chart_html(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for item in soup.select("div.items div.item"):

        def get_text(selector: str) -> str | None:
            element = item.select_one(selector)
            return element.get_text(" ", strip=True) if element else None

        records.append(
            {
                "rank": get_text(".rang"),
                "title": get_text(".titre"),
                "artist": get_text(".artiste"),
                "label_distributor": get_text(".editeur"),
                
            }
        )

    return pd.DataFrame(records)



def crawl_chart(
    chart_slug: str,
    year: int,
    week: int,

) -> pd.DataFrame:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    url = build_chart_url(chart_slug, year, week)

    response = session.get(url, timeout=50)
    response.raise_for_status()

    df = parse_chart_html(response.text)

    if df.empty:
        raise ValueError(f"No chart item found for {chart_slug} {year} week {week}")
    
    df["chart_slug"] = chart_slug
    df["source_year"] = year
    df["source_week"] = week
    df["source_url"] = url

    return df