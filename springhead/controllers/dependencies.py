from logging import getLogger

from fastapi import Request

logger = getLogger(__name__)


async def get_handler(request: Request):
    request.app.state.bootstrap.handler
