from dataclasses import field
from typing import Any, Dict, List

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from springhead.models import Specification
from springhead.utils.dataclass_config import Config


@dataclass(config=Config)
class SpecificationReader:
    file_path: FilePath
    specifications: List[Specification] = field(default_factory=list)

    def __post_init__(self):
        pass

    def is_spec_file_valid(self, yml_dict: Dict[str, Any]) -> bool:
        return True

    def _read_yml_file(self, path):
        pass

    def read_spec_file(self, path):
        return self._read_spec_file(path)

    def _read_spec_file(self, path):
        yml_config = self._read_yml_file(path)

        if not self.is_spec_file_valid(yml_config):
            raise Exception("error")

        self.specification = yml_config
