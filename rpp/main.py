import logging
import pprint
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from rpp import domains, entities, hosts, messages, organisations
from rpp.common import EppException
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import ConnectionPool
from contextlib import asynccontextmanager
from rpp.epp_connection_pool import get_connection
from rpp.model.rpp.common import GreetingModel
from rpp.model.rpp.common_converter import to_base_response, to_greeting_model


logger = logging.getLogger('uvicorn.error')

cfg = Config()
logger.info(f'Using config:\n {pprint.pformat(cfg.model_dump())}')

async def create_connection_pool():
    return ConnectionPool(cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating EPP connection pool")
    app.state.pool = await create_connection_pool()
    yield

app = FastAPI(
    title="RPP ",
    description="Restful Provisioning Protocol - Modern Domain Registry API",
    version="0.0.1",
    lifespan=lifespan
)

@app.exception_handler(EppException)
async def epp_exception_handler(request: Request, exc: EppException):
    logger.error(f"EPPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=to_base_response(exc.epp_response).model_dump(exclude_none=True) if exc.epp_response else {"error": str(exc.detail)},
        headers=getattr(exc, "headers", None)
    )

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.__class__.__name__} did something. There goes a rainbow..."},
        headers=getattr(exc, "headers", None)
    )

@app.middleware("http")
async def cleanup_after_request(request: Request, call_next):
    logger.info("Before endpoint")
    response = await call_next(request)
    if response.status_code in (307, 308):
        # Skip cleanup for redirect responses
        # redirects may be caused by client not using / at the end of the URL
        return response
    state = getattr(request.app, "state", None)
    if (
        not cfg.rpp_epp_connection_cache
        and state is not None
        and hasattr(state, "session_id")
        and state.session_id
    ):
        logger.info(f"Cleaning up connection for session_id: {state.session_id}")
        # not keeping connection in cache, close the connection for this session
        if hasattr(state, "pool") and state.pool is not None:
            await state.pool.invalidate_connection(state.session_id)
    
    return response

app.include_router(entities.router, prefix="/entities", tags=["Entities"])
app.include_router(domains.router, prefix="/domains", tags=["Domains"])
app.include_router(hosts.router, prefix="/hosts", tags=["Hosts"])
app.include_router(organisations.router, prefix="/organisations", tags=["Organisations"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])

@app.get("/", tags=["Service"], response_model_exclude_none=True, summary="Service Discovery", description="Returns a description of features supported by the service.")
async def do_root(conn: EppClient = Depends(get_connection)) -> GreetingModel:
    return to_greeting_model(conn.greeting)
