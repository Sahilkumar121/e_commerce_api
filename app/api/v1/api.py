from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, cart_item, order, product, transaction

route = APIRouter(prefix="/api")

route.include_router(admin.route)
route.include_router(auth.route)
route.include_router(product.route)
route.include_router(order.route)
route.include_router(transaction.route)
route.include_router(cart_item.route)
