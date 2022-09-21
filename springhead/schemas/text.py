from statefun import make_json_type

SPRINGHEAD_TEXT_REQUEST_TYPE = make_json_type(typename="springhead/TextRequest")
SPRINGHEAD_POST_PREPROCESS_REQUEST_TYPE = make_json_type(
    typename="springhead/PostPreprocessRequest"
)

SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE = make_json_type(
    typename="springhead/TextEgressRecord"
)
