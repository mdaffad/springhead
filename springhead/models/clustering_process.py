from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class ClustreamProcess(Process):
    type_process: ProcessType = ProcessType.CLUSTREAM
