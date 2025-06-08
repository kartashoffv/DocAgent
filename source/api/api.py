from fastapi import APIRouter
from source.api.endpoints import health, chats

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(chats.router)
