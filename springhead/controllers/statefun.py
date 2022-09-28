import logging

from fastapi import APIRouter, Request, Response
from statefun import RequestReplyHandler, StatefulFunctions

from .greet import greeter
from .text import cluster, vectorize

router = APIRouter()
logger = logging.getLogger(__name__)

# enable dynamic routing
FUNCTIONS_MAPPER = {
    "springhead/greeter": (greeter,),
    "springhead/vectorize": (vectorize,),
    "springhead/cluster": (cluster,),
}


functions = StatefulFunctions()

for typename, function in FUNCTIONS_MAPPER.items():
    functions.register(typename, *function)


handler = RequestReplyHandler(functions)


@router.post("")
async def handle(request: Request):
    req = await request.body()
    logger.info(req)
    res = await handler.handle_async(req)
    return Response(
        res,
        media_type="application/octet-stream",
    )
