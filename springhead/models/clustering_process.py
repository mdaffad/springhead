from .process import Process, ProcessType


class ClustreamProcess(Process):
    type_process: ProcessType = ProcessType.CLUSTREAM
