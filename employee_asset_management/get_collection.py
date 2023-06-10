import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient["employee_asset_management"]
instrument_Collection = mydb["instruments"]
user_Collection = mydb["users"]
audit_trail_Collection = mydb["audit_trail_data"]
