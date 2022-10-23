from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class NormalizationProcess(Process):
    type_process: ProcessType = ProcessType.NORMALIZATION
