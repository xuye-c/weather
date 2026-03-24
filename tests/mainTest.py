import pytest
from weather_app.run import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_insert_route(client):
    response = client.post("/insert", data={
        "city": "Durham",
        "date": "2026-03-24",
        "temperature": "20"
    })

    assert response.status_code == 200
    assert b"OK" in response.data


def test_search_route(client):
    response = client.post("/search", data={
        "city": "Durham",
        "start_date": "2026-03-20",
        "end_date": "2026-03-24"
    })

    assert response.status_code == 200
    assert b"Searching" in response.data