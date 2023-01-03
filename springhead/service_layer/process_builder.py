from __future__ import annotations

import logging

from springhead.models import (
    BagOfWordProcess,
    ClustreamProcess,
    CustomProcess,
    NormalizationProcess,
    Process,
    ProcessType,
    Specification,
    TFIDFProcess,
)
from springhead.schemas import (
    SPRINGHEAD_CLUSTREAM_VALUE_SPEC,
    SPRINGHEAD_DFS_VALUE_SPEC,
    SPRINGHEAD_N_DOCUMENT_VALUE_SPEC,
)

from .handlers import bag_of_words, clustream, normalize, tfidf
from .model_loader import ModelLoader

logger = logging.getLogger(__name__)


class ProcessBuilder:
    """
    Inject Specification to Process
    """

    process_type_to_function_mapper = {
        ProcessType.BAG_OF_WORD: (
            BagOfWordProcess,
            bag_of_words,
            [SPRINGHEAD_DFS_VALUE_SPEC],
        ),
        ProcessType.CLUSTREAM: (
            ClustreamProcess,
            clustream,
            [SPRINGHEAD_CLUSTREAM_VALUE_SPEC],
        ),
        ProcessType.NORMALIZATION: (NormalizationProcess, normalize, []),
        ProcessType.TFIDF: (
            TFIDFProcess,
            tfidf,
            [SPRINGHEAD_DFS_VALUE_SPEC, SPRINGHEAD_N_DOCUMENT_VALUE_SPEC],
        ),
        # TODO: implement for CUSTOM type mapper
        ProcessType.CUSTOM: (CustomProcess, None, []),
    }

    @classmethod
    def map_custom_function(cls, process_type: ProcessType):

        return

    @classmethod
    def build(
        cls, specification: Specification, custom_function=None, custom_value_spec=[]
    ) -> Process:
        (
            implemented_class,
            implemented_function,
            value_specs,
        ) = cls.process_type_to_function_mapper[specification.type_process]

        if implemented_class == CustomProcess:
            if custom_function is None or custom_value_spec == []:
                raise Exception("No implementation of custom function")
            implemented_function = None
            value_specs = []

        process = None
        try:
            model = None
            if specification.model_path:
                model = ModelLoader.load_model(specification.model_path)  # type: ignore
            process = implemented_class(
                function_handler=implemented_function,
                value_specs=value_specs,
                model=model,
                **specification.asdict(exception={"model_path"}),
            )
        except Exception as e:
            logger.error(implemented_class)
            raise e
        else:
            return process
