from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TypeDefinition:
    type_def: str
    default: Optional[Any] = None


class DynamicRecord:
    def __init__(self, attributes: Dict[str, TypeDefinition] = {}) -> None:
        self.attributes = attributes

    def validate_json(self, json_data: Dict[str, Any]):
        for attribute in self.attributes:
            print(attribute)
            if (
                attribute not in json_data
                and type(self.attributes[attribute]["default"]).__name__
                != self.attributes[attribute]["type_def"]
            ):
                return False
            elif attribute in json_data:
                if (
                    self.attributes[attribute]["type_def"]
                    != type(json_data[attribute]).__name__  # noqa
                ):
                    return False
            elif attribute not in json_data:
                json_data[attribute] = self.attributes[attribute]["default"]
        return json_data
