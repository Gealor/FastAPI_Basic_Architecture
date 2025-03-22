from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

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
    db_name: str

    echo : bool = False
    echo_pool:  bool = False
    pool_size: int = 50
    max_overflow: int = 10

    def get_db_url() -> PostgresDsn:
        url = f""

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig

settings = Settings()