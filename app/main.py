import logging

from fastapi import FastAPI

from springhead.controllers import main_router
from springhead.core import Bootstrap, bootstrap, settings

from .dummy import custom_process_logger

logger = logging.getLogger()

app = FastAPI()
app.include_router(main_router)


def init_logger(level):
    logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)s %(pathname)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@app.on_event("startup")
async def startup():
    init_logger(settings.log_level)

    logger = logging.getLogger(__name__)
    app.state.bootstrap: Bootstrap = await bootstrap(
        specification_path="./app/specifications.yml",
        custom_functions={"springhead/dummy": custom_process_logger},
    )  # type: ignore
    logger.info("Bootstrap is done")
