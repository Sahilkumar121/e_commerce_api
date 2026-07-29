from fastapi import APIRouter

from app.api.dependencies import db_Session
from app.schemas.order import CreateOrderRequest

route = APIRouter(prefix="/order", tags=["Orders", "Order_item"])


@route.post("/")
async def crete_order(payload: CreateOrderRequest, db: db_Session):
    pass
