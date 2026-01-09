from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_bidon() :
    assert 0 == 1

def test_root() :
    response = client.get("/")
    assert response.status_code == 200