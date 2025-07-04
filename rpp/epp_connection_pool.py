from typing import Dict
import threading
import secrets
from rpp.common import EppException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from rpp.epp_client import EppClient
from fastapi import Cookie, Depends, HTTPException, Response
from rpp.model.config import Config
import logging
from fastapi import Request, Cookie, Cookie, Response

from rpp.model.rpp.common_converter import is_ok_code

logger = logging.getLogger('uvicorn.error')

security = HTTPBasic()

def get_connection(request: Request, response: Response,
                    session_id: str = Cookie(None),
                    credentials: HTTPBasicCredentials = Depends(security)):
    
    return request.app.state.pool.get_connection(request, response, session_id, credentials)

def invalidate_connection(request: Request):
    return request.app.state.pool.invalidate_connection()

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
            except KeyError as e:
                return None
            
        
    # def remove_connection_from_cache(self, session_id: str) -> EppClient:
    #     with self._lock:
    #         return self._connection_cache[session_id]
    
    def __init__(self, cfg: Config):
        self._connection_cache: Dict[str, EppClient] = {}
        self._lock = threading.Lock()
        self.cfg = cfg

    def invalidate_connection(self, session_id: str = Cookie(None)):
        logger.debug(f"Invalidate EPP connection for session_id: {session_id}")
        with self._lock:
            conn = self._connection_cache.pop(session_id, None)
            if conn is not None:
                conn.logout()

    def get_connection(self, request: Request, response: Response, session_id: str = Cookie(None),
                       credentials: HTTPBasicCredentials = None,
                       ) -> EppClient:
        
        if session_id is None:
            if credentials is None:
                logger.error("No credentials provided for EPP connection")
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            session_id = secrets.token_urlsafe(32)

        conn: EppClient = self.get_connection_from_cache(session_id) if session_id else None
        if conn is None:
            logger.info(f"Creating new EPP connection for client: {credentials.username}")
            conn = EppClient(self.cfg)
            #epp_result = conn.login(self.cfg, credentials.username, credentials.password)
            #if is_ok_code(epp_result):
            #ok, msg = 
            if conn.login(self.cfg, credentials.username, credentials.password):
                #logger.info(f"Login successful for client: {credentials.username}")
                #if self.cfg.rpp_epp_connection_cache:
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

            
            #else:
                #logger.error(f"Login failed for client: {credentials.username}, error: {epp_result.response.result[0].msg.value}")
            #    raise EppException(status_code=403, epp_response=msg)

        # Check if the session_id exists in the cache
        #conn = get_connection_from_cache(session_id)

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