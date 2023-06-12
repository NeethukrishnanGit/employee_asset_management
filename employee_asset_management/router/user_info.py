from fastapi import APIRouter, Body
from pydantic import json
from typing import Dict
from employee_asset_management.get_collection import user_Collection, instrument_Collection, audit_trail_Collection
from employee_asset_management.model.user_info import User
from bson.objectid import ObjectId
from datetime import datetime

json.ENCODERS_BY_TYPE[ObjectId] = str

user_app = APIRouter()


@user_app.post("/read_user_data")
async def get_user_data(data: Dict):
    user = user_Collection.find(data)
    user_data = list(user)
    return {"user_data": user_data}


@user_app.delete("/delete_user_data")
async def delete_user_data(user_id: str = Body(..., embed=True)):
    try:
        user_Collection.find_one_and_delete({"_id": ObjectId(user_id)})
    except:
        return "Something went wrong... Deletion Failed!"
    else:
        return "Successfully Deleted..."


@user_app.post("/insert_user_data")
async def create_user_data(user: User):
    user_data = user.dict()
    new_user = user_Collection.insert_one(user_data)
    return {"_id": str(new_user.inserted_id), **user_data}


@user_app.put("/update_user_data")
async def update_user_data(user_id: str = Body(...), role_change: str = Body(...)):
    id_doc = {"_id": ObjectId(user_id)}
    set_doc = {"$set": {"role": role_change}}
    user_Collection.update_one(id_doc, set_doc)
    data = list(user_Collection.find(id_doc))
    return {"updated data": data}