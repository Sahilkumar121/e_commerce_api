from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_URL: str = Field(default=...)
    SECRETE_KEY: str = Field(default=...)
    ACCESS_TOKEN_TIME_EXPIRE: int = Field(default=...)
    ALGORITHM: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env")


setting = Setting()
