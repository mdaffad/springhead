from __future__ import annotations

from .process import Process, ProcessType


class BagOfWordProcess(Process):
    type_process: ProcessType = ProcessType.BAG_OF_WORD


class TFIDFProcess(Process):
    type_process: ProcessType = ProcessType.TFIDF
