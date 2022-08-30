import asyncio

from statefun import *  # noqa: F403

functions = StatefulFunctions()

GREET_REQUEST_TYPE = make_json_type(typename="example/GreetRequest")
EGRESS_RECORD_TYPE = make_json_type(typename="io.statefun.playground/EgressRecord")


@functions.bind(
    typename="example/person", specs=[ValueSpec(name="visits", type=IntType)]
)
async def person(context: Context, message: Message):
    # update the visit count.
    visits = context.storage.visits or 0
    visits += 1
    context.storage.visits = visits

    # enrich the request with the number of vists.
    request = message.as_type(GREET_REQUEST_TYPE)
    request["visits"] = visits

    # next, we will forward a message to a special greeter function,
    # that will compute a super-doper-personalized greeting based on the
    # number of visits that this person has.
    context.send(
        message_builder(
            target_typename="example/greeter",
            target_id=request["name"],
            value=request,
            value_type=GREET_REQUEST_TYPE,
        )
    )


@functions.bind(typename="example/greeter")
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
            value_type=EGRESS_RECORD_TYPE,
        )
    )


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

    await asyncio.sleep(1)
    return greeting


#
# Serve the endpoint
#


handler = RequestReplyHandler(functions)


async def handle(request):
    req = await request.read()
    res = await handler.handle_async(req)
    return web.Response(body=res, content_type="application/octet-stream")


app = web.Application()
app.add_routes([web.post("/statefun", handle)])

if __name__ == "__main__":
    web.run_app(app, port=8000)
