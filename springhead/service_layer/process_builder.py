import logging
from typing import Optional, Type

from springhead.models import (
    ClustreamProcess,
    FilteringProcess,
    Process,
    ProcessType,
    Specification,
    TFIDFProcess,
    TransformationProcess,
)
from springhead.models.normalization_process import NormalizationProcess
from springhead.models.tokenization_process import TokenizationProcess
from springhead.models.vectorization_process import Word2VecProcess
from springhead.schemas import SPRINGHEAD_TFIDF_VALUE_SPEC

from .handlers import (
    bag_of_words,
    clustream,
    filter,
    normalize,
    tfidf,
    tokenize,
    transform,
    word2vec,
)

logger = logging.getLogger(__name__)


class ProcessBuilder:
    """
    Inject Specification to Process
    """

    # TODO: refactor as one flat key-value ProcessType
    process_type_to_function_mapper = {
        ProcessType.BAG_OF_WORD: (TransformationProcess, bag_of_words, []),
        ProcessType.CLUSTREAM: (ClustreamProcess, clustream, []),
        ProcessType.FILTERING: (FilteringProcess, filter, []),
        ProcessType.NORMALIZATION: (NormalizationProcess, normalize, []),
        ProcessType.TFIDF: (TFIDFProcess, tfidf, [SPRINGHEAD_TFIDF_VALUE_SPEC]),
        ProcessType.TOKENIZATION: (TokenizationProcess, tokenize, []),
        ProcessType.TRANSFORMATION: (TransformationProcess, transform, []),
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
            implemented_class: Type[Process]
            process = implemented_class(
                func=implemented_function,
                value_specs=value_specs,
                **specification.asdict()
            )
        except Exception as e:
            logger.error(e)
        finally:
            return process
