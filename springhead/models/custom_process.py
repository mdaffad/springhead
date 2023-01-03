from .process import Process, ProcessType


class CustomProcess(Process):
    type_process: ProcessType = ProcessType.CUSTOM
