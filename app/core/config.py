from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_URL: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env")


setting = Setting()
