from logging import getLogger

logger = getLogger(__name__)


class Reader:
    def __init__(self) -> None:
        pass

    def read(self, path):
        pass

    def show_help(self, error=False) -> None:
        message = """
            error
        """
        if error:
            logger.error(message)
        else:
            logger.info(message)

    pass
