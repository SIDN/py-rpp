from fastapi.testclient import TestClient
from rpp.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}