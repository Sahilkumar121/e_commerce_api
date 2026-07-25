from fastapi import APIRouter

from app.api.v1.endpoints import admin

route = APIRouter(prefix="/api")

route.include_router(admin.route)
