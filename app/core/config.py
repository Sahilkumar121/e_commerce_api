from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_URL: str = Field(default=...)
    SECRET_KEY: str = Field(default=...)
    ACCESS_TOKEN_TIME_EXPIRE: int = Field(default=...)
    ALGORITHM: str = Field(default=...)
    MAIL_USERNAME: str = Field(default=...)
    MAIL_PASSWORD: SecretStr = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


setting = Setting()
