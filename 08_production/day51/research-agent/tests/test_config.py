import pytest
from pydantic import SecretStr, ValidationError

from app.core.config import Settings


def test_default_config():
    settings = Settings(_env_file=".env")

    assert settings.app_env == "development"
    assert settings.model_name == "qwen3.8-max"
    assert settings.max_retries == 3


def test_secret_is_masked():
    settings = Settings(
        _env_file=None,
        openai_api_key="test-secret"
    )
    assert settings.openai_api_key is not None
    assert "test-secret" not in repr(
        settings.openai_api_key
    )


def test_invalid_timeout():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            request_timeout=0,
        )


def test_production_requires_api_key():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            app_env="production",
            openai_api_key=None,
        )
