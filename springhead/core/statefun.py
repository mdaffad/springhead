import logging

from statefun import StatefulFunctions

from springhead.controllers import FUNCTIONS_MAPPER

logger = logging.getLogger(__name__)

functions = StatefulFunctions()
logger.info("test")
for typename, function in FUNCTIONS_MAPPER.items():
    functions.register(typename, *function)
