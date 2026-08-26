from fastapi import FastAPI, Query
import pymongo
from pymongo.server_api import ServerApi
from datetime import datetime
from pydantic import BaseModel # --- NEW: Import Pydantic for data validation ---

app = FastAPI()

# Connect to your MongoDB cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

# --- NEW: Define what the incoming User data looks like ---
class UserAuth(BaseModel):
    uid: str
    email: str

@app.get("/")
def home():
    return {"message": "Campus Timetable API is LIVE!"}

@app.get("/version")
def get_app_version():
    return {
        "status": "success",
        "latest_version": "1.0", 
        "download_url": "https://github.com/kaaficlear/AUD-TIMETABLE/releases" 
    }

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

# --- NEW: The endpoint to catch new user registrations from Flutter ---
@app.post("/users/sync")
async def sync_user(user: UserAuth):
    # Check if the user already exists in your MongoDB 'users' collection
    existing_user = db.users.find_one({"uid": user.uid})
    
    if existing_user:
        return {
            "message": "User exists", 
            "is_premium": existing_user.get("is_premium", False)
        }
    
    # If it is a new user, create their profile
    new_user = {
        "uid": user.uid,
        "email": user.email,
        "is_premium": False, # Everyone starts on the free tier
    }
    
    db.users.insert_one(new_user)
    return {"message": "New user registered", "is_premium": False}