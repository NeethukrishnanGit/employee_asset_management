from bson import ObjectId
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    Check_out = "Check Out"
    Check_in = "Check In"


class Audit(BaseModel):
    user_id: ObjectId = Field(...)
    instrument_id: ObjectId = Field(...)
    Event_Type: Status = Field(...)
    Date_Time: str = Field(default=datetime.utcnow())
