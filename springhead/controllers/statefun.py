import logging
from time import time_ns

from fastapi import APIRouter, Depends, Request, Response
from statefun import RequestReplyHandler

from .dependencies import get_handler

router = APIRouter()
logger = logging.getLogger(__name__)


# enable dynamic routing
@router.post("")
async def handle(request: Request, handler: RequestReplyHandler = Depends(get_handler)):
    start_time = time_ns()
    req = await request.body()
    res = await handler.handle_async(req)
    response = Response(
        res,
        media_type="application/octet-stream",
    )
    end_time = time_ns()
    logger.info(f"elapsed statefun endpoint: {end_time-start_time}")
    return response
