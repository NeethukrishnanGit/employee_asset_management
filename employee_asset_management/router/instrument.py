from fastapi import APIRouter, status, Body
from pydantic import json
from employee_asset_management.db_creator import Instrument_Collection
from bson.objectid import ObjectId
from employee_asset_management.model.instrument import Instruments
from typing import Dict

json.ENCODERS_BY_TYPE[ObjectId] = str

instrument_app = APIRouter()


@instrument_app.post(
    "/get_instrument/",
    description="**To get An Instrument details specify the requirements inside the response body**",
    status_code=status.HTTP_302_FOUND
)
async def get_instrument(search: Dict):
    data = Instrument_Collection.find(search)
    return {"data": list(data)}


@instrument_app.delete("/")
async def delete_instrument(instrument_id: str = Body(..., embed=True)):
    try:
        query = {"_id": ObjectId(instrument_id)}
        Instrument_Collection.find_one_and_delete(query)
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
    result = Instrument_Collection.insert_one(data_dict)
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
    Instrument_Collection.update_one(query, update)
    updated_data = list(Instrument_Collection.find(query))
    return {"updated_data": updated_data}

