from __future__ import annotations

from typing import Dict, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass
from statefun import Context, Message, StatefulFunctions

from springhead.utils import Config

from .process import Process


class PipelineException(Exception):
    pass


@dataclass(config=Config)
class Pipeline:
    processes: Dict[str, Process] = Field(default_factory=dict)
    stateful_functions: StatefulFunctions = StatefulFunctions()
    model_directory: Optional[str] = None

    def register_process(self, process: Process):
        if process.typename in self.processes.keys():
            raise PipelineException("process typename is not unique")

        # wrap function at here to not self inject process on its own handler_function
        def wrapped_springhead_process(context: Context, message: Message):
            function_handler = process.function_handler
            process_dependency = process
            return function_handler(context, message, process_dependency)

        self.processes[process.typename] = process
        self.stateful_functions.register(
            process.typename, wrapped_springhead_process, process.value_specs
        )

    def show_config(self):
        pass

    class Config:
        arbitrary_types_allowed = True
