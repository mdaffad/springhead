from dataclasses import dataclass
from typing import Any

from springhead.models import ModelLoader, Pipeline
from springhead.service_layer import PipelineBuilder


@dataclass
class Bootstrap:
    text_model: Any
    pipeline: Pipeline


async def bootstrap(
    model: ModelLoader = ModelLoader(""), pipeline: Pipeline = PipelineBuilder.build()
):
    return Bootstrap(model)
