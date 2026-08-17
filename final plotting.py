import pymongo
from pymongo.server_api import ServerApi
import sys

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
db = client['timetable_db']

# 2. Fetch reference data directly from your database!
# We sort them alphabetically so they are easy to find in the menu
rooms_data = list(db.rooms.find({}, {"_id": 0, "room_code": 1}).sort("room_code", 1))
courses_data = list(db.courses.find({}, {"_id": 0, "course_code": 1, "semester": 1}).sort("course_code", 1))

# Extract just the codes into clean lists
room_list = [r["room_code"] for r in rooms_data]
semesters_list = sorted(list(set(c["semester"] for c in courses_data)))

# 3. Define the static menus
days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
slots_list = [
    "Slot 1 (9:00 AM - 11:00 AM)", 
    "Slot 2 (11:00 AM - 1:00 PM)", 
    "Slot 3 (1:30 PM - 3:30 PM)", 
    "Slot 4 (3:30 PM - 5:30 PM)"
]
sections_list = ["A", "B", "C", "D", "None (No Section)"]

# Helper dictionary to map the chosen slot string back to the database format
times_mapping = {
    "Slot 1 (9:00 AM - 11:00 AM)": {"start_time": "9:00 AM", "end_time": "11:00 AM", "slot_name": "Slot 1"},
    "Slot 2 (11:00 AM - 1:00 PM)": {"start_time": "11:00 AM", "end_time": "1:00 PM", "slot_name": "Slot 2"},
    "Slot 3 (1:30 PM - 3:30 PM)": {"start_time": "1:30 PM", "end_time": "3:30 PM", "slot_name": "Slot 3"},
    "Slot 4 (3:30 PM - 5:30 PM)": {"start_time": "3:30 PM", "end_time": "5:30 PM", "slot_name": "Slot 4"}
}

# 4. Helper function to create a numbered menu automatically
def select_from_menu(title, options):
    print(f"\n--- {title} ---")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    print("0. Quit")
    
    while True:
        choice = input(f"Enter number (0-{len(options)}): ").strip()
        if choice == '0':
            print("\n👋 Data entry session closed. Great work!")
            sys.exit()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(options):
                return options[choice_idx]
        except ValueError:
            pass
        print("❌ Invalid selection. Please enter a valid number.")

# 5. Main Interactive Loop
print("=======================================")
print(" 🗓️ MENU-DRIVEN DATA ENTRY TERMINAL 🗓️")
print("=======================================")

while True:
    print("\n" + "=" * 40)
    print(" 🆕 ADDING NEW CLASS SCHEDULE")
    print("=" * 40)
    
    # Step A: Pick Day & Slot
    selected_day = select_from_menu("Select Day", days_list)
    selected_slot_str = select_from_menu("Select Time Slot", slots_list)
    
    # Step B: Pick Room
    selected_room = select_from_menu("Select Room", room_list)
    
    # Step C: Pick Course (Filtered by Semester for ease of use)
    selected_sem = select_from_menu("Filter Courses by Semester", semesters_list)
    
    # Filter the courses list based on the chosen semester
    filtered_courses = [c["course_code"] for c in courses_data if c["semester"] == selected_sem]
    selected_course = select_from_menu(f"Select Semester {selected_sem} Course", filtered_courses)
    
    # Step D: Pick Section
    selected_section = select_from_menu("Select Section", sections_list)
    if selected_section == "None (No Section)":
        selected_section = None
        
    # 6. Construct and Insert Document
    class_document = {
        "day_of_week": selected_day,
        "time_slot": times_mapping[selected_slot_str],
        "room_code": selected_room,
        "course_code": selected_course,
        "section": selected_section
    }
    
    try:
        db.schedule.insert_one(class_document)
        sec_text = f" (Sec {selected_section})" if selected_section else ""
        print(f"\n✅ SUCCESS: Plotted {selected_course}{sec_text} in {selected_room} on {selected_day} ({times_mapping[selected_slot_str]['slot_name']})!")
    except Exception as e:
        print("\n❌ Failed to insert data:")
        print(e)
