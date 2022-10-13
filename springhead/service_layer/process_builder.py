from springhead.models import Process, ProcessType, VectorizationType

from .handlers import bag_of_words, tf_idf


class ProcessBuilder:
    process_type_to_function = {
        ProcessType.VECTORIZATION: {
            VectorizationType.BAG_OF_WORDS: bag_of_words,
            VectorizationType.TF_IDF: tf_idf,
        }
    }

    @classmethod
    def build(cls) -> Process:
        pass
