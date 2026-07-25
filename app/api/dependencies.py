from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import CredentialException
from app.core.security import decode_access_token
from app.db.database import SessionLocal

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/admin/login")


async def get_db():
    async with SessionLocal() as session:
        yield session


db_Session = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(db: db_Session, token: str = Depends(oauth2_schema)):
    try:
        payload: dict = decode_access_token(token=token)

        user_id: str | None = payload.get("sub")

        if not user_id:
            return CredentialException

    except JWTError:
        return CredentialException
