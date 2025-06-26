import logging
from fastapi import APIRouter, Depends, Request, Cookie, Cookie, Response
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient

from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create
from rpp.model.rpp.contact import Card

logger = logging.getLogger('uvicorn.error')
from fastapi import APIRouter

router = APIRouter()


# cfg = Config()

# print(f'Using config: {cfg}')

# connection_pool = ConnectionPool(cfg)

# def invalidate_connection(response: Response, session_id: str = Cookie(None)):
#     return connection_pool.invalidate_connection(response, session_id)

# def get_connection(response: Response, session_id: str = Cookie(None)):
#     return connection_pool.get_connection(response, session_id)


# @app.post("/contacts/")
# def do_contact_create(conn: EppClient = Depends(connection_pool.get_connection)):
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



@router.post("/")
def do_contact_create(request: Request, card: Card, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new contact: {card.model_dump_json()}")

    epp_request = contact_create(card)
    epp_response = conn.send_command(epp_request)
 
    logger.info(f"Contact create response: {epp_response}")
    return epp_response