from enum import Enum

from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


class VectorizationType(Enum):
    BAG_OF_WORDS = "bag_of_words"
    TF_IDF = "tf_idf"
    WORD2VEC = "word2vec"

    @classmethod
    def option_to_type(cls, option: str):
        return cls(option)


@dataclass
class VectorizationProcess(Process):
    _type_process: ProcessType = ProcessType.VECTORIZATION
    vectorization_type: VectorizationType = VectorizationType.BAG_OF_WORDS
