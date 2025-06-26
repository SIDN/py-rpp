import logging
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from rpp import contacts
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create
from rpp.epp_connection_pool import ConnectionPool
from contextlib import asynccontextmanager
from rpp.epp_connection_pool import get_connection, invalidate_connection


logger = logging.getLogger('uvicorn.error')

cfg = Config()
print(f'Using config: {cfg}')

async def create_connection_pool():
    return ConnectionPool(cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    app.state.pool = await create_connection_pool()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])


# _connection_cache: Dict[str, EppClient] = {}
# _lock = threading.Lock()


# def invalidate_connection(response: Response, session_id: str = Cookie(None)):
#     logger.debug(f"Get EPP connection for session_id: {session_id}")

#     with _lock:
#         return _connection_cache.pop(session_id, None)
    
# def get_connection(response: Response, session_id: str = Cookie(None)):
#     if session_id is None:
#         session_id = secrets.token_urlsafe(32)

#     with _lock:
#         if session_id not in _connection_cache:
#             logger.debug(f"Creating new EPP connection for session_id: {session_id}")
#             client = EppClient(host=cfg.host, port=cfg.port, timeout=cfg.timeout)
            
#             client.login(cfg)
            
#             response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)

#             _connection_cache[session_id] = client
        
#         conn = _connection_cache[session_id]

#         if not conn.logged_in:
#             raise HTTPException(status_code=403, detail="Not logged in")

#         return conn

# def get_pool(request: Request):
#     return request.app.state.pool.get_connection

# def invalidate_pool(request: Request):
#     return request.app.state.pool.invalidate_connection

@app.get("/")
def do_root(conn: EppClient = Depends(get_connection)):
    return {f"found conn: {conn}"}

@app.get("/logout")
def do_conn_logout(response: Response, conn: EppClient = Depends(invalidate_connection)):

    if conn is None:
        raise HTTPException(status_code=403, detail="No session cookie or connection found")
    
    response.delete_cookie(key="session_id")
    return conn.logout()


@app.get("/domain/{domain_name}")
def do_domain_info(domain_name: str, conn: EppClient = Depends(get_connection)):
    logger.info(f"Fetching info for domain: {domain_name}")

    if not conn.logged_in:
        raise HTTPException(status_code=403, detail="Not logged in")

    epp_request = domain_info(domain=domain_name)
    return conn.send_command(epp_request)


# @app.post("/contacts/")
# def do_contact_create(conn: EppClient = Depends(get_connection)):
#     logger.info(f"Create new contact")

#     if not conn.logged_in:
#         raise HTTPException(status_code=403, detail="Not logged in")

#     epp_request = contact_create(
#         name="John Doe",
#         org="Example Org",
#         addr={
#             "street": "123 Example St",
#             "city": "Example City",
#             "sp": "Example State",
#             "pc": "12345",
#             "cc": "US"
#         },
#         email="test@test.nl",
#         phone="+31.612345678"
#     )
    
    
#     epp_response = conn.send_command(epp_request)
#     logger.info(f"Contact create response: {epp_response}")
#     return epp_response


# @app.post("/contacts2/")
# def do_contact_create(card: Card, conn: EppClient = Depends(get_connection)):
#     logger.info(f"Create new contact: {card.model_dump_json()}")

#     epp_request = contact_create(card)
#     epp_response = conn.send_command(epp_request)
 
#     logger.info(f"Contact create response: {epp_response}")
#     return epp_response