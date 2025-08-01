from fastapi.testclient import TestClient
from rpp.main import app
import logging
from .common import get_credentials
import uuid
import pytest

logging.basicConfig(level=logging.DEBUG)

def random_hostname():
    return f"ns-{uuid.uuid4().hex[:8]}.rpp.example.org"

@pytest.fixture(scope="module")
def test_hostname():
    return random_hostname()

@pytest.mark.order(1)
def test_create_host(get_credentials, test_hostname):
    with TestClient(app) as client:
        payload = {
            "name": test_hostname,
        }
        response = client.post("/hosts/", json=payload, auth=get_credentials)
        assert response.status_code == 201
        #assert response.json().get("name") == test_hostname

@pytest.mark.order(2)
def test_get_host(get_credentials, test_hostname):
    with TestClient(app) as client:
        # Assume host was created in test_create_host
        response = client.get(f"/hosts/{test_hostname}", auth=get_credentials)
        assert response.status_code == 200
        #assert response.json().get("name") == test_hostname

@pytest.mark.order(3)
def test_head_host_availability(get_credentials, test_hostname):
    with TestClient(app) as client:
        response = client.head(f"/hosts/{test_hostname}/availability", auth=get_credentials)
        assert response.status_code == 200

@pytest.mark.order(4)
def test_patch_host(get_credentials, test_hostname):
    with TestClient(app) as client:
        patch_payload = {
            "add": {
                "addr": [],
                "status": [{"name": "clientUpdateProhibited"}]
            }
        }
        response = client.patch(f"/hosts/{test_hostname}", json=patch_payload, auth=get_credentials)
        assert response.status_code == 200

@pytest.mark.order(5)
def test_delete_host(get_credentials, test_hostname):
    with TestClient(app) as client:
        response = client.delete(f"/hosts/{test_hostname}", auth=get_credentials)
        assert response.status_code == 204


