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

    tf_idf = TFIDF()
    if document_counter:
        tf_idf.dfs = document_counter
        tf_idf.n = document_number

    text = message.as_type(SPRINGHEAD_TEXT_REQUEST_TYPE)

    tf_idf = tf_idf.learn_one(text)

    # Update docs storage
    context.storage.dfs = dict(tf_idf.dfs)
    context.storage.n = tf_idf.n

    request = message.as_type(SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE)
    request["tf_idf"] = dict(tf_idf.transform_one(text))

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
    tf_idf = request["tf_idf"]

    egress_record = {"topic": "cluster", "payload": tf_idf}

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

"""
LOG error
2022-09-24 11:49:44
java.lang.IllegalStateException: The io.statefun.kafka.v1/ingress ingress requires a UTF-8 key set for each record.
	at org.apache.flink.statefun.flink.io.kafka.binders.ingress.v1.RoutableKafkaIngressDeserializer.requireNonNullKey(RoutableKafkaIngressDeserializer.java:70)
	at org.apache.flink.statefun.flink.io.kafka.binders.ingress.v1.RoutableKafkaIngressDeserializer.deserialize(RoutableKafkaIngressDeserializer.java:48)
	at org.apache.flink.statefun.flink.io.kafka.binders.ingress.v1.RoutableKafkaIngressDeserializer.deserialize(RoutableKafkaIngressDeserializer.java:29)
	at org.apache.flink.statefun.flink.io.kafka.KafkaDeserializationSchemaDelegate.deserialize(KafkaDeserializationSchemaDelegate.java:46)
	at org.apache.flink.streaming.connectors.kafka.KafkaDeserializationSchema.deserialize(KafkaDeserializationSchema.java:79)
	at org.apache.flink.streaming.connectors.kafka.internals.KafkaFetcher.partitionConsumerRecordsHandler(KafkaFetcher.java:179)
	at org.apache.flink.streaming.connectors.kafka.internals.KafkaFetcher.runFetchLoop(KafkaFetcher.java:142)
	at org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumerBase.run(FlinkKafkaConsumerBase.java:826)
	at org.apache.flink.streaming.api.operators.StreamSource.run(StreamSource.java:110)
	at org.apache.flink.streaming.api.operators.StreamSource.run(StreamSource.java:67)
	at org.apache.flink.streaming.runtime.tasks.SourceStreamTask$LegacySourceFunctionThread.run(SourceStreamTask.java:323)

TODO: Maybe there are issue on deserializer for TextRequest
"""
