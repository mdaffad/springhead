from fastapi import APIRouter

from .config import router as config_router
from .statefun import router as statefun_router

main_router = APIRouter()

main_router.include_router(config_router, prefix="/config")
main_router.include_router(statefun_router, prefix="/statefun")
