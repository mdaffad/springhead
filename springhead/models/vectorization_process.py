from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class BagOfWordProcess(Process):
    type_process: ProcessType = ProcessType.BAG_OF_WORD


@dataclass
class TFIDFProcess(Process):
    type_process: ProcessType = ProcessType.TF_IDF


@dataclass
class Word2VecProcess(Process):
    type_process: ProcessType = ProcessType.WORD2VEC
