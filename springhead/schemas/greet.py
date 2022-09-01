from statefun import make_json_type

GREET_REQUEST_TYPE = make_json_type(typename="example/GreetRequest")
GREET_EGRESS_RECORD_TYPE = make_json_type(
    typename="io.statefun.playground/EgressRecord"
)
