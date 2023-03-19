from pydantic import BaseModel


class MeterValue(BaseModel):
    value: int
