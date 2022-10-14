from enum import Enum


class CustomEnumType(Enum):
    @classmethod
    def option_to_type(cls, option: str):
        return cls(option)
