# Springhead

Declarative Apache Flink Statefun over FastAPI

## Requirement
1. Python ^3.9
2. Poetry
2. GNU Make
3. [Compose V2](https://docs.docker.com/compose/compose-v2/)

## Quick Start

1. Run run_dev recipe on Makefile

```bash
make run_dev 
```

2. Create consumer to subcribe message on `cluster` topic. Example

```python
from kafka import KafkaConsumer

if __name__ == "__main__":

    topic_name = "cluster"
    try:
        consumer = KafkaConsumer(topic_name, bootstrap_servers=["localhost:9092"])
        for message in consumer:
            message = message.value
            print(message)
    except Exception as e:
        print(str(e))

```

3. Create producer to publish message on `message-topic` topic. Example
```python
import json
from time import sleep
import pandas as pd

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

if __name__ == "__main__":
    data = pd.read_csv('file:///path-to-your-data-csv')
    topic_name = "message-topic"
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

    datas = data["your-str-column"]
    total_data = len(datas)
    for index, content in enumerate(datas):
        producer.send(topic_name, value=content.encode("utf-8"), key="test".encode("utf-8"))
        sleep(0.1)
```