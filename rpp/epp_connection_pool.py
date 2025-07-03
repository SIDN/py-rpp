from typing import Dict
import threading
import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from rpp.epp_client import EppClient
from fastapi import Cookie, Depends, HTTPException, Response
from rpp.model.config import Config
import logging
from fastapi import Request, Cookie, Cookie, Response

logger = logging.getLogger('uvicorn.error')

security = HTTPBasic()

def get_connection(request: Request, response: Response,
                    session_id: str = Cookie(None),
                    credentials: HTTPBasicCredentials = Depends(security)):
    
    return request.app.state.pool.get_connection(response, session_id, credentials)

def invalidate_connection(request: Request):
    return request.app.state.pool.invalidate_connection


class ConnectionPool:
    def __init__(self, cfg: Config):
        self._connection_cache: Dict[str, EppClient] = {}
        self._lock = threading.Lock()
        self.cfg = cfg

    def invalidate_connection(self, response: Response, session_id: str = Cookie(None)):
        logger.debug(f"Invalidate EPP connection for session_id: {session_id}")
        with self._lock:
            return self._connection_cache.pop(session_id, None)

    def get_connection(self, response: Response, session_id: str = Cookie(None),
                       credentials: HTTPBasicCredentials = None) -> EppClient:
        if session_id is None:
            session_id = secrets.token_urlsafe(32)

        if credentials is None:
            logger.error("No credentials provided for EPP connection")
            raise HTTPException(status_code=401, detail="Unauthorized")

        with self._lock:
            if session_id not in self._connection_cache:
                logger.info(f"Creating new EPP connection for client: {credentials.username}")
                client = EppClient(self.cfg)
                client.login(self.cfg, credentials.username, credentials.password)
                response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
                self._connection_cache[session_id] = client

            conn = self._connection_cache[session_id]

            if not conn.logged_in:
                raise HTTPException(status_code=403, detail="Not logged in")

            return conn
        
    def close(self):
        with self._lock:
            for session_id, client in self._connection_cache.items():
                if client.logged_in:
                    client.logout()
            self._connection_cache.clear()
            logger.debug("All EPP connections closed and cache cleared.")   