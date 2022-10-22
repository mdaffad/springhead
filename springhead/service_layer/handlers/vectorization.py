from river.feature_extraction import TFIDF
from statefun import Context, Message

from springhead.models import Process
from springhead.schemas import SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE


def bag_of_words(context: Context, message: Message, process: Process) -> None:
    pass


def tf_idf(context: Context, message: Message, process: Process) -> None:
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    tf_idf = TFIDF()
    if document_counter:
        tf_idf.dfs = document_counter
        tf_idf.n = document_number

    text = message.as_type(process.source_type_value)

    tf_idf = tf_idf.learn_one(text)

    # Update docs storage
    context.storage.dfs = dict(tf_idf.dfs)
    context.storage.n = tf_idf.n

    request = message.as_type(SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE)
    request["tf_idf"] = dict(tf_idf.transform_one(text))

    # TODO: define what id used for in this method => maybe target/version model
    process.send(target_id=process.target_id, value=request, context=context)


def word2vec(context: Context, message: Message, process: Process) -> None:
    pass
