from fastapi import APIRouter

from .statefun import router as statefun_router

main_router = APIRouter()

main_router.include_router(statefun_router, prefix="/statefun")
