from typing import Dict
import threading
import secrets
from rpp.common import EppException, epp_to_rpp_code
from rpp.model.rpp.common_converter import get_status_from_response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from rpp.epp_client import EppClient
from fastapi import Cookie, Depends, Response
from rpp.model.config import Config
import logging
from fastapi import Request

import asyncio

logger = logging.getLogger('uvicorn.error')

security = HTTPBasic()

async def get_connection(request: Request, response: Response,
                    session_id: str = Cookie(None),
                    credentials: HTTPBasicCredentials = Depends(security)):
    return await request.app.state.pool.get_connection(request, response, session_id, credentials)

class ConnectionPool:
    """
    Manages a pool of EPP client connections, providing thread-safe caching, retrieval, and invalidation of connections
    based on session IDs. Handles authentication and session management for EPP clients, ensuring that connections are
    reused when possible and properly closed when no longer needed.
    Attributes:
        _connection_cache (Dict[str, EppClient]): Thread-safe cache mapping session IDs to EppClient instances.
        _lock (threading.Lock): Lock to ensure thread-safe access to the connection cache.
        cfg (Config): Configuration object used to initialize EppClient instances.
    Methods:
        __init__(cfg: Config):
            Initializes the connection pool with the given configuration.
        add_connection_to_cache(session_id: str, client: EppClient):
            Adds an EppClient instance to the cache for the specified session ID.
        get_connection_from_cache(session_id: str) -> EppClient:
            Retrieves an EppClient instance from the cache by session ID, or returns None if not found.
        invalidate_connection(response: Response, session_id: str = Cookie(None)):
            Removes and returns the EppClient associated with the given session ID from the cache.
        get_connection(response: Response, session_id: str = Cookie(None), credentials: HTTPBasicCredentials = None) -> EppClient:
            Retrieves an existing EppClient from the cache or creates a new one if not present.
            Handles authentication and sets a session cookie if a new connection is created.
        close():
            Logs out all active EppClient connections and clears the connection cache.
    """

    def add_connection_to_cache(self, session_id: str, client: EppClient):
        with self._lock:
            self._connection_cache[session_id] = client

    def get_connection_from_cache(self, session_id: str) -> EppClient:
        with self._lock:
            try:
                return self._connection_cache[session_id]
            except KeyError:
                return None
                
    def __init__(self, cfg: Config):
        self._connection_cache: Dict[str, EppClient] = {}
        self._lock = threading.Lock()
        self.cfg = cfg

    async def invalidate_connection(self, session_id: str):
        logger.debug(f"Invalidate EPP connection for session_id: {session_id}")
        with self._lock:
            conn = self._connection_cache.pop(session_id, None)
        if conn is not None:
            ok, epp_response, message = await conn.logout()
            if not ok:
                logger.error(f"Logout failed for session_id {session_id}: {message}")
                epp_status: int = get_status_from_response(epp_response)
                raise EppException(epp_to_rpp_code(epp_status), epp_response, {"Rpp-Epp-Code": str(epp_status)})

    async def get_connection(self, request: Request, response: Response, session_id: str = Cookie(None),
                       credentials: HTTPBasicCredentials = None,
                       ) -> EppClient:
        
        if session_id is None:
            if credentials is None:
                logger.error("No credentials provided for EPP connection")
                raise EppException(status_code=401, headers = {"Rpp-Epp-Code": "401"})
            
            session_id = secrets.token_urlsafe(32)

        conn: EppClient = self.get_connection_from_cache(session_id) if session_id else None
        if conn is None:
            logger.info(f"Creating new EPP connection for client: {credentials.username}")
            conn = EppClient(self.cfg)
            login_ok, epp_result, msg = await conn.login(self.cfg, credentials.username, credentials.password)
            if login_ok:
                # Store the connection in the cache
                logger.debug(f"Storing EPP connection in cache for session_id: {session_id}")
                self.add_connection_to_cache(session_id, conn)
                if not self.cfg.rpp_epp_connection_cache:
                    # keep session id in request state, so the connection can be removed after request
                    request.app.state.session_id = session_id
                else:
                    # connection not reused by client, do not set cookie
                    # connection will be closed after request
                    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)

            elif not conn.logged_in:
                epp_status: int = get_status_from_response(epp_result)
                raise EppException(epp_to_rpp_code(epp_status), epp_result, {"Rpp-Epp-Code": str(epp_status)})

        return conn
        
    async def close(self):
        with self._lock:
            clients = list(self._connection_cache.items())
            self._connection_cache.clear()
        # Logout all clients outside the lock
        for session_id, client in clients:
            if client.logged_in:
                await client.logout()
        logger.debug("All EPP connections closed and cache cleared.")