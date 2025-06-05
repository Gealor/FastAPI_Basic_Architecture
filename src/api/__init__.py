from fastapi import APIRouter

from .api_v1 import router as router_api_v1
from .auth_api import router as router_auth_api
from core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
) # основной роутер, к которому будут подключаться другие роутеры

router.include_router(
    router_api_v1,
)

router.include_router(
    router_auth_api,
)

