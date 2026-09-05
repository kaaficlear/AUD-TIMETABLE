from fastapi import FastAPI, Query
import pymongo
from pymongo.server_api import ServerApi
from datetime import datetime
from pydantic import BaseModel
import razorpay
import hmac
import hashlib

app = FastAPI()

# Connect to MongoDB cluster[cite: 9]
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1')) #[cite: 9]
db = client['timetable_db'] #[cite: 9]

# --- RAZORPAY CONFIGURATION ---
# Replace with your test keys from https://dashboard.razorpay.com/app/keys
RAZORPAY_KEY_ID = "rzp_test_YourKeyIDHere"
RAZORPAY_KEY_SECRET = "YourKeySecretHere"

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# --- DATA MODELS ---
class UserAuth(BaseModel): #[cite: 9]
    uid: str #[cite: 9]
    email: str #[cite: 9]

class UserProfileUpdate(BaseModel): #[cite: 9]
    uid: str #[cite: 9]
    username: str #[cite: 9]
    dob: str #[cite: 9]
    gender: str #[cite: 9]
    university: str #[cite: 9]
    course: str #[cite: 9]
    year: str #[cite: 9]

class PasswordResetVerify(BaseModel): #[cite: 9]
    email: str #[cite: 9]
    username: str #[cite: 9]
    dob: str #[cite: 9]

class AvatarUpdate(BaseModel): #[cite: 9]
    uid: str #[cite: 9]
    profile_pic: str #[cite: 9]

class PremiumRestoreRequest(BaseModel): #[cite: 9]
    uid: str #[cite: 9]

class CreateOrderRequest(BaseModel):
    uid: str
    plan: str
    amount: int  # Amount in paise (₹29 = 2900, ₹49 = 4900, ₹89 = 8900)

class VerifyPaymentRequest(BaseModel):
    uid: str
    plan: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

# --- TIMETABLE ENDPOINTS ---
@app.get("/") #[cite: 9]
def home(): #[cite: 9]
    return {"message": "Campus Timetable API is LIVE!"} #[cite: 9]

@app.get("/version") #[cite: 9]
def get_app_version(): #[cite: 9]
    return { #[cite: 9]
        "status": "success", #[cite: 9]
        "latest_version": "1.0", #[cite: 9]
        "download_url": "https://github.com/kaaficlear/AUD-TIMETABLE/releases" #[cite: 9]
    } #[cite: 9]

@app.get("/schedule") #[cite: 9]
def get_full_schedule(): #[cite: 9]
    try: #[cite: 9]
        pipeline = [ #[cite: 9]
            {"$lookup": {"from": "courses", "localField": "course_code", "foreignField": "course_code", "as": "course_info"}}, #[cite: 9]
            {"$unwind": {"path": "$course_info", "preserveNullAndEmptyArrays": True}}, #[cite: 9]
            {"$addFields": {"course_name": "$course_info.course_name", "semester": "$course_info.semester"}}, #[cite: 9]
            {"$project": {"_id": 0, "course_info": 0}} #[cite: 9]
        ] #[cite: 9]
        schedule_data = list(db.schedule.aggregate(pipeline)) #[cite: 9]
        return {"status": "success", "total_classes": len(schedule_data), "data": schedule_data} #[cite: 9]
    except Exception as e: #[cite: 9]
        return {"status": "error", "message": str(e)} #[cite: 9]

def is_time_in_slot(check_time_str, start_time_str, end_time_str): #[cite: 9]
    try: #[cite: 9]
        fmt = "%I:%M %p" #[cite: 9]
        check_time = datetime.strptime(check_time_str, fmt).time() #[cite: 9]
        start_time = datetime.strptime(start_time_str, fmt).time() #[cite: 9]
        end_time = datetime.strptime(end_time_str, fmt).time() #[cite: 9]
        return start_time <= check_time <= end_time #[cite: 9]
    except ValueError: #[cite: 9]
        return False #[cite: 9]

@app.get("/rooms/empty") #[cite: 9]
def get_empty_rooms(day: str = Query(...), time: str = Query(...)): #[cite: 9]
    try: #[cite: 9]
        all_rooms = db.schedule.distinct("room_code") #[cite: 9]
        all_rooms = [room for room in all_rooms if room and str(room).strip()] #[cite: 9]
        todays_classes = list(db.schedule.find({"day_of_week": day}, {"_id": 0})) #[cite: 9]
        busy_rooms = set() #[cite: 9]

        for cls in todays_classes: #[cite: 9]
            time_slot = cls.get("time_slot") #[cite: 9]
            if time_slot and isinstance(time_slot, dict): #[cite: 9]
                start = time_slot.get("start_time") #[cite: 9]
                end = time_slot.get("end_time") #[cite: 9]
                room = cls.get("room_code") #[cite: 9]
                if start and end and room and is_time_in_slot(time, start, end): #[cite: 9]
                    busy_rooms.add(room) #[cite: 9]

        empty_rooms = [room for room in all_rooms if room not in busy_rooms] #[cite: 9]
        empty_rooms.sort() #[cite: 9]
        return {"status": "success", "day_checked": day, "time_checked": time, "total_empty": len(empty_rooms), "data": empty_rooms} #[cite: 9]
    except Exception as e: #[cite: 9]
        return {"status": "error", "message": str(e)} #[cite: 9]

