from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
ENV_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.template")

# конфиги для запуска приложения
class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: str = 8000

class ApiV1PrefixConfig(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"
    info: str = "/info"

class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1PrefixConfig = ApiV1PrefixConfig()

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
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig

settings = Settings()
