import logging
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_DIR = Path(__file__).parent.parent

ENV_PATH = BASE_DIR / ".env"
ENV_TEMPLATE_PATH = BASE_DIR / ".env.template"
# ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# ENV_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.template")

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# конфиги для запуска приложения
class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: str = 8000

class LoggingConfig(BaseModel):
    log_level: Literal[
        'CRITICAL',
        'FATAL',
        'ERROR',
        'WARN',
        'WARNING',
        'INFO',
        'DEBUG',
        'NOTSET'
    ] = 'INFO'

    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level]

class AuthApiPrefixConfig(BaseModel):
    prefix: str = '/auth'
    basic_auth: str = '/basic-auth'
    header_auth: str = '/header-auth'
    cookie_auth: str = '/cookie-auth'
    jwt_auth: str = '/jwt-auth'

class ApiV1PrefixConfig(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    info: str = "/info"

class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1PrefixConfig = ApiV1PrefixConfig()
    auth: AuthApiPrefixConfig = AuthApiPrefixConfig()

class AuthJWTConfig(BaseModel):
    private_key_path : Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path : Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm : str = "RS256"
    access_token_expire_minutes : int = 3

class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    name: str

    echo : bool
    echo_pool:  bool 
    pool_size: int
    max_overflow: int

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = (ENV_TEMPLATE_PATH, ENV_PATH),
        case_sensitive = False,
        env_nested_delimiter="__",
        env_prefix = "APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    log: LoggingConfig = LoggingConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig # берем данные из .env файлов, поэтому и не инициируем начальным значением(объектом)
    jwt : AuthJWTConfig = AuthJWTConfig()
    

settings = Settings()

# print(logging.getLevelNamesMapping()) # Посмотреть какие уровни логирование есть и какие значения им соответствуют