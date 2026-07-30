from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session, get_current_user_data
from app.models.order_items import OrderItem
from app.models.orders import Orders
from app.models.products import Products
from app.schemas.order import CreateOrderRequest

route = APIRouter(prefix="/order", tags=["Orders"])


@route.post("/")
async def crete_order(
    payload: CreateOrderRequest, db: db_Session, current_user: get_current_user_data
):

    current_user_id = current_user["id"]

    total_amount = 0.0
    order_items_list = []

    for item_data in payload.item:
        stmt = select(Products).where(Products.id == item_data.product_id)
        product = (await db.execute(stmt)).scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item_data.product_id} not found",
            )

        total_amount += float(product.price * item_data.quantity)

        if payload.discount_code in ["SUMMER50", "SUNDAY50"]:
            total_amount *= 0.5
        elif payload.discount_code in ["HAPPY20", "FIRST20"]:
            total_amount *= 0.2

        new_order_item = OrderItem(
            product_id=product.id, quantity=item_data.quantity, unit_price=product.price
        )
        order_items_list.append(new_order_item)

    new_order = Orders(
        user_id=current_user_id,
        total_amount=total_amount,
        status=payload.status,
        discount_code=payload.discount_code,
        items=order_items_list,
    )

    try:
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {e} ",
        )

    return new_order
