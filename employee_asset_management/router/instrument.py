from fastapi import APIRouter
from pydantic import json
from employee_asset_management.db_creator import Instrument_Collection
from bson.objectid import ObjectId
from employee_asset_management.model.instrument import Instruments

json.ENCODERS_BY_TYPE[ObjectId] = str

instrument_app = APIRouter()


@instrument_app.post("/instrument/{instrument_id}")
async def get_instrument(instrument_id: str):
    query = {"_id": ObjectId(instrument_id)}
    data = Instrument_Collection.find(query)
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


@instrument_app.put("/instruments/{instrument_id}/{type_change}", response_model=Instruments)
async def update_instrument_type(instrument_id: str, type_change: str):
    query = {"_id": ObjectId(instrument_id)}
    update = {"$set": {"type": type_change}}
    stored_data = Instrument_Collection.update_one(query, update)

    if stored_data.matched_count:
        return {"message": "update successful"}
    else:
        return {"message": "Data not found"}
