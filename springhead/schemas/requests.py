from pydantic import BaseModel


class SpringheadTimeCreateRequest(BaseModel):
    time_ns: int
    type_timer: str
    type_test_case: str
