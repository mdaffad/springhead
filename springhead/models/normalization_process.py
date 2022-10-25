from .process import Process, ProcessType


class NormalizationProcess(Process):
    type_process: ProcessType = ProcessType.NORMALIZATION
