from fastapi import FastAPI, Query
import pymongo
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Connect to MongoDB cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

# --- DATA MODELS ---
class UserAuth(BaseModel):
    uid: str
    email: str

class UserProfileUpdate(BaseModel):
    uid: str
    username: str
    dob: str
    gender: str
    university: str
    course: str
    year: str

class PasswordResetVerify(BaseModel):
    email: str
    username: str
    dob: str

class AvatarUpdate(BaseModel):
    uid: str
    profile_pic: str

class PremiumRestoreRequest(BaseModel):
    uid: str

# --- TIMETABLE ENDPOINTS ---
@app.get("/")
def home():
    return {"message": "Campus Timetable API is LIVE!"}

@app.get("/holidays")
def get_holidays(university: str = Query("Dr. B.R. Ambedkar University Delhi")):
    try:
        # Fetch holidays collection from MongoDB synchronously 
        records = list(db.holidays.find(
            {"university": university},
            {"_id": 0}  # Exclude Mongo internal ID
        ).sort("raw_date", 1))
        
        return {
            "status": "success",
            "data": records
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
            {"$lookup": {"from": "courses", "localField": "course_code", "foreignField": "course_code", "as": "course_info"}},
            {"$unwind": {"path": "$course_info", "preserveNullAndEmptyArrays": True}},
            {"$addFields": {"course_name": "$course_info.course_name", "semester": "$course_info.semester"}},
            {"$project": {"_id": 0, "course_info": 0}}
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
                if start and end and room and is_time_in_slot(time, start, end):
                    busy_rooms.add(room)

        empty_rooms = [room for room in all_rooms if room not in busy_rooms]
        empty_rooms.sort()
        return {"status": "success", "day_checked": day, "time_checked": time, "total_empty": len(empty_rooms), "data": empty_rooms}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- USER & AUTH ENDPOINTS ---
@app.post("/users/sync")
async def sync_user(user: UserAuth):
    existing_user = db.users.find_one({"uid": user.uid})
    if existing_user:
        return {
            "message": "User exists",
            "is_premium": existing_user.get("is_premium", False),
            "profile_completed": existing_user.get("profile_completed", False),
            "university": existing_user.get("university", ""),
            "username": existing_user.get("username", ""),
            "profile_pic": existing_user.get("profile_pic", "")
        }
    
    new_user = {
        "uid": user.uid,
        "email": user.email,
        "is_premium": False,
        "profile_completed": False,
        "university": "",
        "username": "",
        "profile_pic": ""
    }
    db.users.insert_one(new_user)
    return {"message": "New user registered", "is_premium": False, "profile_completed": False, "university": "", "username": "", "profile_pic": ""}

@app.get("/users/check-username")
def check_username(username: str = Query(...)):
    clean_username = username.strip().lower()
    if not clean_username:
        return {"available": False, "message": "Username cannot be empty"}
        
    existing_user = db.users.find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}})
    return {"available": existing_user is None}

@app.post("/users/update-profile")
def update_profile(profile: UserProfileUpdate):
    clean_username = profile.username.strip()
    
    existing = db.users.find_one({
        "username": {"$regex": f"^{clean_username}$", "$options": "i"},
        "uid": {"$ne": profile.uid}
    })
    
    if existing:
        return {"status": "error", "message": "Username already taken by another account"}

    db.users.update_one(
        {"uid": profile.uid},
        {"$set": {
            "username": clean_username,
            "dob": profile.dob,
            "gender": profile.gender,
            "university": profile.university,
            "course": profile.course,
            "year": profile.year,
            "profile_completed": True
        }}
    )
    return {"status": "success"}

@app.post("/users/update-avatar")
def update_avatar(data: AvatarUpdate):
    db.users.update_one(
        {"uid": data.uid},
        {"$set": {"profile_pic": data.profile_pic}}
    )
    return {"status": "success"}

@app.post("/users/verify-reset")
def verify_reset(data: PasswordResetVerify):
    user = db.users.find_one({"email": data.email})
    if not user:
        return {"status": "error", "message": "Email not found in database."}

    db_username = user.get("username", "").lower()
    db_dob = user.get("dob", "")

    if db_username == data.username.lower() and db_dob == data.dob:
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Security details do not match."}

# --- PREMIUM ENDPOINTS (RAZORPAY REMOVED) ---

@app.post("/premium/restore")
def restore_premium(data: PremiumRestoreRequest):
    user = db.users.find_one({"uid": data.uid})
    if user and user.get("is_premium", False):
        return {
            "status": "success",
            "is_premium": True,
            "plan": user.get("premium_plan", "Semester Pass")
        }
    return {"status": "not_found", "is_premium": False}