from core.bootstrap import Bootstrap, bootstrap
from fastapi import FastAPI

app = FastAPI()

app.on_event("startup")


async def startup():
    """
    State()
    An object that can be used to store arbitrary state.
    Used for `request.state` and `app.state`.
    """
    app.state.bootstrap: Bootstrap = await bootstrap()
