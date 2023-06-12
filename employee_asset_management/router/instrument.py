from fastapi import APIRouter, status, Body
from pydantic import json
from employee_asset_management.get_collection import instrument_Collection, audit_trail_Collection
from bson.objectid import ObjectId
from employee_asset_management.model.instrument import Instruments
from typing import Dict
from datetime import datetime

json.ENCODERS_BY_TYPE[ObjectId] = str

instrument_app = APIRouter()


@instrument_app.post(
    "/get_instrument/",
    description="**To get An Instrument details specify the requirements inside the response body**",
    status_code=status.HTTP_302_FOUND
)
async def get_instrument(search: Dict):
    data = instrument_Collection.find(search)
    return {"data": list(data)}


@instrument_app.delete("/")
async def delete_instrument(instrument_id: str = Body(..., embed=True)):
    try:
        query = {"_id": ObjectId(instrument_id)}
        instrument_Collection.find_one_and_delete(query)
    except:
        return "Failed to delete"
    else:
        return "SUCCESSFULLY DELETED !!!"


@instrument_app.post(
    "/",
    response_model=Instruments,
    status_code=status.HTTP_201_CREATED,
    response_description="**instrument is added**"
)
async def add_instrument(instrument: Instruments):
    data_dict = instrument.dict()
    result = instrument_Collection.insert_one(data_dict)
    return {"id": str(result.inserted_id), **data_dict}


@instrument_app.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="UPDATE SUCCESSFUL"
)
async def update_instrument(*,
                            instrument_id: str = Body(...),
                            update_data: Dict
                            ):
    query = {"_id": ObjectId(instrument_id)}
    update = {"$set": update_data}
    instrument_Collection.update_one(query, update)
    updated_data = list(instrument_Collection.find(query))
    return {"updated_data": updated_data}


async def get_one_instrument(instrument_id: str):
    query = {"_id": ObjectId(instrument_id)}
    return instrument_Collection.find(query)


@instrument_app.post("/check_in_instrument")
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
    data = list(instrument_Collection.find(instrument_query))
    return {"checked_in_instrument": data}


@instrument_app.post("/check_out_instrument")
async def check_out(user_id: str, instrument_id: str):
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
    data = list(instrument_Collection.find(instrument_query))
    return {"checked_out_instrument": data}


@instrument_app.post("/instruments_available")
async def check_available():
    data = instrument_Collection.find({"availability": True})
    return {"instruments_available": list(data)}
