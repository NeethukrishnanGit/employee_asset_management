from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Instruments(BaseModel):
    name: str = Field(...)
    type: str = Field(...)
    description: Optional[str]
    availability: bool = Field(...)
    check_in: datetime = Field(default=datetime(2000, 1, 1, 00, 00, 00))
    check_out: datetime = Field(default=datetime(2000, 1, 1, 00, 00, 00))
