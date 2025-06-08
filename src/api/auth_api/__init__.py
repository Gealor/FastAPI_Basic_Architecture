from fastapi import APIRouter
from core.config import settings
from .basic_auth import router as auth_router
from .header_auth import router as header_auth_router
from .cookie_auth import router as cookie_auth_router
from .jwt_auth import router as jwt_auth_router

router = APIRouter(
    prefix = settings.api.auth.prefix,
    tags = ["Auth"],
)

router.include_router(
    auth_router,
    prefix = settings.api.auth.basic_auth,
)

router.include_router(
    header_auth_router,
    prefix = settings.api.auth.header_auth,
)

router.include_router(
    cookie_auth_router,
    prefix = settings.api.auth.cookie_auth,
)

router.include_router(
    jwt_auth_router,
    prefix=settings.api.auth.jwt_auth,
)
