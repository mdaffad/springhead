from asyncio import sleep

from statefun import egress_message_builder

from springhead.schemas import GREET_EGRESS_RECORD_TYPE, GREET_REQUEST_TYPE


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
    request = message.as_type(GREET_REQUEST_TYPE)
    person_name = request["name"]
    visits = request["visits"]

    greeting = await compute_fancy_greeting(person_name, visits)

    egress_record = {"topic": "greetings", "payload": greeting}

    context.send_egress(
        egress_message_builder(
            target_typename="io.statefun.playground/egress",
            value=egress_record,
            value_type=GREET_EGRESS_RECORD_TYPE,
        )
    )
