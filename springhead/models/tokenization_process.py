from .process import Process, ProcessType


class TokenizationProcess(Process):
    type_process: ProcessType = ProcessType.TOKENIZATION
