from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session, get_current_user_data
from app.models.cart_items import CartItems
from app.schemas.cart_item import CartItemCreate, CartItemResponse, CartItemUpdate

route = APIRouter(prefix="/cartitem", tags=["CartItem"])


# Get the cart item by using user id
@route.get("/", response_model=list[CartItemResponse])
async def get_cart_item_by_id(db: db_Session, current_user: get_current_user_data):

    stmt = select(CartItems).where(CartItems.user_id == current_user.id)
    cart_data = (await db.execute(stmt)).scalars().all()

    return cart_data


# Create new cart item
@route.post("/", response_model=CartItemResponse)
async def post_cart_item(
    cart_item_request: CartItemCreate,
    db: db_Session,
    current_user: get_current_user_data,
):

    # check if item is already in cart for the login user
    stmt = select(CartItems).where(
        CartItems.user_id == current_user.id,
        CartItems.product_id == cart_item_request.product_id,
    )

    existing_item = (await db.execute(stmt)).scalar_one_or_none()

    if existing_item:
        existing_item.quantity += cart_item_request.quantity
        await db.commit()
        return existing_item

    else:
        # if not then create new cart item
        new_cart_item = CartItems(
            user_id=current_user.id,
            product_id=cart_item_request.product_id,
            quantity=cart_item_request.quantity,
        )

        try:
            db.add(new_cart_item)
            await db.commit()
            await db.refresh(new_cart_item)
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"There is some error {e}",
            )

        return new_cart_item


# Update create item using cart id
@route.patch("/{cart_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_id: int,
    cart_update_request: CartItemUpdate,
    db: db_Session,
    current_user: get_current_user_data,
):

    # check if cart_id exist in database
    stmt = select(CartItems).where(
        CartItems.id == cart_id, CartItems.user_id == current_user.id
    )

    existing_cart_item = (await db.execute(stmt)).scalar_one_or_none()

    if not existing_cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found of id {cart_id}",
        )

    try:
        existing_cart_item.quantity = cart_update_request.quantity
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some error {e}",
        )

    return existing_cart_item


# Delete cart item using id
@route.delete("/{cart_id}", response_model=CartItemResponse)
async def delete_cart_item(
    cart_id: int, db: db_Session, current_user: get_current_user_data
):

    # check if the cart item exist or not
    stmt = select(CartItems).where(
        CartItems.id == cart_id, CartItems.user_id == current_user.id
    )

    existing_user = (await db.execute(stmt)).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for id {cart_id}",
        )

    try:
        await db.delete(existing_user)
        await db.refresh(existing_user)

    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some error {e}",
        )

    return existing_user
