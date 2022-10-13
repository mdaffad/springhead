from pydantic.dataclasses import dataclass

from .process import ProcessType, SpringheadProcess


@dataclass
class TokenizationProcess(SpringheadProcess):
    _type_process: ProcessType = ProcessType.TOKENIZATION
