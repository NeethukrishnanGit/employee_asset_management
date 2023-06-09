from fastapi import APIRouter, Body
from pydantic import json
from typing import Dict
from bson.objectid import ObjectId
from employee_asset_management.db_creator import Audit_Collection
from employee_asset_management.model.audit_trial import Audit

json.ENCODERS_BY_TYPE[ObjectId] = str

audit_app = APIRouter()


@audit_app.post("/audit_data/read")
async def read__audit_data(value: Dict):
    data = list(Audit_Collection.find(value))
    return {"audit_data": data}


@audit_app.delete("/audit_data/delete_one")
async def delete_audit_data(audit_id: str = Body(..., embed=True)):
    try:
        Audit_Collection.find_one_and_delete({"_id": ObjectId(audit_id)})
    except:
        return "Something went wrong... Failed to Delete!"
    else:
        return "Successfully Deleted..."


@audit_app.post("/audit_data/insert_one")
async def insert_audit_data(given_value: Audit):
    given_value.user_id = ObjectId(given_value.user_id)
    given_value.instrument_id = ObjectId(given_value.instrument_id)
    data = given_value.dict()
    Audit_Collection.insert_one(data)
    return {"inserted data": data}


# @audit_app.put("/audit_data/update")
# async def update_data(my_id: str, value: Dict):
#     my_query = {"_id": ObjectId(my_id)}
#     update = {"$set": value}
#     Audit_Collection.update_one(my_query, update)
#     data = list(Audit_Collection.find(my_query))
#     return {"updated data": data}
