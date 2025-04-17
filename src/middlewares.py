from logging import Logger
import time
from typing import Awaitable, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# самописные middleware в виде классов
class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next : Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()
        response.headers["X-Process-Time-Class"] = f"{(end_time-start_time):.5f}" # можно добавлять заголовки к существующему ответу и уже после этого отправлять клиенту
        return response
    
class LogNewRequirements(BaseHTTPMiddleware):
    def __init__(self, *args, logger_ : Logger, **kwargs): # Нельзя просто переопределить метода __init__, для этого надо также прокинуть все аргументы *args и **kwargs и вызвать super().__init__(...)
        super().__init__(*args, **kwargs)
        self.log = logger_

    async def dispatch(
            self,
            request: Request,
            call_next : Callable[[Request], Awaitable[Response]]
    ) -> Response:
        self.log.info(
            "New Request %s to %s",
            request.method,
            request.url.path,
        )
        return await call_next(request) 