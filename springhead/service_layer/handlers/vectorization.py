from collections import Counter

from river.feature_extraction import TFIDF, BagOfWords
from statefun import Context, Message

from springhead.models import Process


def bag_of_words(context: Context, message: Message, process: Process) -> None:
    # TODO: add model loader for bag_of_words when document_cunter == {}
    document_counter = context.storage.dfs or {}
    document_counter = Counter(document_counter)
    bow = BagOfWords()

    text = message.as_type(process.source_type_value)
    bow = bow.transform_one(text)

    dfs = dict(document_counter + bow)
    context.storage.dfs = dfs

    request = {"bag_of_words": dfs}
    process.send(target_id=process.target_id, value=request, context=context)


def tfidf(context: Context, message: Message, process: Process) -> None:
    # TODO: add model loader for bag_of_words when document_cunter == {} or n == 0
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
