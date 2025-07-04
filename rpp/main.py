import logging
from typing import Annotated 
from fastapi import FastAPI, Depends, HTTPException, Header, Response, Request
from fastapi.responses import JSONResponse
from rpp import domains, entities, hosts, messages
from rpp.common import EppException
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import ConnectionPool
from contextlib import asynccontextmanager
from rpp.epp_connection_pool import get_connection, invalidate_connection
from rpp.model.rpp.common_converter import to_base_response, to_greeting_model


logger = logging.getLogger('uvicorn.error')

cfg = Config()
logger.info(f'Using config: {cfg}')

async def create_connection_pool():
    return ConnectionPool(cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating EPP connection pool")
    app.state.pool = await create_connection_pool()
    yield

# def store_credentials(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
#     request.state.credentials = credentials    

app = FastAPI(
    lifespan=lifespan
)

@app.exception_handler(EppException)
async def epp_exception_handler(request: Request, exc: EppException):
    logger.error(f"EPPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=to_base_response(exc.epp_response).model_dump(exclude_none=True),
        
    )

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.__class__.__name__} did something. There goes a rainbow..."},
    )

@app.middleware("http")
async def cleanup_after_request(request: Request, call_next):
    logger.info("Before endpoint")
    response = await call_next(request)
    if response.status_code in (307, 308):
        # Skip cleanup for redirect responses
        # redirects may be caused by client not using / at the end of the URL
        return response
    #session_id = request.cookies.get("session_id") or request.headers.get("session_id")
    if not cfg.rpp_epp_connection_cache and hasattr(request.app.state, "session_id") and request.app.state.session_id:
        logger.info(f"Cleaning up connection for session_id: {request.app.state.session_id}")
        # not keeping connection in cache, close the connection for this session
        request.app.state.pool.invalidate_connection(request.app.state.session_id)
    
    #TODO: add headers to response here?
    return response

app.include_router(entities.router, prefix="/entities", tags=["entities"])
app.include_router(domains.router, prefix="/domains", tags=["domains"])
app.include_router(hosts.router, prefix="/hosts", tags=["hosts"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

@app.get("/")
def do_root(conn: EppClient = Depends(get_connection)):
    return to_greeting_model(conn.greeting)


@app.get("/logout")
def do_conn_logout(response: Response, 
                   rpp_cl_trid: Annotated[str | None, Header()] = None,
                   conn: EppClient = Depends(invalidate_connection)):

    if conn is None:
        raise HTTPException(status_code=403, detail="No session cookie or connection found")
    
    response.delete_cookie(key="session_id")
    return conn.logout()



