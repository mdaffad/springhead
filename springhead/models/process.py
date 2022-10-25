from __future__ import annotations

from typing import Any, Callable, List, Optional

from pydantic import Field, FilePath
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
    CLUSTREAM = "clustream"
    CUSTOM = "custom"
    FILTERING = "filtering"
    NORMALIZATION = "normalization"
    TFIDF = "tfidf"
    TOKENIZATION = "tokenization"
    TRANSFORMATION = "transformation"
    WORD2VEC = "word2vec"


@dataclass(config=Config)
class Process:
    typename: str
    function_handler: Callable[[Context, Message, Process], None]
    source_type_value: Type
    source_typename: Optional[str] = None
    target_type_value: Type = None
    target_typename: Optional[str] = None
    target_id: str = "v1"
    type_process: ProcessType = ProcessType.CUSTOM
    model_path: Optional[FilePath] = None
    value_specs: List[ValueSpec] = Field(default_factory=list)

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

    class Config:
        arbitrary_types_allowed = True
