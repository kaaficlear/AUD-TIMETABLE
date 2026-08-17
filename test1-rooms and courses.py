import pymongo
from pymongo.server_api import ServerApi

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

try:
    # 2. Count the data to ensure everything transferred
    room_count = db.rooms.count_documents({})
    course_count = db.courses.count_documents({})
    
    print(f"✅ Connection successful!")
    print(f"📊 DATABASE SUMMARY: Found {room_count} Rooms and {course_count} Courses.\n")
    
    # 3. Fetch and display all Rooms
    print("-" * 40)
    print("ROOMS DATA")
    print("-" * 40)
    rooms = db.rooms.find()
    for room in rooms:
        # Using string formatting to make it look like a neat table
        print(f"Room: {room['room_code']:<25} | Capacity: {room['capacity']}")
        
    # 4. Fetch and display a sample of Courses (first 10)
    print("\n" + "-" * 80)
    print("COURSES DATA (Showing first 200 entries)")
    print("-" * 80)
    courses = db.courses.find().limit(200)
    for course in courses:
        print(f"Sem: {course['semester']} | Code: {course['course_code']:<25} | Name: {course['course_name']}")

except Exception as e:
    print("❌ Failed to fetch data:")
    print(e)
