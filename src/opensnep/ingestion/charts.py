import requests
import pandas as pd
from bs4 import BeautifulSoup


BASE_WEEKLY_CHART_URL = (
    "https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/"
)

BASE_RADIO_CHART_URL = (
    "https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/"
)

CHART_CATEGORIES = {
    "Top Albums": None,
    "Top Singles": "Top%20Singles",
    "Top Albums Classique": "Top%20Albums%20Classique",
    "Top Albums Jazz": "Top%20Albums%20Jazz",
    "Top Rock & Metal": "Top%20Rock%20%2526%20Metal",
    "Top Albums Physiques": "Top%20Albums%20Physiques",
    "Top Radio": None,
}


def build_chart_url(chart_name: str, year: int, week: int) -> str:
    if chart_name not in CHART_CATEGORIES:
        raise ValueError(f"Unknown chart name: {chart_name}")
    
    if chart_name == "Top Radio":
        return f"{BASE_RADIO_CHART_URL}?annee={year}&semaine={week}"

    url = f"{BASE_WEEKLY_CHART_URL}?annee={year}&semaine={week}"

    category_param = CHART_CATEGORIES[chart_name]

    if category_param:
        url += f"&categorie={category_param}"

    return url


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
    chart_name: str,
    year: int,
    week: int,
) -> pd.DataFrame:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    url = build_chart_url(chart_name, year, week)

    response = session.get(url, timeout=50)
    response.raise_for_status()

    df = parse_chart_html(response.text)

    if df.empty:
        raise ValueError(
            f"No chart item found for {chart_name} {year} week {week}"
        )

    df["chart_name"] = chart_name
    df["source_year"] = year
    df["source_week"] = week

    return df