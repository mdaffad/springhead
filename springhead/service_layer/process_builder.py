from springhead.models import Process, ProcessType, VectorizationType
from springhead.schemas.text import SPRINGHEAD_TF_IDF_VALUE_SPEC

from .handlers import bag_of_words, tf_idf, tokenize


class ProcessBuilder:
    """
    Inject Specification to Process
    """

    process_type_to_function_mapper = {
        ProcessType.VECTORIZATION: {
            VectorizationType.BAG_OF_WORDS: (bag_of_words,),
            VectorizationType.TF_IDF: (tf_idf, [SPRINGHEAD_TF_IDF_VALUE_SPEC]),
        },
        ProcessType.TOKENIZATION: tokenize,
    }

    @classmethod
    def build(cls) -> Process:
        pass
