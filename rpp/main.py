import logging
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from rpp import contacts, domains, hosts
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create
from rpp.epp_connection_pool import ConnectionPool
from contextlib import asynccontextmanager
from rpp.epp_connection_pool import get_connection, invalidate_connection


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

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(domains.router, prefix="/domains", tags=["domains"])
app.include_router(hosts.router, prefix="/hosts", tags=["hosts"])

@app.get("/")
def do_root(conn: EppClient = Depends(get_connection)):
    return {f"found conn: {conn}"}

@app.get("/logout")
def do_conn_logout(response: Response, conn: EppClient = Depends(invalidate_connection)):

    if conn is None:
        raise HTTPException(status_code=403, detail="No session cookie or connection found")
    
    response.delete_cookie(key="session_id")
    return conn.logout()



