from __future__ import annotations

from dataclasses import dataclass
from typing import List

from statefun import RequestReplyHandler

from springhead.models import Pipeline, Process
from springhead.service_layer import (
    PipelineBuilder,
    ProcessBuilder,
    SpecificationBuilder,
)


@dataclass
class Bootstrap:
    pipeline: Pipeline
    handler: RequestReplyHandler


async def bootstrap() -> None:
    specification_builder = SpecificationBuilder("./app/specifications.yml")
    specifications = specification_builder.read_spec_file()
    processes: List[Process] = []
    for specification in specifications:
        process = ProcessBuilder.build(specification=specification)
        processes.append(process)

    pipeline: Pipeline = PipelineBuilder.build(processes=processes)
    handler = RequestReplyHandler(pipeline.stateful_functions)
    return Bootstrap(pipeline=pipeline, handler=handler)
