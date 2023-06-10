from pydantic import BaseModel, Field
from datetime import datetime


class Audit(BaseModel):
    user_id: str = Field(...)
    instrument_id: str = Field(...)
    event_type: str = Field(...)
    time: datetime = Field(default=datetime(2000, 1, 1, 00, 00, 00))
