from statefun import message_builder

from springhead.schemas import GREET_REQUEST_TYPE


async def person(context, message):
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
