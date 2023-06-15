from fastapi import APIRouter, Body, HTTPException
from pydantic import json
from typing import Dict
from bson.objectid import ObjectId
from bson.errors import InvalidId
from employee_asset_management.get_collection import audit_trail_Collection, instrument_Collection, user_Collection
from employee_asset_management.model.audit_trial import Audit

json.ENCODERS_BY_TYPE[ObjectId] = str
audit_app = APIRouter()


@audit_app.post("/read_audit_trail_data")
async def read_audit_trail_data(value: Dict):
    """Endpoint to fetch the audit trail data from the db"""
    try:
        for i in value.keys():
            if i in ["_id", "user_id", "instrument_id"]:
                value[i] = ObjectId(value[i])
            if i == "event_type":
                if value[i] not in ["check_out", "check_in"]:
                    return "Invalid Event type..."
        data = list(audit_trail_Collection.find(value))
        return {"audit_data": data}
    except InvalidId:
        return "Invalid entry... "


@audit_app.delete("/delete_audit_trail_data")
async def delete_audit_trail_data(audit_id: str = Body(..., embed=True)):
    """Endpoint to delete the audit_trail_data"""
    try:
        result = audit_trail_Collection.find_one_and_delete({"_id": ObjectId(audit_id)})
        if result:
            return "---Deleted Successfully---"
        else:
            raise HTTPException(status_code=404, detail="audit trail data id not found...")
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=str(e))


@audit_app.post("/insert_audit_trail_data", status_code=201)
async def insert_audit_trail_data(given_value: Audit):
    """Endpoint to add an audit trail data"""
    try:
        given_value.user_id = ObjectId(given_value.user_id)
        given_value.instrument_id = ObjectId(given_value.instrument_id)
        if {"_id": given_value.user_id} in list(user_Collection.find({}, {"_id": True})):
            if {"_id": given_value.instrument_id} in list(instrument_Collection.find({}, {"_id": True})):
                if given_value.event_type in ["check_out", "check_in"]:
                    data = given_value.dict()
                    result = audit_trail_Collection.insert_one(data)
                    return {"_id": result.inserted_id, **data}
                else:
                    return "Insertion Failed--->Enter valid event_type"
            else:
                return "Insertion Failed--->Enter valid instrument_id"
        else:
            return "Insertion Failed--->Enter valid user_id"
    except InvalidId as e:
        raise HTTPException(status_code=400, detail=str(e))


@audit_app.post("/checked_out_instruments")
async def get_checked_out_instruments(user_id: str = Body(..., embed=True)):
    """Endpoint that displays the instruments that are checked out by a specific employee"""
    try:
        if {"_id": ObjectId(user_id)} in list(user_Collection.find({}, {"_id": True})):
            find_query = {"user_id": ObjectId(user_id), "event_type": "check_out"}
            find_data = {"_id": False, "instrument_id": True}
            data = list(audit_trail_Collection.find(find_query, find_data))
            available_instruments = [{"_id": ObjectId(instrument["instrument_id"])} for instrument in data]
            get_query = {"$or": available_instruments}
            find_instruments = list(instrument_Collection.find(get_query))
            return {"checked out instruments": find_instruments}
        else:
            raise HTTPException(status_code=404, detail="user id not exist...")
    except InvalidId as e1:
        raise HTTPException(status_code=400, detail=str(e1))
