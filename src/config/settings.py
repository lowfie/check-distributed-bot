from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DSN: PostgresDsn | None = None

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DSN: RedisDsn | None = None

    @field_validator("POSTGRES_DSN")
    @classmethod
    def assemble_db_connection(cls, value: PostgresDsn | None, values: FieldValidationInfo) -> PostgresDsn:
        if isinstance(value, str):
            return value

        postgres_url = "{schema}://{user}:{password}@{host}:{port}/{db}".format(
            schema="postgresql+asyncpg",
            user=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            db=values.data.get("POSTGRES_DB")
        )
        return postgres_url

    @field_validator("REDIS_DSN")
    @classmethod
    def assemble_redis_connection(cls, value: RedisDsn | None, values: FieldValidationInfo) -> RedisDsn:
        if isinstance(value, str):
            return value

        redis_url = "{schema}://{host}:{port}/0".format(
            schema="redis",
            host=values.data.get("REDIS_HOST"),
            port=values.data.get("REDIS_PORT"),
            db=0
        )
        return redis_url
