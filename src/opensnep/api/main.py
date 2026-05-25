import os 
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


from fastapi import FastAPI, Query, HTTPException, Request
from opensnep.database import query
from opensnep.api.schemas import CertificationResponse, ChartEntryResponse, CountResponse, ArtistCountResponse, LabelCountResponse, CategoryCountResponse, CertificationLevelResponse, YearCountResponse, NumberOneEntriesResponse
from opensnep.api.schemas import ChartName, CategoryName
from sqlalchemy import text
from opensnep.database.connection import engine
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI(title="OpenSnep API",
              description="Open data API for French music certifications and charts",
              version=os.getenv("API_VERSION", "1.0.0"),
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def raise_404_if_empty(rows, message: str):
    if not rows:
        raise HTTPException(status_code=404, detail=message)

# =======
# Root
# =======

@app.get("/", tags=["Root"], 
         summary="API overview", 
         description="Returns general information about OpenSnep and available resources.")
def root():
    return {
        "name": "OpenSnep API",
        "version": "1.0.0",
        "description": "French music data API powered by SNEP charts and certifications",
        "documentation": "/docs",
        "resources": [
            "/certifications",
            "/charts",
            "/artists/JUL",
            "/stats/top-artists",

        ],
    }

# =============
# Health check
# =============

@app.get(
    "/health",
    tags=["Root"],
    summary="Health check",
    description="Returns API health status"
)
@limiter.limit("120/minute")
def health(request: Request):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
    
# ================
# Certifications
# ================

@app.get("/certifications/count", 
         tags=["Certifications"], 
         response_model=CountResponse,
         summary="Count certification entries",
         description="Returns total number of certifications, optionally filtered by category")
@limiter.limit("120/minute")
def certifications_count(
    request: Request,
    category: CategoryName | None = None):
    return {
        "count": query.count_certifications(category)
    }

@app.get("/certifications",
        tags=["Certifications"],
        response_model=list[CertificationResponse],
        summary="Search certification entries",
        description="""
Filter certification entries by:

- artist
- title
- category
- year
- certification

Supports pagination with `skip` and `limit`.
"""
)
@limiter.limit("30/minute")
def certifications(
    request: Request,
    artist: str | None = None,
    title: str | None = None,
    category: CategoryName | None = None,
    year: int | None = None,
    certification: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = query.search_certifications(
        artist=artist,
        title=title,
        category=category.value if category else None,
        year=year,
        certification=certification,
        skip=skip,
        limit=limit,
    )
    return rows



# ==========
# Artists
# ==========

@app.get("/artists/{name}",
        tags=["Artists"],
        response_model=list[CertificationResponse],
        summary="Get artist certifications",
        description="""
Return certification records for a specific artist.

Optionally filter by category.

Supports pagination with `skip` and `limit`.
""")
@limiter.limit("60/minute")
def artist(
    request: Request,
    name: str,
    category: CategoryName | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = query.get_artist(
        name=name,
        category=category.value if category else None,
        skip=skip,
        limit=limit,
    )

    raise_404_if_empty(
        rows,
        "No certifications found for artist '{name}.",
    )
    return rows


@app.get(
    "/artists/{name}/charts",
    tags=["Artists"],
    response_model=list[ChartEntryResponse],
    summary="Get artist chart history",
    description="""
Return weekly chart history for a specific artist.

Optionally filter by chart name.

Supports pagination with `skip` and `limit`.
""",
)
@limiter.limit("60/minute")
def artist_charts(
    request: Request,
    name: str,
    chart_name: ChartName | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = query.artist_chart_history(
        artist=name,
        chart_name=chart_name.value if chart_name else None,
        skip=skip,
        limit=limit,
    )

    raise_404_if_empty(
        rows,
        f"No chart history found for artist '{name}'.",
    )
    return rows


@app.get("/artists/{name}/certifications",
        tags=["Artists"],
        response_model=list[CertificationLevelResponse],
        summary="Get artist certification levels",
        description="""
Return certification level breakdown for a specific artist.

Example:
- Or: 12
- Platine: 8
- Diamant: 2
""")
@limiter.limit("60/minute")
def artist_certification_levels(
    request: Request,
    name: str,
    category: CategoryName | None = None,
): 
    rows = query.artist_certifications(
        name=name,
        category=category.value if category else None,
    )
    return [
        {
            "certification": certification,
            "count": count,
        }
        for certification, count in rows
    ]

# =========
# Charts
# =========

@app.get("/charts",
        tags=["Charts"],
        response_model=list[ChartEntryResponse],
        summary="Search weekly chart entries",
        description="""
Filter weekly chart entries by:

- chart_name
- rank
- artist
- title
- label_distributor
- week
- year

Supports pagination with `skip` and `limit`.
"""
)
@limiter.limit("30/minute")
def charts(
    request: Request,
    chart_name: ChartName | None = None,
    rank: int | None = None,
    artist: str | None = None,
    title: str | None = None,
    label_distributor: str | None = None,
    week: int | None = None,
    year: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    rows = query.search_charts(
        chart_name=chart_name.value if chart_name else None,
        rank=rank,
        artist=artist,
        title=title,
        label_distributor=label_distributor,
        week=week,
        year=year,
        skip=skip,
        limit=limit,
    )
    return rows


@app.get("/charts/count", 
         tags=["Charts"], 
         response_model=CountResponse, 
         summary="Count chart entries", 
         description="Returns total number of chart rows, opyionally filtered by chart_name.")
@limiter.limit("120/minute")
def chart_entries_count(
    request: Request,
    chart_name: ChartName | None = None,
):
    return {
        "count": query.count_chart_entries(chart_name)
    }


@app.get("/charts/week",
        tags=["Charts"],
        response_model=list[ChartEntryResponse],
        summary="Get weekly chart snapshot",
        description="""
Return a full weekly chart ranking for a given:

- chart_name
- year
- week

Results are ordered by rank ascending.
""")
@limiter.limit("30/minute")
def charts_week(
    request: Request,
    chart_name: ChartName,
    week: int,
    year: int,
):
    rows = query.get_chart_week(
        chart_name=chart_name.value,
        week=week,
        year=year,
    )
    raise_404_if_empty(
        rows,
        "No chart entries found for this chart, year and week.",
    )
    return rows

# =========
# Stats
# =========

@app.get("/stats/charts/top-artists",
        tags=["Stats"],
        response_model=list[ArtistCountResponse],
        summary="Top chart artists", 
        description="Returns artists with the highest number of chart appearances.")
@limiter.limit("20/minute")
def charts_top_artists(
    request: Request,
    chart_name: ChartName | None = None,
    limit: int = 10
):
    rows = query.top_chart_artists(
        chart_name=chart_name.value if chart_name else None,
        limit=limit
    )
    return [
        {
        "artist": artist,
        "count": count,
        } 
        for artist, count in rows
    ] 


@app.get("/stats/charts/top-distributors",
        tags=["Stats"],
        response_model=list[LabelCountResponse],
        summary="Top chart distributors",
        description="""
Return labels / distributors with the highest number of chart entries.

Optionally filter by chart name.
""")
@limiter.limit("20/minute")
def charts_top_distributors(
    request: Request,
    chart_name: ChartName | None = None,
    limit: int = 10
):
    rows = query.top_chart_distributors(
        chart_name=chart_name.value if chart_name else None,
        limit=limit
    )
    return [
        {
        "label_distributor": label_distributor,
        "count": count,
        } 
        for label_distributor, count in rows
    ] 


@app.get("/stats/charts/number-ones",
        tags=["Stats"],
        response_model=list[NumberOneEntriesResponse],
        summary="Number one chart entries",
        description="""
Return artists with the most number one chart entries.

Can filter by:
- artist
- chart_name
""")
@limiter.limit("20/minute")
def charts_number_ones(
    request: Request,
    artist: str | None = None,
    chart_name: ChartName | None = None,
    limit: int = 10,
):
    chart_name_value = chart_name.value if chart_name else None
    rows = query.entries_at_number_one(
        artist=artist,
        chart_name=chart_name_value,
        limit=limit,
    )

    if artist:
        return [
            {
            "artist": artist,
            "chart_name": chart_name_value,
            "weeks_at_number_one": rows,
            }
        ]

    return [
        {    
            "artist": artist_name,
            "chart_name": chart_name_value,
            "weeks_at_number_one": count,
        }
        for artist_name, count in rows
    ]


@app.get("/stats/by-category",
        tags=["Stats"],
        response_model=list[CategoryCountResponse],
        summary="Certification counts by category",
        description="Return number of certifications grouped by category.")
@limiter.limit("20/minute")
def stats_by_category(request: Request):
    rows = query.count_by_category()
    return [
        {
            "category": category,
            "count": count,
        }
        for category, count in rows
    ]


@app.get("/stats/by-year",
        tags=["Stats"],
        response_model=list[YearCountResponse],
        summary="Certification counts by year",
        description="Return number of certifications grouped by source year.")
@limiter.limit("20/minute")
def stats_by_year(request: Request):
    rows = query.count_by_year()
    return [
        {
            "year": year,
            "count": count,
        }
        for year, count in rows
    ]


@app.get("/stats/top-artists",
        tags=["Stats"],
        response_model=list[ArtistCountResponse],
        summary="Top certified artists",
        description="""
Return artists with the highest number of certifications.

Optionally filter by category.
""")
@limiter.limit("20/minute")
def stats_top_artists(
    request: Request,
    category: CategoryName | None = None,
    limit: int = 10,
):
    rows = query.top_artists(
        category=category.value if category else None,
        limit=limit,
    )
    return [
        {
            "artist": artist,
            "count": count,
        }
        for artist, count in rows
    ]


@app.get("/stats/top-distributors",
        tags=["Stats"],
        response_model=list[LabelCountResponse],
        summary="Top distributors by certifications",
        description="""
Return distributors / labels with the highest number of certifications.

Optionally filter by category.
""")
@limiter.limit("20/minute")
def stats_top_distributors(
    request: Request,
    category: CategoryName | None = None,
    limit: int = 10,
):
    rows = query.top_distributors(
        category=category.value if category else None,
        limit=limit,
    )
    return [
        {
            "label_distributor": label_distributor,
            "count": count,
        }
        for label_distributor, count in rows
    ]


@app.get("/stats/certification-levels",
        tags=["Stats"],
        response_model=list[CertificationLevelResponse],
        summary="Certification level breakdown",
        description="""
Return counts by certification level.

Example:
- Or
- Platine
- Diamant
""")
@limiter.limit("20/minute")
def stats_certification_levels(
    request: Request,
    category: CategoryName | None = None):
    rows = query.certification_by_levels(category=category.value if category else None)

    return [
        {
            "certification": certification,
            "count": count,
        }
        for certification, count in rows ]

