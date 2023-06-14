import datetime

import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["employee_asset_management"]

instrument_Collection = mydb["instruments"]

instruments = [
    {
        "name": "prober",
        "type": "A",
        "description": "This is used to test wafer ",
        "availability": True,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "handler",
        "type": "A",
        "description": "This used to test packaged device and place the component for testing",
        "availability": True,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "manipulator",
        "type": "C",
        "description": "This is used to support and tilt the test head",
        "availability": True,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "test head",
        "type": "B",
        "description": "This carries some critical sensitive devices",
        "availability": False,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "tester rack",
        "type": "COMBINED",
        "description": "This contains of bulky instruments",
        "availability": True,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "device interface",
        "type": "COMBINED",
        "description": "This sits on top of the TEST HEAD",
        "availability": True,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    },
    {
        "name": "instrument cards",
        "type": "COMBINED",
        "description": "This is Fixed inside the TEST HEAD",
        "availability": False,
        "check_in": datetime.datetime(2022, 11, 16, 00, 00, 00),
        "check_out": datetime.datetime(2022, 11, 16, 00, 00, 00)
    }
]


instrument_ids = instrument_Collection.insert_many(instruments)

user_Collection = mydb["users"]
user_dict = [
    {
        "user_name": "John",
        "role": "EMPLOYEE"
    },
    {
        "user_name": "Naveen",
        "role": "CUSTOMER"
    },
    {
        "user_name": "Roshan",
        "role": "PARTNER"
    },
    {
        "user_name": "Jessi",
        "role": "EMPLOYEE"
    },
    {
        "user_name": "Ram",
        "role": "CUSTOMER"
    }
]

user_ids = user_Collection.insert_many(user_dict)

audit_trail_Collection = mydb["audit_trail_data"]
audit_dict = [
    {
        "user_id": user_ids.inserted_ids[0],
        "instrument_id": instrument_ids.inserted_ids[0],
        "event_type": "check_out",
        "time": datetime.datetime(2022, 11, 2, 00, 00, 00)
    },
    {
        "user_id": user_ids.inserted_ids[0],
        "instrument_id": instrument_ids.inserted_ids[0],
        "event_type": "check_in",
        "time": datetime.datetime(2022, 11, 2, 00, 00, 00)
    },
    {
        "user_id": user_ids.inserted_ids[1],
        "instrument_id": instrument_ids.inserted_ids[6],
        "event_type": "check_out",
        "time": datetime.datetime(2022, 11, 2, 00, 00, 00)
    },
    {
        "user_id": user_ids.inserted_ids[1],
        "instrument_id": instrument_ids.inserted_ids[2],
        "event_type": "check_in",
        "time": datetime.datetime(2022, 11, 2, 00, 00, 00)
    },
    {
        "user_id": user_ids.inserted_ids[2],
        "instrument_id": instrument_ids.inserted_ids[3],
        "event_type": "check_out",
        "time": datetime.datetime(2022, 11, 2, 00, 00, 00)
    }
]

audit_data = audit_trail_Collection.insert_many(audit_dict)
print(mydb)
