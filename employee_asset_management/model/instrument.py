from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Instruments(BaseModel):
    name: str = Field(...)
    type: str = Field(...)
    description: Optional[str]
    availability: bool = Field(...)
    check_in: str = Field(default=datetime.utcnow())
    check_out: str = Field(default=datetime.utcnow())
