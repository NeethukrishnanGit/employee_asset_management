from fastapi import APIRouter
from pydantic import json
from employee_asset_management.db_creator import user_Collection
from employee_asset_management.model.user_info import User
from bson.objectid import ObjectId

json.ENCODERS_BY_TYPE[ObjectId] = str


user_app = APIRouter()


@user_app.post("/get_users/{getuser_id}")
async def get_all_data(user_id: str):
    user = user_Collection.find({"_id": ObjectId(user_id)})
    return {"user_data": list(user)}


@user_app.delete("/users/{user_id}")
async def delete_data(user_id: str):
    user = user_Collection.find_one_and_delete({"_id": ObjectId(user_id)})
    return f"{user} DELETED"


@user_app.post("/users/{user_id}")
async def create_data(user_id: str):
    user = user_Collection.update_one({"id": ObjectId(user_id)})
    return {"user_data": list(user)}


@user_app.put("/users/{user_id}/{role_change}", response_model=User)
async def update_user_data(user_id: str, role_change: str):
    res_data = user_Collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": role_change}})
    return f"{res_data} update is done"
