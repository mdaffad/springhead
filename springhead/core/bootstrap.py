from dataclasses import dataclass

from springhead.models import Pipeline
from springhead.service_layer import PipelineBuilder


@dataclass
class Bootstrap:
    pipeline: Pipeline


async def bootstrap() -> None:
    # TODO: read specification
    # TODO: build process by specification: inject specification to ProcessBuilder
    # TODO: register process to pipeline: inject Process to Pipeline
    pipeline = PipelineBuilder.build()
    return Bootstrap(pipeline)
