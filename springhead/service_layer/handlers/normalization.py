import unicodedata

import nltk
from nltk.tokenize import word_tokenize
from statefun import Context, Message

from springhead.models import Process

nltk.download("stopwords")

stopwords = set(nltk.corpus.stopwords.words("english"))
lemmatizer = nltk.stem.WordNetLemmatizer()


def is_punct(token):
    return all(unicodedata.category(char).startswith("P") for char in token)


def is_stopword(token):
    return token.lower() in stopwords


def lemmatize(token):
    return lemmatizer.lemmatize(token)


def normalize(context: Context, message: Message, process: Process) -> None:
    # TODO: normalize
    text: str = message.as_type(process.source_type_value)  # str expected
    normalized_text = [
        lemmatize(word).lower()
        for word in word_tokenize(text)
        if not is_punct(word) and not is_stopword(word)
    ]
    process.send(target_id=process.target_id, value=normalized_text, context=context)
