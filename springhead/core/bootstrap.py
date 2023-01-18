from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from pydantic import AnyHttpUrl, FilePath
from statefun import Context, Message, RequestReplyHandler, ValueSpec

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
    side_car_address: AnyHttpUrl = "http://sidecar:8889/springhead"  # type: ignore
    type_test_case: str = "all-combination"
    benchmark_mode: bool = False


async def bootstrap(
    specification_path: FilePath = "./app/specifications.yml",  # type: ignore
    custom_functions: Dict[str, Callable[[Context, Message, Process], None]] = dict(),
    custom_value_specs: Dict[str, List[ValueSpec]] = dict(),
    side_car_address: AnyHttpUrl = "http://sidecar:8889/springhead",  # type: ignore
    type_test_case: str = "all-combination",
    benchmark_mode: bool = False,
) -> Bootstrap:
    specification_builder = SpecificationBuilder(specification_path)  # type: ignore
    specifications = specification_builder.read_spec_file()
    processes: List[Process] = []
    for specification in specifications:
        custom_function = custom_functions.get(specification.typename)
        custom_value_spec = custom_value_specs.get(specification.typename, [])
        process = ProcessBuilder.build(
            specification=specification,
            custom_function=custom_function,
            custom_value_spec=custom_value_spec,
        )
        processes.append(process)

    pipeline: Pipeline = PipelineBuilder.build(processes=processes)
    handler = RequestReplyHandler(pipeline.stateful_functions)
    return Bootstrap(
        pipeline=pipeline,
        handler=handler,
        side_car_address=side_car_address,
        type_test_case=type_test_case,
        benchmark_mode=benchmark_mode,
    )
