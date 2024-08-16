from fastapi.testclient import TestClient # type: ignore
from main import app

client = TestClient(app)

def test_get_top_news():
    response = client.get("/")
    assert response.status_code == 200
    