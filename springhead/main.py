from core.bootstrap import Bootstrap, bootstrap
from fastapi import FastAPI

app = FastAPI()

app.on_event("startup")


async def startup():
    app.state.bootstrap: Bootstrap = await bootstrap()
