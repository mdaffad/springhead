import logging

from river.feature_extraction import TFIDF
from statefun import Context, Message

from springhead.schemas import SPRINGHEAD_TEXT_REQUEST_TYPE

logger = logging.getLogger(__name__)


async def vectorize(context: Context, message: Message):
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    tf_idf = TFIDF()
    if document_counter:
        tf_idf.dfs = document_counter
        tf_idf.n = document_number

    text = message.as_type(SPRINGHEAD_TEXT_REQUEST_TYPE)

    tf_idf = tf_idf.learn_one(text)
    print(tf_idf.transform_one(text))
    # Update docs storage
    context.storage.dfs = dict(tf_idf.dfs)
    context.storage.n = tf_idf.n

    # enrich the request with the number of vists.
    # request = message.as_type(SPRINGHEAD_TEXT_REQUEST_TYPE)
    # request["visits"] = visits

    # next, we will forward a message to a special greeter function,
    # that will compute a super-doper-personalized greeting based on the
    # number of visits that this person has.
    # context.send(
    #     message_builder(
    #         target_typename="example/greeter",
    #         target_id=request["name"],
    #         value=request,
    #         value_type=GREET_REQUEST_TYPE,
    #     )
    # )
