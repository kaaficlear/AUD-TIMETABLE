import pymongo
from pymongo.server_api import ServerApi

# 1. Connect to your cluster
uri = "mongodb+srv://priyanshmaurya:mummypapaM@timetable.yramfud.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# 2. Access the Database
db = client['timetable_db']

# 3. Prepare the Data Dictionaries
courses_data = [
    # Semester 1
    {"course_code": "AEC2 - NSUS1AE001", "course_name": "English for Academic Purposes", "semester": 1},
    {"course_code": "AEC1-NSUS1AE006, AE007", "course_name": "Hindi (Vyaharik / Madhyamik)", "semester": 1},
    {"course_code": "NSUS1SE001", "course_name": "English Proficiency Course", "semester": 1},
    {"course_code": "NSUS1SE002", "course_name": "IT Networking Fundamentals", "semester": 1},
    {"course_code": "NSUS1SE008", "course_name": "IASTN", "semester": 1},
    {"course_code": "NSUS1SE009", "course_name": "YTOM", "semester": 1},
    {"course_code": "NSUS1SE010", "course_name": "CL", "semester": 1},
    {"course_code": "NSUS1SE011", "course_name": "Introduction to C Language", "semester": 1},
    {"course_code": "NSUS1VA001", "course_name": "", "semester": 1},
    {"course_code": "NSUS1VA002", "course_name": "", "semester": 1},
    {"course_code": "NSUS1VA003", "course_name": "", "semester": 1},
    {"course_code": "NSUS1VA004", "course_name": "", "semester": 1},
    {"course_code": "DSC1 - NSUS1PS701", "course_name": "Understanding personality", "semester": 1},
    {"course_code": "DSC2 - NSUS1PS702", "course_name": "Human Cognition", "semester": 1},
    {"course_code": "RSUS1MA501 - DSC", "course_name": "Introduction to Mathematical Thinking", "semester": 1},
    {"course_code": "RSUS1MA502-DSC", "course_name": "Calculus", "semester": 1},
    {"course_code": "RSUS1MA561", "course_name": "Cyber Security", "semester": 1},
    {"course_code": "NSUS1SC819 - DSC", "course_name": "Introduction to Sociological Concepts and Thinkers", "semester": 1},
    {"course_code": "NSUS1SC803 - DSC", "course_name": "Sociology of India", "semester": 1},
    {"course_code": "NSUS1HS401 - DSC", "course_name": "Understanding the Past: Myths, Epics, Chronicles and Histories", "semester": 1},
    {"course_code": "NSUS1HS402", "course_name": "Ancient Societies", "semester": 1},
    {"course_code": "NSUS1EN201: DSC 1", "course_name": "Literatures of the Indian Subcontinent", "semester": 1},
    {"course_code": "NSUS1PO601 - DSC", "course_name": "Understanding Political Theory", "semester": 1},
    {"course_code": "NSUS1PO631 - DSC", "course_name": "Colonialism and Nationalism in India", "semester": 1},
    {"course_code": "NSUS1EC101 - DSC1", "course_name": "Mathematics for Economics", "semester": 1},
    {"course_code": "NSUS1EC102-DSC2", "course_name": "Statistics for Economics", "semester": 1},
    {"course_code": "NSUS1EN202: DSC 2", "course_name": "Understanding Poetry", "semester": 1},
    {"course_code": "ENM001", "course_name": "Language, Learning, and the Learner", "semester": 1},

    # Semester 3
    {"course_code": "SWSUS1SE007", "course_name": "Introduction to Cybersecurity", "semester": 3},
    {"course_code": "NSUS1AE044", "course_name": "Logic & Reasoning", "semester": 3},
    {"course_code": "NSUS1AE009", "course_name": "Environment: Issues and Challenges (EIC)", "semester": 3},
    {"course_code": "NSUS1SE005", "course_name": "Business Communication I", "semester": 3},
    {"course_code": "NSUS1AE047", "course_name": "Hindi Sahitya Itihas ki rooprekha", "semester": 3},
    {"course_code": "NSUS1GE004", "course_name": "Gendered Lives in Performance", "semester": 3},
    {"course_code": "DSC4 - NSUS1PS704", "course_name": "Social Psychology", "semester": 3},
    {"course_code": "DSC5 - NSUS1PS705", "course_name": "Statistics", "semester": 3},
    {"course_code": "DSC6 - NSUS1PS706", "course_name": "Methods in Psychology", "semester": 3},
    {"course_code": "DSC4-NSUS1MA504", "course_name": "Numerical Analysis", "semester": 3},
    {"course_code": "DSC5-NSUS1MA505", "course_name": "Analysis II", "semester": 3},
    {"course_code": "DSC6-NSUS1MA506", "course_name": "Algebra II", "semester": 3},
    {"course_code": "NSUS1SC804 - DSC", "course_name": "Conceptualising Rural and Urban Societies", "semester": 3},
    {"course_code": "NSUS1SC805 - DSC", "course_name": "Marriage, Kinship and Family Forms", "semester": 3},
    {"course_code": "NSUS1SC806 - DSC", "course_name": "Politics, Law and Society", "semester": 3},
    {"course_code": "NSUS1HS404 - DSC", "course_name": "Medieval India 1", "semester": 3},
    {"course_code": "NSUS1HS405 - DSC", "course_name": "Medieval World", "semester": 3},
    {"course_code": "NSUS1HS406 - DSC", "course_name": "Delhi in History", "semester": 3},
    {"course_code": "DSC 4: NSUS1EN204", "course_name": "The Epic", "semester": 3},
    {"course_code": "DSC 5: NSUS1EN205", "course_name": "American Literature", "semester": 3},
    {"course_code": "DSC 6: NSUS1EN206", "course_name": "Introduction to Drama", "semester": 3},
    {"course_code": "NSUS1PO604 -DSC", "course_name": "Western Political Thought", "semester": 3},
    {"course_code": "NSUS1PO605 - DSC", "course_name": "State Politics in India", "semester": 3},
    {"course_code": "NSUS1PO606 - DSC", "course_name": "Comparative Government and Politics", "semester": 3},
    {"course_code": "NSUS1GEPO1 - GE", "course_name": "Globalization and Politics", "semester": 3},
    {"course_code": "NSUS1EC104 -DSC", "course_name": "Statistical Methods for Economics", "semester": 3},
    {"course_code": "NSUS1EC105 -DSC", "course_name": "Microeconomics-1", "semester": 3},
    {"course_code": "NSUS1EC106 - DSC", "course_name": "Macroeconomics-1", "semester": 3},

    # Semester 5
    {"course_code": "NSUS1GE908", "course_name": "Indian History through Literature", "semester": 5},
    {"course_code": "NSUS1GE003", "course_name": "Reading Gendered Power in Dystopia", "semester": 5},
    {"course_code": "NSUS1GE918", "course_name": "Basics of Performance Making", "semester": 5},
    {"course_code": "NSUS1GE304", "course_name": "Sanjhi Sanskriti aur Hindustani Kavita", "semester": 5},
    {"course_code": "DSC10 - NSUS1PS710", "course_name": "Psychology for India", "semester": 5},
    {"course_code": "DSC11 - NSUS1PS711", "course_name": "Clinical Case Study - Practicum", "semester": 5},
    {"course_code": "DSE1 - NSUS1PS731", "course_name": "Psychology in Action", "semester": 5},
    {"course_code": "DSE2 - NSUS1PS732", "course_name": "Neuropsychology", "semester": 5},
    {"course_code": "DSC10-NSUS1MA510", "course_name": "Ordinary Differential Equations", "semester": 5},
    {"course_code": "DSC11-NSUS1MA540", "course_name": "Advanced Analysis", "semester": 5},
    {"course_code": "DSE1-NSUS1MA541", "course_name": "Mathematical Modelling", "semester": 5},
    {"course_code": "NSUS1SC810 - DSC", "course_name": "Sociological Theory-I", "semester": 5},
    {"course_code": "NSUS1SC811 - DSC", "course_name": "Social Movements", "semester": 5},
    {"course_code": "NSUS1SC832 - DSE", "course_name": "Food and Society", "semester": 5},
    {"course_code": "NSUS1SC831 - DSE", "course_name": "Sociology of Work", "semester": 5},
    {"course_code": "NSUS1HS410 - DSC", "course_name": "Modern India", "semester": 5},
    {"course_code": "NSUS1HS411 - DSC", "course_name": "Modern and Post Modern World", "semester": 5},
    {"course_code": "NSUS1HS431 - DSE", "course_name": "Introduction to Society and Culture in East Asia", "semester": 5},
    {"course_code": "NSUS1HS432 - DSE", "course_name": "Society and Economy of Medieval India", "semester": 5},
    {"course_code": "DSC 10: SUS1EN210", "course_name": "Modernism", "semester": 5},
    {"course_code": "DSC 11: NSUS1EN211", "course_name": "Literary Theory", "semester": 5},
    {"course_code": "DSE 1: NSUS1EN231", "course_name": "Indian and World Literatures", "semester": 5},
    {"course_code": "DSE 2: NSUS1EN232", "course_name": "Issues of Gender in Indian Literary Texts", "semester": 5},
    {"course_code": "NSUS1PO610 - DSC", "course_name": "India's Foreign Policy", "semester": 5},
    {"course_code": "NSUS1PO611 - DSC", "course_name": "Public Policy", "semester": 5},
    {"course_code": "NSUS1PO631, DSE", "course_name": "Colonialism and Nationalism in India", "semester": 5},
    {"course_code": "NSUS1PO632, DSE", "course_name": "Party Politics in India", "semester": 5},
    {"course_code": "NSUS1GE001 - GE", "course_name": "Feminism: Theory and Practice", "semester": 5},
    {"course_code": "NSUS1EC111 - DSC", "course_name": "Public Economics: Theory and Policy", "semester": 5},
    {"course_code": "NSUS1EC112 - DSC", "course_name": "Development Economics", "semester": 5},
    {"course_code": "NSUS1EC131 - DSE", "course_name": "Money, Banking and Finance", "semester": 5},

    # Semester 7
    {"course_code": "NSUS1GE913", "course_name": "School, Schooling and Education", "semester": 7},
    {"course_code": "NSUS1GE310", "course_name": "Bhartiya katha Sahitya evam anya Gadya Vidhayen (GE Hindi)", "semester": 7},
    {"course_code": "DSC15 - NSUS1PS715", "course_name": "Community Mental Health", "semester": 7},
    {"course_code": "RM (DSC16) - NSUS1PS716", "course_name": "Advanced Research Methods in Psychology", "semester": 7},
    {"course_code": "DSE4 - NSUS1PS734", "course_name": "Psychosocial Perspectives in Education", "semester": 7},
    {"course_code": "DSE5 - NSUS1PS735", "course_name": "Understanding love from psychosocial perspectives", "semester": 7},
    {"course_code": "NSUS1SC814 - DSC", "course_name": "Culture, Identity and Society", "semester": 7},
    {"course_code": "NSUS1SC815 - DSC", "course_name": "'Methods and Techniques in Sociology'", "semester": 7},
    {"course_code": "NSUS1SC835 - DSE", "course_name": "Economy and Society", "semester": 7},
    {"course_code": "NSUS1HS414 - DSC", "course_name": "Reading and Academic Writing in Historical Study", "semester": 7},
    {"course_code": "NSUS1HS436 - DSE", "course_name": "Protests, Resistance and Movements in Colonial India", "semester": 7},
    {"course_code": "NSUS1HS433", "course_name": "Histories of Caste: Hierarchy, Identity and Resistance in South Asia", "semester": 7},
    {"course_code": "NSUS1HS437 - DSC (RM)", "course_name": "Theories and Methods in the Study of History", "semester": 7},
    {"course_code": "NSUS1EN215 - DSC", "course_name": "Theories of Marginality", "semester": 7},
    {"course_code": "NSUS1EN236 - DSE", "course_name": "Understanding Cinema", "semester": 7},
    {"course_code": "NSUS1EN237 - DSE", "course_name": "Reading Crime Fiction", "semester": 7},
    {"course_code": "NSUS1EN238 - DSE", "course_name": "Introduction to Cultural studies", "semester": 7},
    {"course_code": "NSUS1EN216 - RM (DSC)", "course_name": "Introduction to Research Methods", "semester": 7},
    {"course_code": "NSUS1PO614 -DSC", "course_name": "Introduction to Global International Relations: Non-Western Perspective", "semester": 7},
    {"course_code": "NSUS1PO634 -DSE", "course_name": "Citizenship in the Contemporary World", "semester": 7},
    {"course_code": "NSUS1PO636 -DSE", "course_name": "Peace and Conflict Studies", "semester": 7},
    {"course_code": "NSUS1PO635 -DSE", "course_name": "Democracy, Governance and Development: The Indian Experience", "semester": 7},
    {"course_code": "NSUS1PO615 - DSC", "course_name": "Research Methods for Political Science", "semester": 7},
    {"course_code": "NSUS1EC115 - DSC", "course_name": "International trade", "semester": 7},
    {"course_code": "NSUS1EC138 - DSE", "course_name": "Economics of Regulation", "semester": 7},
    {"course_code": "NSUS1EC121 - DSC (RM)", "course_name": "Research Methods in Economics", "semester": 7},
    {"course_code": "NSUS1EC140 - DSE", "course_name": "Financial Economics", "semester": 7},
    {"course_code": "NSUS1EC135-DSE", "course_name": "Social Policy and Welfare", "semester": 7}
]
rooms_data = [
    {"room_code": "305", "capacity": 50},
    {"room_code": "71B", "capacity": 25},
    {"room_code": "CR1", "capacity": 45},
    {"room_code": "NL2", "capacity": 85},
    {"room_code": "71F", "capacity": 25},
    {"room_code": "WS(GF)- 2B", "capacity": 35},
    {"room_code": "CR3", "capacity": 45},
    {"room_code": "CR4", "capacity": 45},
    {"room_code": "CR5", "capacity": 40},
    {"room_code": "CR6", "capacity": 42},
    {"room_code": "WS(GF)-1A", "capacity": 35},
    {"room_code": "SSR1", "capacity": 36},
    {"room_code": "SSR2", "capacity": 36},
    {"room_code": "N4", "capacity": 40},
    {"room_code": "N5", "capacity": 40},
    {"room_code": "CR11", "capacity": 85},
    {"room_code": "301", "capacity": 80},
    {"room_code": "308", "capacity": 25},
    {"room_code": "LAB 58", "capacity": 80}
]

# 4. Clear existing collections to prevent duplicates during testing
db.courses.drop()
db.rooms.drop()

# 5. Insert the data into collections
try:
    print("Pushing rooms and courses to MongoDB Atlas...")
    db.courses.insert_many(courses_data)
    db.rooms.insert_many(rooms_data)
    print("✅ Rooms and courses successfully populated in your cloud database!")
except Exception as e:
    print("❌ Failed to insert data:")
    print(e)
