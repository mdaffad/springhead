from __future__ import annotations

import logging
from typing import Optional

from springhead.models import (
    BagOfWordProcess,
    ClustreamProcess,
    NormalizationProcess,
    Process,
    ProcessType,
    Specification,
    TFIDFProcess,
    Word2VecProcess,
)
from springhead.schemas import (
    SPRINGHEAD_CLUSTREAM_VALUE_SPEC,
    SPRINGHEAD_DFS_VALUE_SPEC,
    SPRINGHEAD_N_DOCUMENT_VALUE_SPEC,
)

from .handlers import bag_of_words, clustream, normalize, tfidf, word2vec

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
        ProcessType.WORD2VEC: (Word2VecProcess, word2vec, []),
    }

    @classmethod
    def build(cls, specification: Specification) -> Optional[Process]:
        (
            implemented_class,
            implemented_function,
            value_specs,
        ) = cls.process_type_to_function_mapper[specification.type_process]
        process = None
        try:
            process = implemented_class(
                function_handler=implemented_function,
                value_specs=value_specs,
                **specification.asdict(),
            )
        except Exception as e:
            logger.error(implemented_class)
            # logger.error(e)
            raise e
        else:
            return process
