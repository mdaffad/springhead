from logging import getLogger
from time import time_ns

import requests
from fastapi import Request

from springhead.schemas import SpringheadTimeCreateRequest

logger = getLogger(__name__)


async def get_handler(request: Request):
    start_time = time_ns()
    handler = request.app.state.bootstrap.handler
    end_time = time_ns()
    bootstrap_object = request.app.state.bootstrap
    if bootstrap_object.benchmark_mode:
        elapsed_time = end_time - start_time
        requests.post(
            bootstrap_object.side_car_address,
            json=SpringheadTimeCreateRequest(
                time_ns=elapsed_time,
                type_test_case=bootstrap_object.type_test_case,
                type_timer="get_handler",
            ).dict(),
        )
        logger.info(f"elapsed springhead get_handler: {elapsed_time}")
    return handler
