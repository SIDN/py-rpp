import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.params import Body, Header
from fastapi.security import HTTPBasic
from rpp.common import add_check_status, auth_info_from_header, update_response
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import get_connection
from rpp.model.rpp.common import BaseResponseModel

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()
router = APIRouter(dependencies=[Depends(security)])


@router.get("/{process_id}", response_model_exclude_none=True, summary="Get Organisation Info")
async def do_info(process_id: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_authorization: Annotated[str | None, Header()] = None,
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:

    logger.info(f"Info for Process: {process_id}")

