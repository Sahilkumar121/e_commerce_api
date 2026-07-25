from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session
from app.models.categories import Categories
from app.models.products import Products
from app.schemas.category import CategoryCreate, CategoryFieldQuery, CategoryResponse

route = APIRouter(tags=["Products"])


@route.post(
    "/categories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse
)
async def create_categories(payload: CategoryCreate, db: db_Session):

    new_category = Categories(name=payload.name, slug=payload.slug)

    try:
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some error {e}",
        )

    return new_category


@route.get(
    "/categories", status_code=status.HTTP_200_OK, response_model=list[CategoryResponse]
)
async def get_categories(
    query_data: Annotated[CategoryFieldQuery, Query()], db: db_Session
):
    stmt = select(Categories)

    if query_data.name and query_data.slug:
        stmt = select(Categories).where(
            Categories.name == query_data.name, Categories.slug == query_data.slug
        )
        data = (await db.execute(stmt)).scalars().all()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No Data Found for name {query_data.name}, slug {query_data.slug}",
            )

    elif query_data.name:
        stmt = select(Categories).where(Categories.name == query_data.name)
        data = (await db.execute(stmt)).scalars().all()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No Data Found for name {query_data.name}",
            )

    elif query_data.slug:
        stmt = select(Categories).where(Categories.slug == query_data.slug)
        data = (await db.execute(stmt)).scalars().all()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No Data Found for slug {query_data.slug}",
            )
    else:
        data = (await db.execute(stmt)).scalars().all()

    return data[: query_data.limit]


@route.get("/products/{product_id}")
async def get_product_by_id(
    db: db_Session,
    product_id: int = Path(..., gt=0),
):

    stmt = select(Products).where(Products.id == product_id)
    product_data = (await db.execute(stmt)).scalar_one_or_none()

    if not product_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No Data Found In Database for {product_id}",
        )

    return product_data
