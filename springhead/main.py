import logging

from fastapi import FastAPI

from .controllers import main_router
from .core import Bootstrap, bootstrap, settings

app = FastAPI()

logger = logging.getLogger()


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
    """
    State()
    An object that can be used to store arbitrary state.
    Used for `request.state` and `app.state`.
    """
    init_logger(settings.log_level)

    logger = logging.getLogger(__name__)
    app.state.bootstrap: Bootstrap = await bootstrap()
    logger.info("Bootstrap is done")


app.include_router(main_router)
