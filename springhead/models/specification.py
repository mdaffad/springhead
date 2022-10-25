from dataclasses import asdict
from typing import List, Optional

from pydantic import DirectoryPath, FilePath
from pydantic.dataclasses import dataclass
from statefun import Type, make_json_type
from statefun.wrapper_types import PY_TYPE_TO_WRAPPER_TYPE

from springhead.utils.dataclass_config import Config
from springhead.utils.type_helper import get_type

from .process import ProcessType


@dataclass(config=Config)
class DictTypeSchema:
    typename: str


@dataclass(config=Config)
class Specification:
    typename: str
    type_process: ProcessType

    source_type_value: Type
    source_type_value_name_dictionary: Optional[str] = None
    source_typename: Optional[str] = None

    target_type_value: Type = None
    target_type_value_name_dictionary: Optional[str] = None
    target_typename: Optional[str] = None

    model_path: Optional[FilePath] = None

    def __post_init__(self):
        if isinstance(self.type_process, str):
            self.type_process = ProcessType.option_to_type(self.type_process)

        if isinstance(self.source_type_value, str):
            self.source_type_value = self.option_to_type(
                self.source_type_value,
                self.source_type_value_name_dictionary,
            )

        if isinstance(self.target_type_value, str):
            self.target_type_value = self.option_to_type(
                self.target_type_value,
                self.target_type_value_name_dictionary,
            )
        print(self.target_type_value)
        print(self.target_typename)

        if not (self.target_type_value and self.target_typename) and (
            self.target_type_value or self.target_typename
        ):
            """
            self.target_type_value == None and self.target_typename == Some
            self.target_type_value == Some and self.target_typename == None
            """
            raise ValueError(
                "target type value and target typename must be configured together"
            )

    def option_to_type(self, _type: str, dictionary_name: str):
        _type = get_type(self.source_type_value)
        if _type == dict and dictionary_name:
            return make_json_type(dictionary_name)
        elif (_type == dict and not dictionary_name) or (
            _type != dict and dictionary_name
        ):
            """
            _type == dict and dictiory_name == None
            _type != dict and dictiory_name == Some
            """
            print(_type)
            print(dictionary_name)
            raise ValueError(
                "dictionary must be \
                followed with source_type_value_name_dictionary"
            )
        else:
            _type = PY_TYPE_TO_WRAPPER_TYPE.get(_type, None)
            print(_type)
            if _type:
                return _type
            else:
                raise ValueError("source value type is invalid")

    def asdict(self):
        return asdict(self)


class Specifications:
    specifications: List[Specification]
    model_directory: Optional[DirectoryPath]
