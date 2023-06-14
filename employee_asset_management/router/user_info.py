from fastapi import APIRouter, Body, HTTPException
from pydantic import json
from typing import Dict
from employee_asset_management.get_collection import user_Collection
from employee_asset_management.model.user_info import User
from bson.objectid import ObjectId
from bson.errors import InvalidId


json.ENCODERS_BY_TYPE[ObjectId] = str

user_app = APIRouter()


@user_app.post("/read_user_data")
async def get_user_data(data: Dict):
    """ Endpoint to fetch the user data from the db """
    for i in data.keys():
        if i == "_id":
            data[i] = ObjectId(data[i])
    user = user_Collection.find(data)
    user_data = list(user)
    return {"user_data": user_data}


@user_app.delete("/delete_user_data")
async def delete_user_data(user_id: str = Body(..., embed=True)):
    """ Endpoint to delete the user """
    try:
        data = user_Collection.find_one_and_delete({"_id": ObjectId(user_id)})
        if data is None:
            raise HTTPException(status_code=404, detail="user not found")
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return "Successfully Deleted..."


@user_app.post("/insert_user_data")
async def create_user_data(user: User):
    """ Endpoint to add user """
    user_data = user.dict()
    new_user = user_Collection.insert_one(user_data)
    return {"_id": str(new_user.inserted_id), **user_data}


@user_app.put("/update_user_data")
async def update_user_data(user_id: str = Body(...), role_change: str = Body(...)):
    """ Endpoint to update user data """
    try:
        id_doc = {"_id": ObjectId(user_id)}
        set_doc = {"$set": {"role": role_change}}
        data = user_Collection.update_one(id_doc, set_doc)
        if data.matched_count:
            updated_data = list(user_Collection.find(id_doc))
            return {"updated data": updated_data}
        else:
            raise HTTPException(status_code=404, detail="user not found")
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=str(e))
