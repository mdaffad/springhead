import logging

from fastapi import APIRouter, Request, Response
from statefun import RequestReplyHandler, StatefulFunctions

from .greet import greeter
from .text import cluster, vectorize

router = APIRouter()
logger = logging.getLogger(__name__)

FUNCTIONS_MAPPER = {
    "springhead/greeter": (greeter,),
    "springhead/vectorize": (vectorize,),
    "springhead/cluster": (cluster,),
}


functions = StatefulFunctions()

for typename, function in FUNCTIONS_MAPPER.items():
    functions.register(typename, *function)


handler = RequestReplyHandler(FUNCTIONS_MAPPER)


@router.post("/")
async def handle(request: Request):
    request.receive
    req = await request.body()
    res = await handler.handle_async(req)
    return Response(
        res,
        media_type="application/octet-stream",
    )
