from logging import getLogger
from time import time_ns

from fastapi import Request

logger = getLogger(__name__)


async def get_handler(request: Request):
    start_time = time_ns()
    handler = request.app.state.bootstrap.handler
    end_time = time_ns()
    logger.info(f"elapsed get_handler: {end_time-start_time}")
    return handler
