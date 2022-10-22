from statefun import ValueSpec, make_json_type

SPRINGHEAD_TEXT_REQUEST_TYPE = make_json_type(typename="springhead/TextRequest")
SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE = make_json_type(
    typename="springhead/PostPreprocessRequest"
)

SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE = make_json_type(
    typename="springhead/TextEgressRecord"
)

SPRINGHEAD_TF_IDF_TYPE = make_json_type(typename="springhead/TFIDF")

SPRINGHEAD_TF_IDF_VALUE_SPEC = ValueSpec(name="tf_idf", type=SPRINGHEAD_TF_IDF_TYPE)
