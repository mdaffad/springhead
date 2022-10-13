from pydantic.dataclasses import dataclass

from .process import ProcessType, SpringheadProcess


@dataclass
class TransformationProcess(SpringheadProcess):
    _type_process: ProcessType = ProcessType.TRANSFORMATION
