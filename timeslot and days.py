import pymongo
from pymongo.server_api import ServerApi

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

# 2. Define the exact days and standard time slots in 12-hour format
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

time_slots = [
    {"slot_name": "Slot 1", "start_time": "9:00 AM", "end_time": "11:00 AM"},
    {"slot_name": "Slot 2", "start_time": "11:00 AM", "end_time": "1:00 PM"},
    {"slot_name": "Slot 3", "start_time": "1:30 PM", "end_time": "3:30 PM"},
    {"slot_name": "Slot 4", "start_time": "3:30 PM", "end_time": "5:30 PM"}
]

# 3. Generate the empty weekly grid
schedule_template = []

for day in days_of_week:
    for slot in time_slots:
        schedule_template.append({
            "day_of_week": day,
            "time_slot": slot,
            "room_code": None,   # Leaving this blank to fill in later
            "course_code": None  # Leaving this blank to fill in later
        })

# 4. Clear any existing schedule data to prevent duplicates
db.schedule.drop()

# 5. Insert the 24 empty slots into the database
try:
    print("Pushing the empty weekly schedule grid (12-hour format) to MongoDB Atlas...")
    db.schedule.insert_many(schedule_template)
    print(f"✅ Successfully created {len(schedule_template)} empty time slots (Monday-Saturday) in the 'schedule' collection!")
except Exception as e:
    print("❌ Failed to insert data:")
    print(e)
