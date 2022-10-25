import logging

from fastapi import FastAPI

from springhead.controllers import main_router
from springhead.core import Bootstrap, bootstrap, settings
from springhead.service_layer.specification_builder import SpecificationBuilder

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
    app.state.bootstrap: Bootstrap = await bootstrap()
    specification_builder = SpecificationBuilder("./app/specifications.yml")
    logger.info(specification_builder.read_spec_file())
    logger.info("Bootstrap is done")
