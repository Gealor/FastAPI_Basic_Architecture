from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api import router as api_router
from core.config import settings
from core.models import db_helper, Base
 


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # async with db_helper.engine.begin() as conn:
    #     # чтобы все модели мигрировались нужно чтобы эти модели были известны(т.е. добавить в __init__ туда где лежит Base)
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    db_helper.dispose()

main_app = FastAPI(
    lifespan = lifespan
)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix
)

if __name__=="__main__":
    uvicorn.run("main:main_app", 
                host = settings.run.host, 
                port = settings.run.port, 
                reload=True,
                )