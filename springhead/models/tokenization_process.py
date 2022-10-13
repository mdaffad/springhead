from pydantic.dataclasses import dataclass

from .process import Process, ProcessType


@dataclass
class TokenizationProcess(Process):
    _type_process: ProcessType = ProcessType.TOKENIZATION
