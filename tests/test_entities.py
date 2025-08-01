from fastapi.testclient import TestClient
from rpp.main import app
import logging
from .common import get_credentials
import uuid
import pytest

logging.basicConfig(level=logging.DEBUG)

def random_entity_id():
    return f"ent-{uuid.uuid4().hex[:8]}"

@pytest.fixture(scope="module")
def test_entity_id():
    return random_entity_id()

@pytest.mark.order(1)
def test_create_entity(get_credentials, test_entity_id):
    with TestClient(app) as client:
        payload = {
                    "clTRID": "ABC-1234",
                    "authInfo": {
                        "value": "XYZ12345"
                    },
                    "card": {
                        "@type": "Card",
                        "version": "2.0",
                        "rpp.ietf.org:id": test_entity_id,
                        "rpp.ietf.org:legalForm": {
                            "name": "PERSOON",
                            "number": "12345"
                    },
                        "name": {
                            "full": "Maarten Wulliak",
                            "components": [
                                {
                                    "kind": "surname",
                                    "value": "Maarten"
                                },
                                {
                                    "kind": "given",
                                    "value": "Wullink"
                                }
                            ]
                        },
                        "organizations": {
                            "org": {
                                "name": "Org Example"
                            }
                        },
                        "addresses": {
                            "addr": {
                                "components": [
                                    {
                                        "kind": "name",
                                        "value": "Main Street 1"
                                    },
                                    {
                                        "kind": "locality",
                                        "value": "Ludwigshafen am Rhein"
                                    },
                                    {
                                        "kind": "region",
                                        "value": "Rhineland-Palatinate"
                                    },
                                    {
                                        "kind": "postcode",
                                        "value": "67067"
                                    },
                                    {
                                        "kind": "country",
                                        "value": "Germany"
                                    }
                                ],
                                "countryCode": "DE",
                                "coordinates": "geo:49.477409, 8.445180"
                            },
                            "addresses-1": {
                                "full": "Somewhere Street 1 Mutterstadt 67112 Germany",
                                "contexts": {
                                    "private": True
                                }
                            }
                        },
                        "phones": {
                            "voice": {
                                "features": {
                                    "voice": True
                                },
                                "number": "+31.621263322"
                            }
                        },
                        "emails": {
                            "email": {
                                "address": "joe.user@example.com"
                            }
                        }
                    }
                }   
        response = client.post("/entities/", json=payload, auth=get_credentials)
        assert response.status_code == 201
        # Optionally: assert response.json().get("id") == test_entity_id

@pytest.mark.order(2)
def test_get_entity(get_credentials, test_entity_id):
    with TestClient(app) as client:
        response = client.get(f"/entities/{test_entity_id}", auth=get_credentials)
        assert response.status_code == 200

@pytest.mark.order(3)
def test_patch_entity(get_credentials, test_entity_id):
    with TestClient(app) as client:
        patch_payload = {
                    "change": {
                        "card": 
                            {
                                "name": {
                                    "full": "Maarten Wulliak 2",
                                    "components": [
                                        {
                                            "kind": "surname",
                                            "value": "Maarten"
                                        },
                                        {
                                            "kind": "given",
                                            "value": "Wullink"
                                        }
                                    ]
                                },
                                "organizations": {
                                    "org": {
                                        "name": "Org Example 2"
                                    }
                                },
                                "addresses": {
                                    "addr": {
                                        "components": [
                                            {
                                                "kind": "name",
                                                "value": "Main Street 1"
                                            },
                                            {
                                                "kind": "locality",
                                                "value": "Ludwigshafen am Rhein"
                                            },
                                            {
                                                "kind": "region",
                                                "value": "Rhineland-Palatinate"
                                            },
                                            {
                                                "kind": "postcode",
                                                "value": "67067"
                                            },
                                            {
                                                "kind": "country",
                                                "value": "Germany"
                                            }
                                        ],
                                        "countryCode": "DE",
                                        "coordinates": "geo:49.477409, 8.445180"
                                    },
                                    "addresses-1": {
                                        "full": "Somewhere Street 1 Mutterstadt 67112 Germany",
                                        "contexts": {
                                            "private": True
                                        }
                                    }
                                },
                                "phones": {
                                    "voice": {
                                        "features": {
                                            "voice": True
                                        },
                                        "number": "+31.621263322"
                                    }
                                },
                                "emails": {
                                    "email": {
                                        "address": "joe.user@example.com"
                                    }
                                }
                            }
                    }
                }
        response = client.patch(f"/entities/{test_entity_id}", json=patch_payload, auth=get_credentials)
        assert response.status_code == 200

@pytest.mark.order(4)
def test_delete_entity(get_credentials, test_entity_id):
    with TestClient(app) as client:
        response = client.delete(f"/entities/{test_entity_id}", auth=get_credentials)
        assert response.status_code == 204