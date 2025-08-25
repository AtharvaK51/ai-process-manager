from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "processes" in data
    assert isinstance(data["processes"], list)
