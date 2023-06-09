from fastapi import APIRouter, status
from pydantic import json
from employee_asset_management.db_creator import Instrument_Collection
from bson.objectid import ObjectId
from employee_asset_management.model.instrument import Instruments
from typing import Dict

json.ENCODERS_BY_TYPE[ObjectId] = str

instrument_app = APIRouter()


@instrument_app.post(
    "/instrument/",
    description="**To get An Instrument details specify the requirements inside the response body**",
    status_code=status.HTTP_302_FOUND
)
async def get_instrument(search: Dict):
    data = Instrument_Collection.find(search)
    return {"data": list(data)}


@instrument_app.delete("/instrument/{instrument_id}")
async def delete_instrument(instrument_id: str):
    query = {"_id": ObjectId(instrument_id)}
    Instrument_Collection.find_one_and_delete(query)
    return "SUCCESSFULLY DELETED !!!"


@instrument_app.post("/add_instrument/", response_model=Instruments)
async def add_instrument(instrument: Instruments):
    data_dict = instrument.dict()
    result = Instrument_Collection.insert_one(data_dict)
    return {"id": str(result.inserted_id), **data_dict}


@instrument_app.put("/instruments/{instrument_id}/")
async def update_instrument_type(instrument_id: str, update_data: Dict):
    query = {"_id": ObjectId(instrument_id)}
    update = {"$set": update_data}
    Instrument_Collection.update_one(query, update)
    updated_data = list(Instrument_Collection.find(query))
    return {"updated_data": updated_data}
