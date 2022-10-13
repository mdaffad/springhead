from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, Callable, List, Optional

from pydantic import FilePath
from pydantic.dataclasses import dataclass
from statefun import (
    Context,
    Message,
    Type,
    ValueSpec,
    egress_message_builder,
    message_builder,
)

from springhead.schemas import SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE


@dataclass
class Process(ABCMeta):
    typename: str
    stateful_function: Callable[[Context, Message], None]
    source_type_value: Type
    target_type_value: Type
    model_path: Optional[FilePath] = None
    source_typename: Optional[str] = None
    target_typename: Optional[str] = None
    specs: List[ValueSpec] = []

    def send(self, target_id: str, value: Any, context: Context):
        if self.target_typename:
            context.send(
                message_builder(
                    target_typename=self.target_typename,
                    target_id=target_id,
                    value=value,
                    value_type=self.target_type_value,
                )
            )
        else:
            context.send_egress(
                egress_message_builder(
                    target_typename="io.statefun.playground/egress",
                    value=value,
                    value_type=SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE,
                )
            )

    @abstractmethod
    def inject_process_dependency(self):
        raise NotImplementedError

    @abstractmethod
    def wrapper_statefun(self):
        raise NotImplementedError


class ProcessType(Enum):
    VECTORIZATION = "vectorization"
    CLUSTERING = "clustering"
    TOKENIZATION = "tokenization"
    TRANSFORMATION = "transformation"
    NORMALIZATION = "normalization"
    FILTERING = "filtering"
    CUSTOM = "custom"

    @classmethod
    def option_to_type(cls, option: str):
        return cls(option)


@dataclass
class SpringheadProcess(Process, ABCMeta):
    _type_process: ProcessType
    func: Callable[[Context, Message, Process], None]

    def inject_process_dependency(self):
        return self

    def __post_init__(self):
        def wrapped_springhead_process(context: Context, message: Message):
            return self.func(context, message, self.inject_process_dependency())

        self.stateful_function = wrapped_springhead_process
