from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class TransformationProcess(Process):
    _type_process: ProcessType = ProcessType.TRANSFORMATION
