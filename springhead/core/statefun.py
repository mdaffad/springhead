from statefun import StatefulFunctions

from springhead.controllers import FUNCTIONS_MAPPER

functions = StatefulFunctions()

for typename, function in FUNCTIONS_MAPPER:
    functions.register(typename, *function)
