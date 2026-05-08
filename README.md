# OpenSnep

OpenSnep is an open data API for French music certifications and weekly
charts, powered by SNEP data.

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
- FastAPI REST API with Swagger docs
- SQLite database with indexes and uniqueness constraints
- Automated update scripts with logging
- Automated API tests with pytest

## Project structure

```text
OpenSnep/
├── data/
├── logs/
├── notebooks/
├── scripts/
│   ├── update_charts.py
│   └── update_certifications.py
├── src/
│   └── opensnep/
│       ├── api/
│       ├── cleaning/
│       ├── database/
│       ├── ingestion/
│       └── parsing/
├── tests/
├── .env
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Installation

Create a virtual environment and install:

```bash
pip install -e .
pip install -r requirements-dev.txt
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

## Update scripts

Update charts:

```bash
python scripts/update_charts.py
```

Update certifications:

```bash
python scripts/update_certifications.py
```

## Tests

Run:

```bash
pytest
```

## Tech stack

- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- BeautifulSoup
- Requests
- Pytest

## License

Open data project for educational and analytical use.
