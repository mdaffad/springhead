from logging import getLogger

from pydantic.env_settings import BaseSettings

logger = getLogger(__name__)


class Settings(BaseSettings):
    model_path: str = ""
    config_path: str = ""
    module_path: str = ""


settings = Settings()


# class Reader:
#     def __init__(self) -> None:
#         pass

#     def read(self, path):
#         pass

#     def show_help(self, error=False) -> None:
#         message = """
#             error
#         """
#         if error:
#             logger.error(message)
#         else:
#             logger.info(message)

#     pass
