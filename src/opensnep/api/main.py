from fastapi import FastAPI
from opensnep.database import query

app = FastAPI(title="OpenSnep API")

@app.get("/")
def root():
    return {"message: Welcome to OpenSnep"}

@app.get("/certifications/count")
def certifications_count(category: str | None = None):
    return {
        "count": query.count_certifications(category)
    }

@app.get("/stats/by-category")
def stats_by_category():
    rows = query.count_by_category()
    return [
        {
            "category": category,
            "count": count,
        }
        for category, count in rows
    ]

@app.get("/stats/top-artists")
def stats_top_artists(
    category: str | None = None,
    limit: int = 10,
):
    rows = query.top_artists(
        category=category,
        limit=limit,
    )
    return [
        {
            "artist": artist,
            "count": count,
        }
        for artist, count in rows
    ]

@app.get("/certifications")
def certifications(
    artist: str | None = None,
    title: str | None = None,
    category: str | None = None,
    year: int | None = None,
    certification: str | None = None,
):
    rows = query.search_certifications(
        artist=artist,
        title=title,
        category=category,
        year=year,
        certification=certification,
    )
    return rows