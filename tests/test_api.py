from fastapi.testclient import TestClient
from opensnep.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] =="ok"

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "OpenSnep API"

def test_certifications():
    response = client.get("/certifications?limit=5")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5

def test_charts():
    response = client.get("/charts?limit=5")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5

def test_invalid_chart_name():
    response = client.get("/charts?chart_name=BadChart")

    assert response.status_code == 422

def test_invalid_pagination_limit():
    response = client.get("/charts?limit=1000")

    assert response.status_code == 422

def test_invalid_category():
    response = client.get("/certifications?category=BadCategory")
    assert response.status_code == 422

def test_negative_skip():
    response = client.get("/charts?skip=-1")
    assert response.status_code == 422

def test_unknown_artist():
    response = client.get("/artists/THIS_ARTIST_DOES_NOT_EXIST_12345")
    assert response.status_code == 404

def test_unknown_artist_charts():
    response = client.get("/artists/THIS_ARTIST_DOES_NOT_EXIST_12345/charts")
    assert response.status_code == 404

def test_unknown_chart_week():
    response = client.get(
        "/charts/week?chart_name=Top Albums&year=1900&week=1"
    )
    assert response.status_code == 404

# Business logic tests

def test_jul_has_certifications():
    response = client.get("/artists/JUL")

    assert response.status_code == 200
    assert len(response.json()) > 0

def test_top_radio_exists():
    response = client.get("/charts?chart_name=Top Radio&limit=5")

    assert response.status_code == 200
    assert len(response.json()) > 0

# Response shape tests

def test_certification_shape():
    response = client.get("/certifications?limit=1")

    row = response.json()[0]

    assert "artist" in row
    assert "title" in row
    assert "category" in row


def test_chart_shape():
    response = client.get("/charts?limit=1")

    row = response.json()[0]

    assert "chart_name" in row
    assert "rank" in row
    assert "artist" in row