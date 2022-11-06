from pickle import dumps, loads

from statefun import IntType, ValueSpec, make_json_type, simple_type

from springhead.utils import CustomEnumType


# Non-protobuf type
class SpringheadType(CustomEnumType):
    NON_PROTOBUF_STRING = "str-no-protobuf"


def serialize_to_utf_8(value: str):
    return value.encode("utf-8")


def deserialize_to_utf_8(value):
    return value.decode("utf-8")


SPRINGHEAD_STRING_TYPE = simple_type(
    typename="springhead/string",
    serialize_fn=serialize_to_utf_8,
    deserialize_fn=deserialize_to_utf_8,
)

SPRINGHEAD_TEXT_EGRESS_RECORD_TYPE = make_json_type(typename="springhead/egress")
SPRINGHEAD_DFS_TYPE = make_json_type(typename="springhead/tfidf")
SPRINGHEAD_CLUSTREAM_TYPE = simple_type(
    typename="springhead/clustream",
    serialize_fn=dumps,
    deserialize_fn=loads,
)


SPRINGHEAD_DFS_VALUE_SPEC = ValueSpec(name="dfs", type=SPRINGHEAD_DFS_TYPE)
SPRINGHEAD_CLUSTREAM_VALUE_SPEC = ValueSpec(
    name="clustream", type=SPRINGHEAD_CLUSTREAM_TYPE
)

SPRINGHEAD_N_DOCUMENT_VALUE_SPEC = ValueSpec(name="n", type=IntType)
