from fastapi import APIRouter, status, Body, HTTPException
from pydantic import json
from employee_asset_management.get_collection import instrument_Collection, audit_trail_Collection, user_Collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from employee_asset_management.model.instrument import Instruments
from typing import Dict
from datetime import datetime

json.ENCODERS_BY_TYPE[ObjectId] = str

instrument_app = APIRouter()


@instrument_app.post(
    "/get_instrument",
    description="**To get An Instrument details specify the requirements inside the response body**"
)
async def get_instrument(search: Dict):
    for key, value in search.items():
        if key == "_id":
            search.update({key: ObjectId(search[key])})
    data = instrument_Collection.find(search)
    return {"data": list(data)}


@instrument_app.delete("/delete_one_instrument")
async def delete_one_instrument(instrument_id: str = Body(..., embed=True)):
    try:
        query = {"_id": ObjectId(instrument_id)}
        result = instrument_Collection.find_one_and_delete(query)
        if result is None:
            raise HTTPException(status_code=404, detail="instrument not found")
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    else:
        return "SUCCESSFULLY DELETED !!!"


@instrument_app.post(
    "/add_one_instrument",
    response_model=Instruments,
    status_code=status.HTTP_201_CREATED,
    response_description="**instrument is added**"
)
async def add_one_instrument(instrument: Instruments):
    data_dict = instrument.dict()
    result = instrument_Collection.insert_one(data_dict)
    return {"id": str(result.inserted_id), **data_dict}


@instrument_app.put(
    "/update_one_instrument",
    status_code=status.HTTP_200_OK,
    response_description="UPDATE SUCCESSFUL"
)
async def update_one_instrument(*,
                                instrument_id: str = Body(...),
                                update_data: Dict
                                ):
    try:
        query = {"_id": ObjectId(instrument_id)}
        update = {"$set": update_data}
        result = instrument_Collection.update_one(query, update)
        if result.matched_count:
            updated_data = list(instrument_Collection.find(query))
            return {"updated_data": updated_data}
        else:
            raise HTTPException(status_code=404, detail="instrument not found")

    except InvalidId as e:
        raise HTTPException(status_code=400, detail=f"{e}")


def get_one_instrument(instrument_id: str):
    query = {"_id": ObjectId(instrument_id)}
    data = instrument_Collection.find(query)
    return list(data)


@instrument_app.post("/check_in_instrument")
async def check_in_instrument(user_id: str, instrument_id: str):
    try:
        instrument_query = {"_id": ObjectId(instrument_id)}
        instrument_update = {"$set": {"availability": True,
                                      "check_in": datetime.now(),
                                      "check_out": (datetime(2000, 1, 1, 00, 00, 00))}}

        instrument_Collection.update_one(instrument_query, instrument_update)
        #user_id check
        user_id_check = user_Collection.find_one({"_id":ObjectId(user_id)})
        if not user_id_check:
            raise Exception("user id is invalid")
        audit_trail_value = {
            "user_id": ObjectId(user_id),
            "instrument_id": ObjectId(instrument_id),
            "event_type": "check_in",
            "time": datetime.now()
        }
        audit_trail_Collection.insert_one(audit_trail_value)
        data = get_one_instrument(instrument_id)
        if not data:
            raise Exception("instrument id is invalid")

        return {"checked_in_instrument": data}

    except Exception as e:
        return str(e)


@instrument_app.post("/check_out_instrument")
async def check_out_instrument(user_id: str, instrument_id: str):
    instrument_query = {"_id": ObjectId(instrument_id)}
    instrument_update = {"$set": {"availability": False,
                                  "check_in": (datetime(2000, 1, 1, 00, 00, 00)),
                                  "check_out": datetime.now()}}

    instrument_Collection.update_one(instrument_query, instrument_update)
    audit_trail_value = {
        "user_id": ObjectId(user_id),
        "instrument_id": ObjectId(instrument_id),
        "event_type": "check_out",
        "time": datetime.now()
    }
    audit_trail_Collection.insert_one(audit_trail_value)
    data = get_one_instrument(instrument_id)
    return {"checked_out_instrument": data}


@instrument_app.post("/available_instruments")
async def check_available_instruments():
    data = instrument_Collection.find({"availability": True})
    return {"instruments_available": list(data)}
