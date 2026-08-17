import pymongo
from pymongo.server_api import ServerApi

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

try:
    print("Updating the schedule grid to support course sections...")
    
    # 2. Update EVERY document in the schedule collection
    # $set adds the new field if it doesn't exist, or updates it if it does
    result = db.schedule.update_many(
        {}, # An empty filter {} means "target all documents"
        {"$set": {"section": None}}
    )
    
    print(f"✅ Success! Modified {result.modified_count} time slots to include the 'section' field.")

except Exception as e:
    print("❌ Failed to update data:")
    print(e)
