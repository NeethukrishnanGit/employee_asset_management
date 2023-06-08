from pydantic import BaseModel, Field
from enum import Enum


class Roles(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    CUSTOMER = "CUSTOMER"
    PARTNER = "PARTNER"


class User(BaseModel):
    user_name: str = Field(...)
    role: Roles = Field(...)
