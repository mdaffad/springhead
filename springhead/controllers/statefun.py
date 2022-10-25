import logging

from fastapi import APIRouter, Depends, Request, Response
from statefun import RequestReplyHandler

from .dependencies import get_handler

router = APIRouter()
logger = logging.getLogger(__name__)


# enable dynamic routing
@router.post("")
async def handle(request: Request, handler: RequestReplyHandler = Depends(get_handler)):
    req = await request.body()
    logger.info(req)
    res = await handler.handle_async(req)
    return Response(
        res,
        media_type="application/octet-stream",
    )
