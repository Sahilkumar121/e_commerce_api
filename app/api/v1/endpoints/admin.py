from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.dependencies import db_Session
from app.core.exception import EmailAlreadyExistsException, UnauthorizedException
from app.core.security import (
    create_access_token,
    get_hashed_password,
    verify_hashed_password,
)
from app.models.users import Users
from app.schemas.user import UserRegisterRequest, UserRegisterResponse

route = APIRouter(prefix="/admin", tags=["Admin"])


@route.post(
    "/register", status_code=status.HTTP_200_OK, response_model=UserRegisterResponse
)
async def register_user(db: db_Session, user_request: UserRegisterRequest):
    email = user_request.email

    stmt = select(Users).where(Users.email == email)
    email_result = await db.execute(stmt)
    email_exist = email_result.scalar_one_or_none()

    if email_exist:
        raise EmailAlreadyExistsException(user_request.email)

    user_data = user_request.model_dump()

    hashed_password = get_hashed_password(user_data["password"])

    del user_data["password"]
    user_data["hashed_password"] = hashed_password
    user_register = Users(**user_data)

    try:
        db.add(user_register)
        await db.commit()
        await db.refresh(user_register)

    except SQLAlchemyError as e:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There is some error {e}",
        )

    return user_register


@route.post("/login")
async def login_access_token(db: db_Session, form_data: OAuth2PasswordRequestForm):
    stmt = select(Users).where(Users.email == form_data.username)
    user_result = await db.execute(stmt)
    user_exist = user_result.scalars().first()

    if not user_exist or not verify_hashed_password(
        form_data.password, user_exist.hashed_password
    ):
        raise UnauthorizedException()

    token = create_access_token(
        data={"sub": user_exist.id, "email": user_exist.email, "role": user_exist.role}
    )

    return {"access_token": token, "token_type": "bearer"}
