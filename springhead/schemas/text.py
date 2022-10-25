from statefun import IntType, ValueSpec, make_json_type

SPRINGHEAD_TEXT_REQUEST_TYPE = make_json_type(typename="springhead/TextRequest")
SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE = make_json_type(
    typename="springhead/PostPreprocessRequest"
)

SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE = make_json_type(
    typename="springhead/TextEgressRecord"
)

SPRINGHEAD_TFIDF_TYPE = make_json_type(typename="springhead/TFIDF")

SPRINGHEAD_DFS_VALUE_SPEC = ValueSpec(name="dfs", type=SPRINGHEAD_TFIDF_TYPE)

SPRINGHEAD_N_DOCUMENT_VALUE_SPEC = ValueSpec(name="n", type=IntType)
