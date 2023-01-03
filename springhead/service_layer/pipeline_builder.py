from typing import List, Optional

from springhead.models import Pipeline, Process


class PipelineBuilder:
    """
    Inject Process to Pipeline
    """

    @staticmethod
    def build(
        pipeline: Optional[Pipeline] = None, processes: List[Process] = []
    ) -> Pipeline:
        if not pipeline:
            pipeline = Pipeline()

        for process in processes:
            pipeline.register_process(process)

        return pipeline
