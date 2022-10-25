from __future__ import annotations

from typing import Any, Callable, List, Optional

from pydantic import BaseModel, Field, FilePath, root_validator
from statefun import (
    Context,
    Message,
    Type,
    ValueSpec,
    egress_message_builder,
    message_builder,
)

from springhead.schemas import SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE
from springhead.utils import CustomEnumType


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


# @dataclass(config=Config)
class Process(BaseModel):
    typename: str
    function_handler: Callable[[Context, Message, Process], None]
    source_type_value: Type
    stateful_function: Callable[[Context, Message], None]
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

    def inject_process_dependency(self):
        return self

    @root_validator(pre=True)
    def generate_stateful_function(cls, values):
        def wrapped_springhead_process(context: Context, message: Message):
            function_handler = values.get("function_handler")
            process_dependency = cls.inject_process_dependency()
            return function_handler(context, message, process_dependency)

        values["stateful_function"] = wrapped_springhead_process
        return values

    class Config:
        arbitrary_types_allowed = True
