import asyncio
from contextlib import asynccontextmanager
import logging
import time
from typing import Awaitable, Callable
from fastapi import Depends, FastAPI, Request, Response
import uvicorn

from api import router as api_router
from core.config import settings
from core.models import db_helper, Base
from middlewares import LogNewRequirements, ProcessTimeHeaderMiddleware
 

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


# ---------------------------------------------------------------------------------------------------------
log = logging.getLogger(__name__)
@main_app.middleware("http") # middleware нужен для обработки запроса перед его отправкой обратно к клиенту
# все функции middleware принимают request, т.е. исходящий запрос от пользователя и call_next - функцию
# middleware ВСЕГДА ДОЛЖЕН ВОЗВРАЩАТЬ ЗНАЧЕНИЕ, ВНЕ ЗАВИСИМОСТИ ОТ ТОГО БЫЛО ЛИ ИСКЛЮЧЕНИЕ ИЛИ НЕТ.
async def log_new_requirements(
    request : Request,
    call_next : Callable[[Request], Awaitable[Response]] 
) -> Response:
    log.info(
        "Request %s to %s",
        request.method,
        request.url.path,
    )
    return await call_next(request) # await call_next(request) - это мы получаем ответ(response) вызыванной ручки

async def add_process_time_to_requests(
    request : Request,
    call_next : Callable[[Request], Awaitable[Response]],
):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    response.headers["X-Process-Time"] = f"{(end_time-start_time):.5f}" # можно добавлять заголовки к существующему ответу и уже после этого отправлять клиенту
    return response
# второй вариант вызова middleware - это если знать как устроены декораторы(а main_app.middleware("http") и есть декоратор)
main_app.middleware("http")(add_process_time_to_requests)
# -------------------------------------------------------------------------------------------------------------------
# либо можно добавлять middleware вот так
main_app.add_middleware(
    ProcessTimeHeaderMiddleware,
)
main_app.add_middleware(
    LogNewRequirements,
    logger_ = log, 
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