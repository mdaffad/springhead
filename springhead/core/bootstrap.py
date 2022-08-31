from dataclasses import dataclass
from typing import Any

from springhead.models import ModelLoader


@dataclass
class Bootstrap:
    model: Any


async def bootstrap(model: ModelLoader = ModelLoader("")):
    return Bootstrap(model)
