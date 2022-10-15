from __future__ import annotations

from dataclasses import field
from typing import Dict

from pydantic import DirectoryPath
from pydantic.dataclasses import dataclass
from statefun import StatefulFunctions

from springhead.utils import Config

from .process import Process


class PipelineException(Exception):
    pass


@dataclass(config=Config)
class Pipeline:
    processes: Dict[str, Process] = field(default_factory=dict)
    stateful_functions: StatefulFunctions = StatefulFunctions()
    model_directory: DirectoryPath = "./app/nlp_models"

    def register_process(self, process: Process):
        if process.typename in self.processes.keys():
            raise PipelineException("process typename is not unique")
        self.processes[process.typename] = process
        self.stateful_functions.register(
            process.typename, process.stateful_function, process.specs
        )

    def show_config(self):
        pass
