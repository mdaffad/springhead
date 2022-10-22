from __future__ import annotations

from abc import ABCMeta
from dataclasses import field
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
from springhead.utils import Config, CustomEnumType


class ProcessType(CustomEnumType):
    BAG_OF_WORD = "bag_of_word"
    CLUSTERING = "clustering"
    CUSTOM = "custom"
    FILTERING = "filtering"
    NORMALIZATION = "normalization"
    TF_IDF = "tf_idf"
    TOKENIZATION = "tokenization"
    TRANSFORMATION = "transformation"
    WORD2VEC = "word2vec"


@dataclass(config=Config)
class Process(ABCMeta):
    typename: str
    func: Callable[[Context, Message, Process], None]
    source_type_value: Type
    source_typename: Optional[str] = None
    target_type_value: Type = None
    target_typename: Optional[str] = None
    target_id: str = "v1"
    type_process: ProcessType = ProcessType.CUSTOM
    model_path: Optional[FilePath] = None
    value_specs: List[ValueSpec] = field(default_factory=list)

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

    def inject_process_dependency(self):
        return self

    def __post_init__(self):
        def wrapped_springhead_process(context: Context, message: Message):
            return self.func(context, message, self.inject_process_dependency())

        self.stateful_function = wrapped_springhead_process
