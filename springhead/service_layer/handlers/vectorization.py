from collections import Counter

from river.feature_extraction import TFIDF
from statefun import Context, Message

from springhead.models import Process


def bag_of_words(context: Context, message: Message, process: Process) -> None:
    pass


def tfidf(context: Context, message: Message, process: Process) -> None:
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    tfidf = TFIDF()
    if document_counter:
        tfidf.dfs = Counter(document_counter)
        tfidf.n = document_number
    text = message.as_type(process.source_type_value)
    raw_text = text

    tfidf = tfidf.learn_one(raw_text)

    # Update docs storage
    context.storage.dfs = dict(tfidf.dfs)
    context.storage.n = tfidf.n

    request = {"tfidf": tfidf.transform_one(raw_text)}
    process.send(target_id=process.target_id, value=request, context=context)


def word2vec(context: Context, message: Message, process: Process) -> None:
    pass
