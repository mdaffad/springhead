from typing import Callable, Dict

from pydantic import BaseModel


class Pipeline(BaseModel):
    processes: Dict[str, Callable]

    def process(self, process_id: str) -> Callable:  # pragma: nocover
        def decorator(func: Callable) -> Callable:
            self.register_process(process_id, func)
            return func

        return decorator

    def register_process(self, process_id: str, process: Callable):
        self.processes[process_id] = process

    pass
