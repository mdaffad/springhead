import json

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":

    topic_name = "text_stream"
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    try:
        # Create Kafka topic
        topic = NewTopic(
            name=topic_name,
            num_partitions=1,
            replication_factor=1,
        )
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
        admin.create_topics([topic])
    except Exception:
        print(f"Topic {topic_name} is already created")

    for i in range(10):
        text = {
            "text": "EventStreams is a Web Service that Exposes "
            "continuous streams of structured event data. "
            "It does so over HTTP using chunked transfer "
            "encoding following the Server-Sent Events "
            "protocol (SSE). EventStreams can be consumed"
            "directly via HTTP, but is more commonly used"
            "via a client library."
        }
        producer.send(topic_name, json.dumps(text).encode("utf-8"))
        print(f"Published message to message broker. text: {text}")

    text = {"text": "continuous integration and delivery"}
    producer.send(topic_name, json.dumps(text).encode("utf-8"))
    print(f"Published message to message broker. text: {text}")
