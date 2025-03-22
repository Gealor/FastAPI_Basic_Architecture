from pydantic import BaseModel
from pydantic_settings import BaseSettings

# конфиги для запуска приложения
class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: str = 8000

class ApiPrefixConfig(BaseModel):
    prefix: str = "/api"

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()

settings = Settings()