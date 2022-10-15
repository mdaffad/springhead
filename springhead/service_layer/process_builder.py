from springhead.models import Process, ProcessType, VectorizationType

from .handlers import bag_of_words, tf_idf, tokenize


class ProcessBuilder:
    """
    Inject Specification to Process
    """

    process_type_to_function_mapper = {
        ProcessType.VECTORIZATION: {
            VectorizationType.BAG_OF_WORDS: bag_of_words,
            VectorizationType.TF_IDF: tf_idf,
        },
        ProcessType.TOKENIZATION: tokenize,
    }

    @classmethod
    def build(cls) -> Process:
        pass
