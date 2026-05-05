from fastapi import FastAPI
from opensnep.database import query

app = FastAPI(title="OpenSnep API",
              description="Open data API for French music certifications and charts",
              version="0.1.0",

)

@app.get("/", tags=["Root"])
def root():
    return {
        "name": "OpenSnep API",
        "version": "0.1.0",
        "description": "French music data API powered by SNEP charts and certifications",
        "resources": {
            "certifications": "/certifications",
            "artists": "/artists/{name}",
            "stats": "/stats",
            "docs": "/docs",

        },
    }

@app.get("/certifications/count", tags=["Certifications"])
def certifications_count(category: str | None = None):
    return {
        "count": query.count_certifications(category)
    }

@app.get("/stats/by-category", tags=["Stats"])
def stats_by_category():
    rows = query.count_by_category()
    return [
        {
            "category": category,
            "count": count,
        }
        for category, count in rows
    ]

@app.get("/stats/by-year", tags=["Stats"])
def stats_by_year():
    rows = query.count_by_year()
    return [
        {
            "year": year,
            "count": count,
        }
        for year, count in rows
    ]

@app.get("/stats/top-artists", tags=["Stats"])
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

@app.get("/stats/top-distributors", tags=["Stats"])
def stats_top_distributors(
    category: str | None = None,
    limit: int = 10,
):
    rows = query.top_distributors(
        category=category,
        limit=limit,
    )
    return [
        {
            "label_distributor": label_distributor,
            "count": count,
        }
        for label_distributor, count in rows
    ]

@app.get("/stats/certification-levels", tags=["Stats"])
def stats_certification_levels(category: str | None = None):
    rows = query.certification_by_levels(category=category)

    return [
        {
            "certification": certification,
            "count": count,
        }
        for certification, count in rows
    ]

@app.get("/certifications", tags=["Certifications"])
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

@app.get("/artists/{name}", tags=["Artists"])
def artist(
    name: str,
    category: str | None = None,
):
    rows = query.get_artist(
        name=name,
        category=category,
    )
    return rows

@app.get("/artists/{name}/certifications", tags=["Artists"])
def artist_certification_levels(
    name: str,
    category: str | None = None,
): 
    rows = query.artist_certifications(
        name=name,
        category=category,
    )
    return [
        {
            "certification": certification,
            "count": count,
        }
        for certification, count in rows
    ]