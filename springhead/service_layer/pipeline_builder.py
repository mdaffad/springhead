from typing import List

from springhead.models import Pipeline, Process


class PipelineBuilder:
    @staticmethod
    def build(pipeline: Pipeline = None, processes: List[Process] = []) -> Pipeline:
        if not pipeline:
            pipeline = Pipeline()

        for process in processes:
            pipeline.register_process(process)

        return pipeline
