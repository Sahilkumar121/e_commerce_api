from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session, get_current_user_data
from app.models.cart_items import CartItems
from app.models.transaction import Transaction, TransactionItems

route = APIRouter(prefix="/transaction", tags=["Transaction"])


@route.post("/checkout")
async def checkout_cart(db: db_Session, current_user: get_current_user_data):

    stmt = select(CartItems).where(CartItems.user_id == current_user.id)
    cart_items = (await db.execute(stmt)).scalars().all()

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Your cart is empty"
        )

    try:
        new_transaction = Transaction(user_id=current_user.id, status="COMPLETED")

        db.add(new_transaction)
        await db.flush()

        for item in cart_items:
            new_transaction_item = TransactionItems(
                transaction_id=new_transaction.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )

            db.add(new_transaction_item)

            await db.delete(item)

        await db.commit()
        await db.refresh(new_transaction)

        return {
            "message": "Transaction Successful",
            "transaction_id": new_transaction.id,
        }
    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some errro {e!s}",
        )
