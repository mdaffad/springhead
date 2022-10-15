from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class TransformationProcess(Process):
    type_process: ProcessType = ProcessType.TRANSFORMATION
