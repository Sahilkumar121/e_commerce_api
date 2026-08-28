from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_TIME_EXPIRE: int
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


setting = Setting()  # type: ignore
