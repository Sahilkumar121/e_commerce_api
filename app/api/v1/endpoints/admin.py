from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session, get_current_user_data
from app.models.users import Users
from app.schemas.user import UserResponse

route = APIRouter(prefix="/admin", tags=["Admin"])


@route.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_user(db: db_Session, current_user: get_current_user_data):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action")

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
