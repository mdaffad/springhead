import logging

from fastapi import APIRouter, Request

router = APIRouter()
logger = logging.getLogger(__name__)


async def resolve_statefun(request: Request):
    pass


@router.get("/")
async def statefun_function():
    logger.info("test")
    return "Hello"
