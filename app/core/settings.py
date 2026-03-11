from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DbSettings(BaseModel):
    dsn: str = "postgresql://postgres:postgres@localhost:5432/promt_hub"
    pool_min_size: int = 2
    pool_max_size: int = 10
    connect_timeout: float = 10.0
    command_timeout: float = 30.0


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "Prompt Hub"
    debug: bool = False
    api: ApiSettings = Field(default_factory=ApiSettings)
    db: DbSettings = Field(default_factory=DbSettings)
