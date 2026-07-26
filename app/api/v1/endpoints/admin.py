from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session, get_current_user_data
from app.core.exception import ForbiddenException
from app.models.users import Users
from app.schemas.user import UserResponse

route = APIRouter(prefix="/admin", tags=["Admin"])


# Get All User
@route.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_user(db: db_Session, current_user: get_current_user_data):

    if current_user["role"] != "admin":
        raise ForbiddenException()

    try:
        stmt = select(Users)
        user_data = (await db.execute(stmt)).scalars().all()

    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some error {e}",
        )

    return user_data


# Get User By Id
@route.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: Annotated[int, Path(gt=0)],
    db: db_Session,
    current_user: get_current_user_data,
):

    if current_user["role"] != "admin":
        raise ForbiddenException()

    try:
        stmt = select(Users).where(Users.id == user_id)
        user_data = (await db.execute(stmt)).scalar_one_or_none()

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Data not found",
            )
    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ther is error {e}",
        )

    return user_data
