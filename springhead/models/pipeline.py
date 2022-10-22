from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from statefun import StatefulFunctions

from .process import Process


class PipelineException(Exception):
    pass


@dataclass
class Pipeline:
    processes: Dict[str, Process] = field(default_factory=dict)
    stateful_functions: StatefulFunctions = StatefulFunctions()
    model_directory: Optional[str] = None

    def register_process(self, process: Process):
        if process.typename in self.processes.keys():
            raise PipelineException("process typename is not unique")
        self.processes[process.typename] = process
        self.stateful_functions.register(
            process.typename, process.stateful_function, process.value_specs
        )

    def show_config(self):
        pass
