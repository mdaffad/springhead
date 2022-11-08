from pickle import load
from typing import Any, Optional

from pydantic import FilePath
from pydantic.dataclasses import dataclass


@dataclass
class Model:
    model_path: FilePath
    pickled_object: Optional[Any] = None

    def __post_init_post_parse__(self):
        if not self.pickled_object:
            with open(f"{self.model_path}", "rb") as model_file:
                self.pickled_object = load(model_file)
