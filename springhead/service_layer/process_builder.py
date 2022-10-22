from springhead.models import Process, ProcessType, Specification
from springhead.schemas import SPRINGHEAD_TF_IDF_VALUE_SPEC

from .handlers import bag_of_words, clustream, tf_idf, tokenize, transform, word2vec


class ProcessBuilder:
    """
    Inject Specification to Process
    """

    # TODO: refactor as one flat key-value ProcessType
    process_type_to_function_mapper = {
        ProcessType.BAG_OF_WORD: (bag_of_words, []),
        ProcessType.CLUSTERING: (clustream, []),
        ProcessType.FILTERING: (filter, []),
        ProcessType.NORMALIZATION: (),
        ProcessType.TF_IDF: (tf_idf, [SPRINGHEAD_TF_IDF_VALUE_SPEC]),
        ProcessType.TOKENIZATION: (tokenize, []),
        ProcessType.TRANSFORMATION: (transform, []),
        ProcessType.WORD2VEC: (word2vec, []),
    }

    @classmethod
    def build(cls, specification: Specification) -> Process:
        implemented_function, value_types = cls.process_type_to_function_mapper[
            specification.type_process
        ]
