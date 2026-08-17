import pymongo
from pymongo.server_api import ServerApi

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

try:
    # 2. Fetch the schedule data
    print("Fetching your weekly schedule grid...\n")
    print("-" * 60)
    
    # We will sort it by day_of_week just to keep it organized
    # (Though MongoDB stores them in the order they were inserted anyway)
    weekly_schedule = db.schedule.find()
    
    current_day = ""
    
    # 3. Loop through and print nicely
    for block in weekly_schedule:
        # Print a header for each new day
        if block['day_of_week'] != current_day:
            current_day = block['day_of_week']
            print(f"\n📍 {current_day.upper()}")
            print("-" * 60)
            
        time = block['time_slot']
        
        # Display the formatted data
        print(f"{time['slot_name']:<8} | {time['start_time']:<8} to {time['end_time']:<8} | Room: {block['room_code']} | Course: {block['course_code']}")
        
except Exception as e:
    print("❌ Failed to fetch data:")
    print(e)
