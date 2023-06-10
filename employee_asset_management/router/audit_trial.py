from fastapi import APIRouter, Body
from pydantic import json
from typing import Dict
from bson.objectid import ObjectId
from employee_asset_management.get_collection import audit_trail_Collection, instrument_Collection
from employee_asset_management.model.audit_trial import Audit
from datetime import datetime

json.ENCODERS_BY_TYPE[ObjectId] = str

audit_app = APIRouter()


@audit_app.post("/read_audit_trail_data")
async def read_audit_trail_data(value: Dict):
    data = list(audit_trail_Collection.find(value))
    return {"audit_data": data}


@audit_app.delete("/delete_audit_trail_data")
async def delete_audit_trail_data(audit_id: str = Body(..., embed=True)):
    try:
        audit_trail_Collection.find_one_and_delete({"_id": ObjectId(audit_id)})
    except:
        return "Something went wrong... Failed to Delete!"
    else:
        return "Successfully Deleted..."


@audit_app.post("/insert_audit_trail_data")
async def insert_audit_trail_data(given_value: Audit):
    given_value.user_id = ObjectId(given_value.user_id)
    given_value.instrument_id = ObjectId(given_value.instrument_id)
    data = given_value.dict()
    audit_trail_Collection.insert_one(data)
    return {"inserted data": data}


# @audit_app.put("/update")
# async def update_data(my_id: str, value: Dict):
#     my_query = {"_id": ObjectId(my_id)}
#     update = {"$set": value}
#     Audit_Collection.update_one(my_query, update)
#     data = list(Audit_Collection.find(my_query))
#     return {"updated data": data}

@audit_app.post("/check_in_instrument")
async def check_in_instrument(user_id: str, instrument_id: str):
    instrument_query = {"_id": ObjectId(instrument_id)}
    instrument_update = {"$set": {"availability": True,
                                  "check_in": datetime.now(),
                                  "check_out": (datetime(2000, 1, 1, 00, 00, 00))}}

    instrument_Collection.update_one(instrument_query, instrument_update)
    audit_trail_value = {
        "user_id": ObjectId(user_id),
        "instrument_id": ObjectId(instrument_id),
        "event_type": "check_in",
        "time": datetime.now()
    }
    audit_trail_Collection.insert_one(audit_trail_value)
    return {"inserted data": audit_trail_value}
