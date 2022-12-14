# TODO: Abstract base class for testing and adapter-like for model
from statefun import Context


class AbstractContext:
    pass


class SpringheadContext(AbstractContext, Context):
    def __init__(self) -> None:
        super().__init__()
