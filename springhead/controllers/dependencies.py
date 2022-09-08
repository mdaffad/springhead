from logging import getLogger
from typing import Any

from fastapi import Request

from springhead.core.bootstrap import Bootstrap

logger = getLogger(__name__)


async def get_text_model(request: Request) -> Any:
    try:
        bootstrap: Bootstrap = request.app.state.bootstrap
    except Exception as e:
        logger.error(str(e))
        raise Exception("Cannot load bootstrap state on request context")
    return bootstrap.text_model
