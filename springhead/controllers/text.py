# flake8: noqa: E501

import logging

from river.feature_extraction import TFIDF
from statefun import Context, Message, egress_message_builder, message_builder

from springhead.schemas import (
    SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE,
    SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE,
    SPRINGHEAD_TEXT_REQUEST_TYPE,
)

logger = logging.getLogger(__name__)


async def vectorize(context: Context, message: Message):
    # NOTE: context is scoped for current
    # address(context.address.typename, context.address.id)
    # Read on flink statefun playground
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    tfidf = TFIDF()
    if document_counter:
        tfidf.dfs = document_counter
        tfidf.n = document_number

    text = message.as_type(SPRINGHEAD_TEXT_REQUEST_TYPE)

    tfidf = tfidf.learn_one(text)

    # Update docs storage
    context.storage.dfs = dict(tfidf.dfs)
    context.storage.n = tfidf.n

    request = message.as_type(SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE)
    request["tfidf"] = dict(tfidf.transform_one(text))

    # TODO: define what id used for in this method => maybe target/version model

    context.send(
        message_builder(
            target_typename="springhead/cluster",
            target_id=request["name"],
            value=request,
            value_type=SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE,
        )
    )


async def cluster(context: Context, message: Message):
    request = message.as_type(SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE)
    tfidf = request["tfidf"]

    egress_record = {"topic": "cluster", "payload": tfidf}

    context.send_egress(
        egress_message_builder(
            target_typename="io.statefun.playground/egress",
            value=egress_record,
            value_type=SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE,
        )
    )


# TODO:
# option: add fucntion to templation sub task on flink => dynamic binding for function e.g register function form template
# define template to pass between function
# preprocess model
# follow transformers templating

"""
    processes:
    - name: tfidf
        function: river.tfidf
        model: './river-tfidf.pickle'
    - name: cluster
        function: river.cluster
        model: './river-cluster.pickle'
"""
