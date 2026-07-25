import stat
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status

from app.api.v1 import api
from app.db.database import engine, Base

from app.core.exception import (
    EmailAlreadyExistsException,
    UnauthorizedException
)


@asynccontextmanager
async def lifespan(__app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(EmailAlreadyExistsException)
async def email_exists_handler(_request: Request, _exc: EmailAlreadyExistsException):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=_exc.message)

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception(_request: Request, _exc: UnauthorizedException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=_exc.message)

app.include_router(api.route)


@app.get("/")
async def home_page():
    return {"message": "E-Commerce API"}
