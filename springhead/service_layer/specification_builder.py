from typing import List

import yaml
from pydantic import Field, FilePath
from pydantic.dataclasses import dataclass

from springhead.models import Specification
from springhead.utils.dataclass_config import Config


@dataclass(config=Config)
class SpecificationBuilder:
    # Build list of specifications from yml file
    file_path: FilePath
    specifications: List[Specification] = Field(default_factory=list)

    def __post_init__(self):
        pass

    def read_spec_file(self):
        return self._read_spec_file()

    def build_spec(self, obj):
        pass

    def _read_spec_file(self):
        with self.file_path.open("r") as stream:
            try:
                specifications_file = yaml.safe_load(stream)["specifications"]
            except yaml.YAMLError as exc:
                print(exc)
        for specification in specifications_file:  # type: ignore
            new_specification = Specification(**specification)
            self.specifications.append(new_specification)

        return self.specifications
