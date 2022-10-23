from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class FilteringProcess(Process):
    type_process: ProcessType = ProcessType.FILTERING
