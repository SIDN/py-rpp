import logging 
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from rpp import domains, entities, hosts, messages
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import ConnectionPool
from contextlib import asynccontextmanager
from rpp.epp_connection_pool import get_connection, invalidate_connection
from rpp.model.rpp.common_converter import to_greeting_model


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
    

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.__class__.__name__} did something. There goes a rainbow..."},
    )

app.include_router(entities.router, prefix="/entities", tags=["entities"])
app.include_router(domains.router, prefix="/domains", tags=["domains"])
app.include_router(hosts.router, prefix="/hosts", tags=["hosts"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])

@app.get("/")
def do_root(conn: EppClient = Depends(get_connection)):
    return to_greeting_model(conn.greeting)



@app.get("/logout")
def do_conn_logout(response: Response, conn: EppClient = Depends(invalidate_connection)):

    if conn is None:
        raise HTTPException(status_code=403, detail="No session cookie or connection found")
    
    response.delete_cookie(key="session_id")
    return conn.logout()

