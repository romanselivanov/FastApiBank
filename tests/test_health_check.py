from os import environ
from main import app
from fastapi.testclient import TestClient

environ['TESTING'] = 'True'
client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
