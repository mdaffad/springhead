from dataclasses import field
from typing import List, Optional

from pydantic import FilePath
from pydantic.dataclasses import dataclass
from statefun import Type

from springhead.utils.dataclass_config import Config

from .process import ProcessType


@dataclass(config=Config)
class ValueSpecSchema:
    name: str
    _type: str


@dataclass(config=Config)
class Specification:
    typename: str
    type_process: ProcessType
    source_type_value: Type
    source_typename: Optional[str] = None
    target_type_value: Type = None
    target_typename: Optional[str] = None
    model_path: Optional[FilePath] = None
    value_specs: List[ValueSpecSchema] = field(default_factory=list)

    def __post_init__(self):
        pass