# --- USER & AUTH ENDPOINTS ---
@app.post("/users/sync") #[cite: 9]
async def sync_user(user: UserAuth): #[cite: 9]
    existing_user = db.users.find_one({"uid": user.uid}) #[cite: 9]
    if existing_user: #[cite: 9]
        return { #[cite: 9]
            "message": "User exists", #[cite: 9]
            "is_premium": existing_user.get("is_premium", False), #[cite: 9]
            "profile_completed": existing_user.get("profile_completed", False), #[cite: 9]
            "university": existing_user.get("university", ""), #[cite: 9]
            "username": existing_user.get("username", ""), #[cite: 9]
            "profile_pic": existing_user.get("profile_pic", "") #[cite: 9]
        } #[cite: 9]
    
    new_user = { #[cite: 9]
        "uid": user.uid, #[cite: 9]
        "email": user.email, #[cite: 9]
        "is_premium": False, #[cite: 9]
        "profile_completed": False, #[cite: 9]
        "university": "", #[cite: 9]
        "username": "", #[cite: 9]
        "profile_pic": "" #[cite: 9]
    } #[cite: 9]
    db.users.insert_one(new_user) #[cite: 9]
    return {"message": "New user registered", "is_premium": False, "profile_completed": False, "university": "", "username": "", "profile_pic": ""} #[cite: 9]

@app.get("/users/check-username") #[cite: 9]
def check_username(username: str = Query(...)): #[cite: 9]
    clean_username = username.strip().lower() #[cite: 9]
    if not clean_username: #[cite: 9]
        return {"available": False, "message": "Username cannot be empty"} #[cite: 9]
        
    existing_user = db.users.find_one({"username": {"$regex": f"^{clean_username}$", "$options": "i"}}) #[cite: 9]
    return {"available": existing_user is None} #[cite: 9]

@app.post("/users/update-profile") #[cite: 9]
def update_profile(profile: UserProfileUpdate): #[cite: 9]
    clean_username = profile.username.strip() #[cite: 9]
    
    existing = db.users.find_one({ #[cite: 9]
        "username": {"$regex": f"^{clean_username}$", "$options": "i"}, #[cite: 9]
        "uid": {"$ne": profile.uid} #[cite: 9]
    }) #[cite: 9]
    
    if existing: #[cite: 9]
        return {"status": "error", "message": "Username already taken by another account"} #[cite: 9]

    db.users.update_one( #[cite: 9]
        {"uid": profile.uid}, #[cite: 9]
        {"$set": { #[cite: 9]
            "username": clean_username, #[cite: 9]
            "dob": profile.dob, #[cite: 9]
            "gender": profile.gender, #[cite: 9]
            "university": profile.university, #[cite: 9]
            "course": profile.course, #[cite: 9]
            "year": profile.year, #[cite: 9]
            "profile_completed": True #[cite: 9]
        }} #[cite: 9]
    ) #[cite: 9]
    return {"status": "success"} #[cite: 9]

@app.post("/users/update-avatar") #[cite: 9]
def update_avatar(data: AvatarUpdate): #[cite: 9]
    db.users.update_one( #[cite: 9]
        {"uid": data.uid}, #[cite: 9]
        {"$set": {"profile_pic": data.profile_pic}} #[cite: 9]
    ) #[cite: 9]
    return {"status": "success"} #[cite: 9]

@app.post("/users/verify-reset") #[cite: 9]
def verify_reset(data: PasswordResetVerify): #[cite: 9]
    user = db.users.find_one({"email": data.email}) #[cite: 9]
    if not user: #[cite: 9]
        return {"status": "error", "message": "Email not found in database."} #[cite: 9]

    db_username = user.get("username", "").lower() #[cite: 9]
    db_dob = user.get("dob", "") #[cite: 9]

    if db_username == data.username.lower() and db_dob == data.dob: #[cite: 9]
        return {"status": "success"} #[cite: 9]
    else: #[cite: 9]
        return {"status": "error", "message": "Security details do not match."} #[cite: 9]

# --- REAL PAYMENT GATEWAY (RAZORPAY) ENDPOINTS ---

@app.post("/premium/create-order")
def create_order(data: CreateOrderRequest):
    try:
        order_data = {
            "amount": data.amount,
            "currency": "INR",
            "receipt": f"rcpt_{data.uid[:8]}_{int(datetime.utcnow().timestamp())}",
            "notes": {
                "uid": data.uid,
                "plan": data.plan
            }
        }
        order = razorpay_client.order.create(data=order_data)
        return {
            "status": "success",
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": RAZORPAY_KEY_ID
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/premium/verify-payment")
def verify_payment(data: VerifyPaymentRequest):
    try:
        # Cryptographically verify that the payment was made to Razorpay
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != data.razorpay_signature:
            return {"status": "error", "message": "Signature mismatch. Fraudulent payment detected."}

        # Payment verified: update user Pro tier in MongoDB
        result = db.users.update_one(
            {"uid": data.uid},
            {"$set": {
                "is_premium": True,
                "premium_plan": data.plan,
                "payment_id": data.razorpay_payment_id,
                "upgraded_at": datetime.utcnow().isoformat()
            }}
        )

        if result.matched_count == 0:
            return {"status": "error", "message": "User not found in database."}

        return {"status": "success", "message": f"Verified! Activated {data.plan} plan."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/premium/restore") #[cite: 9]
def restore_premium(data: PremiumRestoreRequest): #[cite: 9]
    user = db.users.find_one({"uid": data.uid}) #[cite: 9]
    if user and user.get("is_premium", False): #[cite: 9]
        return { #[cite: 9]
            "status": "success", #[cite: 9]
            "is_premium": True, #[cite: 9]
            "plan": user.get("premium_plan", "Semester Pass") #[cite: 9]
        } #[cite: 9]
    return {"status": "not_found", "is_premium": False} #[cite: 9]