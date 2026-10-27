from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Research Agent"
    app_env: Literal[
        "development", "production", "test"
    ] = "development"

    model_name: str = "qwen3.8-max"
    openai_api_key: SecretStr | None = None

    request_timeout: int = 30
    max_retries: int = 3
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@model_validator(mode="after")
def validate_settings(self):
    if self.request_timeout <= 0:
        raise ValueError("request_timeout must be greater than 0")
    if self.max_retries < 0:
        raise ValueError("max_retries must be greater than or equal to 0")

    if (
        self.app_env == "production"
        and not self.openai_api_key
    ):
        raise ValueError("openai_api_key must be provided in production")
    return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
