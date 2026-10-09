from fastapi import APIRouter
from app.api.v1.endpoints import admin, store, health

api_router = APIRouter()
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(store.router, tags=["Customer"])
api_router.include_router(health.router, tags=["Health Check"])
