import logging
from asyncio import sleep

from statefun import StringType, kafka_egress_message

from springhead.schemas import GREET_EGRESS_RECORD_TYPE

logger = logging.getLogger(__name__)


async def compute_fancy_greeting(name: str, seen: int):
    """
    Compute a personalized greeting,
    based on the number of times this @name had been seen before.
    """
    templates = [
        "",
        "Welcome %s",
        "Nice to see you again %s",
        "Third time is a charm %s",
    ]
    if seen < len(templates):
        greeting = templates[seen] % name
    else:
        greeting = f"Nice to see you at the {seen}-nth time {name}!"

    await sleep(1)
    return greeting


async def greeter(context, message):
    logger.error("GET IN THE GREETER")
    request = message.as_type(StringType)

    person_name = request
    logger.debug(context.storage)

    greeting = person_name

    egress_record = {"topic": "greetings", "payload": greeting}

    context.send_egress(
        kafka_egress_message(
            typename="springhead/kafka-egress",
            topic="cluster",
            key="test",
            value=egress_record,
            value_type=GREET_EGRESS_RECORD_TYPE,
        )
    )
