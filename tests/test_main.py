from fastapi import Cookie, Request, Response
from fastapi.security import HTTPBasicCredentials
import pytest
from fastapi.testclient import TestClient
from rpp import main, domains, entities, hosts, messages
import rpp.epp_connection_pool
from rpp.model.epp.epp_1_0 import GreetingType

def test_root_endpoint(monkeypatch):

    # class MockEppClient:
    #     def __init__(self):
    #         self.greeting = GreetingType(
    #         sv_id="dummy_svID",
    #         dcp=None,
    #         svc_menu=None
    #         )
    #         self.logged_in = True

    #     async def send_command(self, *args, **kwargs):
    #         return "dummy_epp_response"

    #     async def login(self, *args, **kwargs):
    #         return True, "dummy_epp_response", "login ok"

    #     async def logout(self, *args, **kwargs):
    #         return True, "dummy_epp_response", "logout ok"

    #     async def connect(self, *args, **kwargs) -> GreetingType:
            
    #         return self.greeting

    # def get_connection(request: Request = None, response: Response = None,
    #                 session_id: str = Cookie(None),
    #                 credentials: HTTPBasicCredentials = None):
    #     return MockEppClient()


    #main.app.dependency_overrides[rpp.epp_connection_pool.get_connection] = get_connection

    with TestClient(main.app) as client:
        response = client.get("/", auth=("903814", "A5sMb7762d\b4691"))
        assert response.status_code == 200
