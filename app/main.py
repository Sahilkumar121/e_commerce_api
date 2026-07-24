from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1 import api
from app.db.database import engine, Base


@asynccontextmanager
async def lifespan(__app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    await engine.dispose()

app = FastAPI()

app.include_router(api.route)