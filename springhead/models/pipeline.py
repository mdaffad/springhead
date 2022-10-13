from __future__ import annotations

from typing import Dict

from pydantic.dataclasses import dataclass
from statefun import StatefulFunctions

from .process import Process


class PipelineException(Exception):
    pass


@dataclass
class Pipeline:
    processes: Dict[str, Process] = {}
    stateful_functions: StatefulFunctions = StatefulFunctions()

    def register_process(self, process: Process):
        if process.typename in self.processes.keys():
            raise PipelineException("process typename is not unique")
        self.processes[process.typename] = process
        self.stateful_functions.register(
            process.typename, process.stateful_function, process.specs
        )

    def show_config(self):
        pass
