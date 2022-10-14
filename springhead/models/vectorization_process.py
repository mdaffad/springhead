from pydantic.dataclasses import dataclass

from springhead.utils import CustomEnumType

from .process import Process, ProcessType


class VectorizationType(CustomEnumType):
    BAG_OF_WORDS = "bag_of_words"
    TF_IDF = "tf_idf"
    WORD2VEC = "word2vec"


@dataclass
class VectorizationProcess(Process):
    _type_process: ProcessType = ProcessType.VECTORIZATION
    vectorization_type: VectorizationType = VectorizationType.BAG_OF_WORDS
