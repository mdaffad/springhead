import logging

from springhead.models import Model

logger = logging.getLogger(__name__)


class ModelLoader:
    @staticmethod
    def load_model(path: str):
        try:
            return Model(model_path=path)
        except Exception as e:
            logger.error(str(e))
