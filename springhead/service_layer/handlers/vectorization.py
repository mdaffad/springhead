from collections import Counter

from river.feature_extraction import TFIDF, BagOfWords
from statefun import Context, Message

from springhead.models import Process


def bag_of_words(context: Context, message: Message, process: Process) -> None:
    document_counter = context.storage.dfs or {}
    if not document_counter and process.model:
        document_counter = process.model.pickled_object
    else:
        document_counter = Counter(document_counter)

    bow = BagOfWords()

    text = message.as_type(process.source_type_value)
    bow = bow.transform_one(text)

    dfs = dict(document_counter + bow)
    context.storage.dfs = dfs

    request = {"bag_of_words": dfs}
    process.send(target_id=process.target_id, value=request, context=context)


def tfidf(context: Context, message: Message, process: Process) -> None:
    document_counter = context.storage.dfs or {}
    document_number = context.storage.n or 0

    if not document_counter and process.model and document_number == 0:
        document_counter = process.model.pickled_object.dfs
        document_number = process.model.pickled_object.n

    tfidf = TFIDF()
    if document_counter:
        tfidf.dfs = Counter(document_counter)
        tfidf.n = document_number
    text = message.as_type(process.source_type_value)

    tfidf = tfidf.learn_one(text)

    # Update docs storage
    dfs = tfidf.dfs
    n = tfidf.n
    context.storage.dfs = dict(dfs)
    context.storage.n = n

    tfidf = tfidf.transform_one(text)
    request = {
        "vectorized_value": tfidf,
    }
    process.send(target_id=process.target_id, value=request, context=context)
