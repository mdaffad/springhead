from .process import Process, ProcessType


class TransformationProcess(Process):
    type_process: ProcessType = ProcessType.TRANSFORMATION
