from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# конфиги для запуска приложения
class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: str = 8000

class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"

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
        env_file = (".env.template", ".env"),
        case_sensitive = False,
        env_nested_delimiter="__",
        env_prefix = "APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig

settings = Settings()
