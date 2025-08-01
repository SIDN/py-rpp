from fastapi.testclient import TestClient
from rpp.main import app
import logging
from .common import get_credentials

logging.basicConfig(level=logging.DEBUG)

def test_root(get_credentials):
    with TestClient(app) as client:
        response = client.get("/", auth=get_credentials)
        assert response.status_code == 200

