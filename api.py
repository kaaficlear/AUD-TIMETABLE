from fastapi import FastAPI, Query
import pymongo
from pymongo.server_api import ServerApi
from datetime import datetime

app = FastAPI()

# Connect to your MongoDB cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

@app.get("/")
def home():
    return {"message": "Campus Timetable API is LIVE!"}

@app.get("/schedule")
def get_full_schedule():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "courses",             
                    "localField": "course_code",   
                    "foreignField": "course_code", 
                    "as": "course_info"            
                }
            },
            {
                "$unwind": {
                    "path": "$course_info",
                    "preserveNullAndEmptyArrays": True 
                }
            },
            {
                "$addFields": {
                    "course_name": "$course_info.course_name",
                    # --- NEW: Grab the semester from the joined course data ---
                    # NOTE: If your courses collection uses 'sem' instead of 'semester', change it here!
                    "semester": "$course_info.semester" 
                }
            },
            {
                "$project": {
                    "_id": 0,             
                    "course_info": 0      
                }
            }
        ]

        schedule_data = list(db.schedule.aggregate(pipeline))
        return {"status": "success", "total_classes": len(schedule_data), "data": schedule_data}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def is_time_in_slot(check_time_str, start_time_str, end_time_str):
    try:
        fmt = "%I:%M %p" 
        check_time = datetime.strptime(check_time_str, fmt).time()
        start_time = datetime.strptime(start_time_str, fmt).time()
        end_time = datetime.strptime(end_time_str, fmt).time()
        return start_time <= check_time <= end_time
    except ValueError:
        return False

@app.get("/rooms/empty")
def get_empty_rooms(day: str = Query(...), time: str = Query(...)):
    try:
        all_rooms = db.schedule.distinct("room_code")
        all_rooms = [room for room in all_rooms if room and str(room).strip()]

        todays_classes = list(db.schedule.find({"day_of_week": day}, {"_id": 0}))

        busy_rooms = set()

        for cls in todays_classes:
            time_slot = cls.get("time_slot")
            if time_slot and isinstance(time_slot, dict):
                start = time_slot.get("start_time")
                end = time_slot.get("end_time")
                room = cls.get("room_code")
                
                if start and end and room:
                    if is_time_in_slot(time, start, end):
                        busy_rooms.add(room)

        empty_rooms = [room for room in all_rooms if room not in busy_rooms]
        empty_rooms.sort()

        return {
            "status": "success", 
            "day_checked": day,
            "time_checked": time,
            "total_empty": len(empty_rooms),
            "data": empty_rooms
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
