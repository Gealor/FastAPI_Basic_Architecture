import asyncio
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
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
    print("Завершение")
    await db_helper.dispose()

main_app = FastAPI(
    lifespan = lifespan,
    # dependencies=[Depends(something1), Depends(something2)] # внедрение зависимостей на уровне приложения(чтобы эти самые зависимости использовались на всех ручках)
    # полезно для зависимостей, с результатом которых нам не требуется работать далее, либо если зависимость ничего не возвращает
)

main_app.include_router(
    api_router,
)
 
# Можно подменить одну зависимость(ф-ию или класс, используемый в Depends) на другую зависимость, к примеру mock(тестовую)
# dependency_overrides - это глобальный словарь, который (согласно документации) используется для "тестирования зависимостей"
# однако dependency_overrides сильно похож на контейнер зависимостей (IoC контейнер)
# main_app.dependency_overrides[db_helper.session_getter] = mock_db_helper.session_getter

if __name__=="__main__":
    uvicorn.run("main:main_app", 
                host = settings.run.host, 
                port = settings.run.port, 
                reload=True,
                )