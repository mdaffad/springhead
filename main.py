from cmath import log
from collections import Counter
from json import dumps, loads

import faust
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

from springhead.model.record import DynamicRecord

KAFKA_HOST = "localhost:9092"

app = faust.App(
    "main",
    broker=f"kafka://{KAFKA_HOST}",
    value_serializer="raw",
)


dynamic_record = DynamicRecord(
    {
        "email": {
            "type_def": "str",
        },
        "age": {"type_def": "int", "default": "asd"},
    }
)

TOTAL_DOCUMENT = "total_document"
TERM_FOUND_IN_DOCUMENT = "term_found_in_document"
FINISHED_PREPROCESS_TEXT = "vectorizer"

text_stream_topic = app.topic("text_stream", value_type=bytes)
vectorizer_topic = app.topic(FINISHED_PREPROCESS_TEXT, value_type=bytes)

total_document = app.Table(TOTAL_DOCUMENT, default=int, partitions=1)
term_found_in_document = app.Table(
    TERM_FOUND_IN_DOCUMENT,
    default=int,
    partitions=1,
)


@app.agent(text_stream_topic)
async def process_input(texts):
    async for text_json in texts:
        text = loads(text_json)["text"]
        total_document["total"] += 1
        preprocessed_texts = text.lower().split(" ")
        map_texts = Counter(preprocessed_texts)
        for map_text in map_texts:
            term_found_in_document[map_text] += 1

        topic_name = FINISHED_PREPROCESS_TEXT
        producer = KafkaProducer(bootstrap_servers=[KAFKA_HOST])

        try:
            # Create Kafka topic
            topic = NewTopic(
                name=topic_name,
                num_partitions=1,
                replication_factor=1,
            )
            admin = KafkaAdminClient(bootstrap_servers=KAFKA_HOST)
            admin.create_topics([topic])
        except Exception:
            print(f"Topic {topic_name} is already created")

        json_text_data = {"text": preprocessed_texts}
        producer.send(topic_name, dumps(json_text_data).encode("utf-8"))


@app.agent(vectorizer_topic)
async def vectorizer(preprocessed_texts):
    async for text_byte in preprocessed_texts:
        text = loads(text_byte)["text"]
        map_texts = Counter(text)
        for map_text in map_texts:
            tf = map_texts[map_text] / len(map_texts)
            print(tf)
            idf = log(total_document["total"] / term_found_in_document[map_text])
            print(total_document["total"])
            print(term_found_in_document[map_text])
            print(tf * idf)
