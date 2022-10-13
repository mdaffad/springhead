from springhead.models import ProcessType, VectorizationType

from .handlers import bag_of_words


class ProcessBuilder:
    process_type_to_function = {
        ProcessType.VECTORIZATION: {VectorizationType.BAG_OF_WORDS: bag_of_words}
    }

    @classmethod
    def build(cls):
        pass
