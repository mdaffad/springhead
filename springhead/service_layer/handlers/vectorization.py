from river.feature_extraction import TFIDF
from statefun import Context, Message

from springhead.models import Process
from springhead.schemas import SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE


def bag_of_words(context: Context, message: Message, process: Process) -> None:
    pass


def tfidf(context: Context, message: Message, process: Process) -> None:
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    tfidf = TFIDF()
    if document_counter:
        tfidf.dfs = document_counter
        tfidf.n = document_number

    # TODO: Fix this => change to json with {"text": str}
    # => for simple like state-fun playground
    # and kafka client
    # File "/app/./springhead/service_layer/handlers/vectorization.py"
    # , line 21, in tfidf
    #   text = message.as_type(process.source_type_value)
    # File "/opt/venv/lib/python3.9/site-packages/statefun/messages.py"
    # , line 99, in as_type
    text = message.as_type(process.source_type_value)

    tfidf = tfidf.learn_one(text)

    # Update docs storage
    context.storage.dfs = dict(tfidf.dfs)
    context.storage.n = tfidf.n

    request = message.as_type(SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE)
    request["tfidf"] = dict(tfidf.transform_one(text))

    process.send(target_id=process.target_id, value=request, context=context)


def word2vec(context: Context, message: Message, process: Process) -> None:
    pass
