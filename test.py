from river import feature_extraction

corpus = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
]
dfs = None
n = None
for sentence in corpus:
    tfidf = None
    tfidf = feature_extraction.TFIDF()
    if dfs:
        tfidf.dfs = dfs
        tfidf.n = n
    tfidf = tfidf.learn_one(sentence)
    print(tfidf.transform_one(sentence))
    dfs = tfidf.dfs
    n = tfidf.n
    print(tfidf.dfs)
    print(tfidf.n)
