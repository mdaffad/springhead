from __future__ import annotations

from typing import Dict, List

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
        self.stateful_functions.register(process.typename, process.func, process.specs)


class PipelineBuilder:
    @staticmethod
    def build(pipeline: Pipeline = None, processes: List[Process] = []) -> Pipeline:
        if not pipeline:
            pipeline = Pipeline()

        for process in processes:
            pipeline.register_process(process)

        return pipeline
