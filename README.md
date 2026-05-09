# OpenSnep

OpenSnep is an open data API for French music certifications and weekly
charts, powered by SNEP data.

---

## Live API

**Base URL**  
https://opensnep.up.railway.app

**Swagger Docs**  
https://opensnep.up.railway.app/docs

**Health Check**  
https://opensnep.up.railway.app/health

---

## Features

- **Certifications dataset**

  - Singles
  - Albums

- **Weekly charts dataset**

  - Top Albums
  - Top Singles
  - Top Albums Classique
  - Top Albums Jazz
  - Top Rock & Metal
  - Top Albums Physiques
  - Top Radio

- **API**
- FastAPI REST API
- Swagger documentation
- PostgreSQL production database
- SQLite local development
- Indexed schema + uniqueness constraints
- Automated update scripts
- Automated tests with pytest

---

## Project structure

```text
OpenSnep/
├── data/
├── logs/
├── notebooks/
├── scripts/
│   ├── backfill_certifications.py
│   ├── backfill_charts.py
│   ├── backfill_top_radio.py
│   ├── update_charts.py
│   ├── update_certifications.py
│   └── migrate_sqlite_to_postgres.py
├── src/
│   └── opensnep/
│       ├── api/
│       ├── cleaning/
│       ├── database/
│       └── ingestion/
│
├── tests/
├── .env
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── README.md
```

## Installation

Create a virtual environment then:

Install base dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Or install the package in editable mode:

```bash
pip install -e .
```

## Configuration

Create a `.env` file:

```env
DATABASE_PATH=./data/opensnep.db
LOG_LEVEL=INFO
API_VERSION=0.1.0
```

## Run locally

Start the API:

```bash
uvicorn opensnep.api.main:app --reload
```

Swagger UI:

- `/docs`
- `/redoc`

Health check:

- `/health`

## Example endpoints

- `/certifications`
- `/charts`
- `/charts/week?chart_name=Top Albums&year=2026&week=18`
- `/artists/JUL`
- `/artists/JUL/charts?chart_name=Top Radio`
- `/stats/charts/top-artists`
- `/stats/top-distributors`

## Backfill scripts

Used to rebuild historical datasets.

```bash
python scripts/backfill_certifications.py
python scripts/backfill_charts.py
python scripts/backfill_top_radio.py
```

## Update scripts

Used for incremental updates
Update charts:

```bash
python scripts/update_charts.py
```

Update certifications:

```bash
python scripts/update_certifications.py
```

## Migration

Used to migrate local SQLite data to PostgreSQL

```bash
pytest
```

## Tests

Run:

```bash
pytest
```

## Tech stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- SQLite
- Pandas
- BeautifulSoup
- Requests
- Pytest
- Railway

## License

Open data project for educational and analytical use.
