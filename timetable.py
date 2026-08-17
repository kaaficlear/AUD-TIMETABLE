from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 1. Paste your connection string here. 
# Make sure to replace <username> and <password> with your actual database credentials!
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?appName=timetable"

# 2. Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# 3. Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Success, Priyansh! You are successfully connected to MongoDB Atlas!")
    
    # Let's go ahead and create your timetable database and a test collection
    db = client['timetable_db']
    courses_collection = db['courses']
    
    # Insert a quick test document
    test_course = {
        "course_code": "EN216",
        "course_name": "Introduction to Research Methods",
        "semester": 7
    }
    
    # Uncomment the line below to actually insert the data
    # courses_collection.insert_one(test_course)
    # print("✅ Test course inserted successfully!")

except Exception as e:
    print("❌ Uh oh, something went wrong:")
    print(e)
