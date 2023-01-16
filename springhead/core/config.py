from logging import getLogger

from pydantic import validator
from pydantic.env_settings import BaseSettings

logger = getLogger(__name__)


class Settings(BaseSettings):
    log_level: str = "DEBUG"

    @validator("log_level")
    def validate_log_level(cls, level: str):
        return level.upper()


settings = Settings()
