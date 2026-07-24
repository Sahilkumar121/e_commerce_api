from app.core.exception import EmailAlreadyExistsException
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.core.security import get_hashed_password, verify_hashed_password
from app.models.users import Users
from app.schemas.user import UserRegisterRequest, UserRegisterResponse

route = APIRouter(prefix="/admin", tags=["Admin"])


@route.post("/register", status_code=status.HTTP_200_OK, response_model=UserRegisterResponse)
async def register_user(
    user_request: UserRegisterRequest, db: AsyncSession = Depends(get_db)
):
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

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"There is some error {e}")

    return user_register


@route.post("/login")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(Users).where(Users.email == form_data.username)
    user_result = await db.execute(stmt)
    user_exist = user_result.scalars().first()

    if not user_exist or not verify_hashed_password(form_data.password, user_exist.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed"
        )
