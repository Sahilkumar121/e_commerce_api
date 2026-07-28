from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlalchemy import func, select

from app.api.dependencies import db_Session
from app.models.categories import Categories
from app.models.products import Products
from app.models.reviews import Review
from app.schemas.category import (
    CategoryFieldQuery,
)
from app.schemas.product import ProductFieldQuery

route = APIRouter(tags=["Products"])


# Query Parameters for categories

# Query:
# page
# limit
# name
# slug


@route.get("/categories", status_code=status.HTTP_200_OK)
async def get_categories(
    query_data: Annotated[CategoryFieldQuery, Query()], db: db_Session
):
    stmt = select(Categories)

    if query_data.name:
        stmt = stmt.where(Categories.name.ilike(f"%{query_data.name}%"))
    if query_data.slug:
        stmt = stmt.where(Categories.slug.ilike(f"%{query_data.slug}%"))

    stmt = stmt.offset(query_data.cal_start).limit(query_data.cal_end)

    data = (await db.execute(stmt)).scalars().all()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found matching the given criteria",
        )

    return {
        "page": query_data.page,
        "limit": query_data.limit,
        "data": data,
    }


# Get products by id
@route.get("/products/{product_id}")
async def get_product_by_id(
    db: db_Session,
    product_id: int = Path(..., gt=0),
):

    stmt = select(Products).where(Products.id == product_id)
    product_data = (await db.execute(stmt)).scalar_one_or_none()

    if not product_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Data Found In Database for {product_id}",
        )

    return product_data


# Query Parameters for products

# Query:
# page
# limit
# name
# price
# rating
# stock_quantity
# is_active


@route.get("/products")
async def get_products(
    query_data: Annotated[ProductFieldQuery, Query()], db: db_Session
):

    stmt = select(Products)

    if query_data.rating:
        stmt = (
            stmt.join(Review, Review.product_id == Products.id)
            .group_by(Products.id)
            .having(func.avg(Review.rating) >= query_data.rating)
        )

    if query_data.name:
        stmt = stmt.where(Products.name.ilike(f"%{query_data.name}%"))
    if query_data.price:
        stmt = stmt.where(Products.price >= query_data.price)
    if query_data.stock_quantity:
        stmt = stmt.where(Products.stock_quantity >= query_data.stock_quantity)
    if query_data.is_active is not None:
        stmt = stmt.where(Products.is_active == query_data.is_active)

    stmt = stmt.offset(query_data.cal_start).limit(query_data.cal_end)

    data = (await db.execute(stmt)).scalars().all()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found matching the given criteria",
        )

    return {"page": query_data.page, "limit": query_data.limit, "data": data}
