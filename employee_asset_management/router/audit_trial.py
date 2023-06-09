from fastapi import APIRouter
from pydantic import json
from bson.objectid import ObjectId
from employee_asset_management.db_creator import Audit_Collection
from employee_asset_management.model.audit_trial import Audit

json.ENCODERS_BY_TYPE[ObjectId] = str

audit_app = APIRouter()


@audit_app.post("/audit_data")
async def read_data():
    data = Audit_Collection.find()
    return {"audit_data": list(data)}


@audit_app.delete("/audit_data/delete/{get_id}")
async def delete_data(get_id: str):
    Audit_Collection.find_one_and_delete({"_id": ObjectId(get_id)})
    data = list(Audit_Collection.find())
    return {"After Deleted data": data}


@audit_app.post("/audit_data/post/")
async def insert_data(given_value: Audit):
    given_value.user_id = ObjectId(given_value.user_id)
    given_value.instrument_id = ObjectId(given_value.instrument_id)
    data = given_value.dict()
    Audit_Collection.insert_one(data)
    return {"inserted data": data}


@audit_app.put("/audit_data/put/")
async def update_data(my_id):
    my_query = {"_id": ObjectId(my_id)}
    update = {"$set": {"event_type": "check in"}}
    Audit_Collection.update_one(my_query, update)
    data = list(Audit_Collection.find({"_id": ObjectId(my_id)}))
    return {"updated data": data}
