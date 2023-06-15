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
    "/get_instrument"
)
async def get_instrument(search: Dict):
    """Endpoint to fetch an instrument from the db"""
    for key, value in search.items():
        if key == "_id":
            search.update({key: ObjectId(search[key])})
    data = instrument_Collection.find(search)
    return {"data": list(data)}


@instrument_app.delete("/delete_one_instrument")
async def delete_one_instrument(instrument_id: str = Body(..., embed=True)):
    """Endpoint to delete the instruments"""
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
    status_code=status.HTTP_201_CREATED
)
async def add_one_instrument(instrument: Instruments):
    """Endpoint to add instruments"""
    names = [i["name"] for i in instrument_Collection.find({}, {"_id": 0, "name": 1})]
    data_dict = instrument.dict()
    if instrument.name in names:
        return {"error": "instrument name is already taken!!!, try a different name"}
    else:
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
    """Endpoint to update the instrument data"""
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


# function to retrieve instrument based on instrument id
def get_one_instrument(instrument_id: str):
    query = {"_id": ObjectId(instrument_id)}
    data = instrument_Collection.find(query)
    return list(data)


async def check_in_instrument(user_id: str, instrument_id: str):
    try:
        # instrument_id check
        instrument_id_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id)})
        if not instrument_id_check:
            raise Exception("instrument id is invalid...")
        # user_id check
        user_id_check = user_Collection.find_one({"_id": ObjectId(user_id)})
        if not user_id_check:
            raise Exception("user id is invalid...")
        availability_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id), "availability": False})
        if not availability_check:
            return {
                "checked_in_instrument": [{"_id": instrument_id, "check_in": "instrument is already checked_in"}]}
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
        data = get_one_instrument(instrument_id)
        return {"checked_in_instrument": data}
    except Exception as e:
        return str(e)


async def check_out_instrument(user_id: str, instrument_id: str):
    try:
        # user_id check
        user_id_check = user_Collection.find_one({"_id": ObjectId(user_id)})
        if not user_id_check:
            raise Exception("user id is invalid...")
        # instrument_id check
        instrument_id_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id)})
        if not instrument_id_check:
            raise Exception("instrument id is invalid...")
        availability_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id), "availability": True})
        if not availability_check:
            return {
                "checked_out_instrument": [{"_id": instrument_id, "check_out": "instrument is already checked_out"}]}
        instrument_query = {"_id": ObjectId(instrument_id)}
        instrument_update = {"$set": {"availability": False,
                                      "check_in": (datetime(2000, 1, 1, 00, 00, 00)),
                                      "check_out": datetime.now()}}
        instrument_Collection.update_one(instrument_query, instrument_update)
        audit_trail_value = {
            "user_id": ObjectId(user_id),
            "instrument_id": ObjectId(instrument_id),
            "event_type": "check_out",
            "time": datetime.now()}
        audit_trail_Collection.insert_one(audit_trail_value)
        data = get_one_instrument(instrument_id)
        return {"checked_out_instrument": data}
    except Exception as e:
        return str(e)


@instrument_app.post("/available_instruments")
async def check_available_instruments():
    """Endpoint to instruments available at present in the inventory"""
    data = instrument_Collection.find({"availability": True})
    return {"instruments_available": list(data)}


@instrument_app.post("/check_out_instruments",
                     description="Enter multiple instruments inside the instruments_list to check_out")
async def check_out_instruments(
        *,
        user_id: str = Body(..., embed=True),
        instruments_list: list = Body(...)):
    """ Endpoint to check_out multiple instruments """
    invalid_instruments = []
    for instrument_id in instruments_list:
        try:
            instrument_id_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id)})
            if not instrument_id_check:
                instruments_list.remove(instrument_id)
                invalid_instruments.append(instrument_id)
        except InvalidId:
            instruments_list.remove(instrument_id)
            invalid_instruments.append(instrument_id)

    instruments = [await check_out_instrument(user_id, instrument) for instrument in instruments_list]
    already_checked_out = []
    check_out_list = []
    for check_out in instruments:
        check = check_out["checked_out_instrument"][0]
        if check["check_out"] == "instrument is already checked_out":
            already_checked_out.append(check)
        else:
            check_out_list.append(check)
    check_outs = {}
    if check_out_list:
        check_outs.update({"multiple_checkouts": check_out_list})
    if already_checked_out:
        check_outs.update({"already_checked_out": already_checked_out})
    if invalid_instruments:
        check_outs.update({"invalid_instruments": invalid_instruments})

    return check_outs


@instrument_app.post("/check_in_instruments",
                     description="Enter multiple instruments inside the instruments_list to check_in")
async def check_in_instruments(
        *,
        user_id: str = Body(..., embed=True),
        instruments_list: list = Body(...)):
    """ Endpoint to check_in multiple instruments """
    invalid_instruments = []
    for instrument_id in instruments_list:
        try:
            instrument_id_check = instrument_Collection.find_one({"_id": ObjectId(instrument_id)})
            if not instrument_id_check:
                instruments_list.remove(instrument_id)
                invalid_instruments.append(instrument_id)
        except InvalidId:
            instruments_list.remove(instrument_id)
            invalid_instruments.append(instrument_id)

    instruments = [await check_in_instrument(user_id, instrument) for instrument in instruments_list]
    already_checked_in = []
    check_in_list = []
    for check_in in instruments:
        check = check_in["checked_in_instrument"][0]
        print(check)
        if check["check_in"] == "instrument is already checked_in":
            already_checked_in.append(check)
        else:
            check_in_list.append(check)
    check_ins = {}
    if check_in_list:
        check_ins.update({"multiple_checkins": check_in_list})
    if already_checked_in:
        check_ins.update({"already_checked_in": already_checked_in})
    if invalid_instruments:
        check_ins.update({"invalid_instruments": invalid_instruments})

    return check_ins


@instrument_app.post("/check_out_status")
async def check_out_status():
    instruments = instrument_Collection.find()
    status_data = []
    for i in instruments:
        if not i["availability"]:
            audit = audit_trail_Collection.find({"instrument_id": ObjectId(i["_id"]), "event_type": "check_out"})
            audit_data = list(audit)
            for data in audit_data:
                i.update({"check_out_status": "True", "check_out_by": data['user_id'], "check_out_time": data["time"]})
            status_data.append(i)
    return {"status_data": status_data}
