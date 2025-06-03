from pathlib import Path

import redis
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 0
    pool_size: int = 1
    pool_timeout: int = 30
    pool_recycle: int = -1

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig:
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
        extra="ignore"
    )
    db: DbSettings
    redis: RedisConfig = RedisConfig()


settings = Settings()

redis_client = redis.StrictRedis(
    host=settings.redis.REDIS_HOST,
    port=settings.redis.REDIS_PORT,
    db=settings.redis.REDIS_DB,
    decode_responses=True,
)

