from .process import Process, ProcessType


class FilteringProcess(Process):
    type_process: ProcessType = ProcessType.FILTERING
