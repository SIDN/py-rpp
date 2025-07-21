from fastapi.testclient import TestClient
from rpp.main import app
import logging
import pytest
import yaml
from pathlib import Path
from .common import get_credentials

logging.basicConfig(level=logging.DEBUG)

def test_root(get_credentials):
    with TestClient(app) as client:
        response = client.get("/", auth=get_credentials)
        assert response.status_code == 200


#TODO: #5 Add more tests for the API endpoints