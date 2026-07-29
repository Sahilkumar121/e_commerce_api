from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, order, product

route = APIRouter(prefix="/api")

route.include_router(admin.route)
route.include_router(auth.route)
route.include_router(product.route)
route.include_router(order.route)
