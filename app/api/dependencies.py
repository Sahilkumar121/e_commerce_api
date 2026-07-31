from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import UnauthorizedException
from app.core.security import decode_access_token
from app.db.database import SessionLocal
from app.models.users import Users
from app.schemas.user import CurrentUserResponse

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_db():
    async with SessionLocal() as session:
        yield session


db_Session = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(db: db_Session, token: str = Depends(oauth2_schema)):
    try:
        payload: dict = decode_access_token(token=token)

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedException()

        user_id = int(user_id_str)

    except JWTError, ValueError:
        raise UnauthorizedException()

    stmt = select(Users).where(Users.id == user_id)
    user_data = (await db.execute(stmt)).scalar_one_or_none()

    if not user_data:
        raise UnauthorizedException()

    current_user = CurrentUserResponse(
        id=user_data.id, email=user_data.email, role=user_data.role
    )
    return current_user


get_current_user_data = Annotated[CurrentUserResponse, Depends(get_current_user)]
