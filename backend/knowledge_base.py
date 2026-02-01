from typing import Dict, List
import sqlite3
from pathlib import Path

class KnowledgeBase:
    def __init__(self):
        self.db_path = Path("data/knowledge_base/college_info.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()
        self._populate_sample_data()

    def _initialize_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY,
            category TEXT,
            information TEXT,
            details TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            course_name TEXT,
            department TEXT,
            duration TEXT,
            eligibility TEXT,
            description TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY,
            facility_name TEXT,
            category TEXT,
            description TEXT,
            location TEXT,
            timings TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_info (
            id INTEGER PRIMARY KEY,
            department TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            office_location TEXT
        )
        ''')

        # Create table for question-answer dataset
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_dataset (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def _populate_sample_data(self):
        """Populate database with sample college information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM admissions")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return

        # Sample admissions data
        admissions_data = [
            ("undergraduate", "Eligibility", "12th standard with minimum 60% marks"),
            ("undergraduate", "Application Period", "March 1st to June 30th"),
            ("undergraduate", "Entrance Test", "College entrance exam required"),
            ("postgraduate", "Eligibility", "Bachelor's degree with minimum 55% marks"),
            ("postgraduate", "Application Period", "April 1st to July 31st"),
            ("postgraduate", "Entrance Test", "Graduate aptitude test required"),
        ]

        cursor.executemany("INSERT INTO admissions (category, information, details) VALUES (?, ?, ?)", 
                          admissions_data)

        # Sample courses data
        courses_data = [
            ("Computer Science Engineering", "Engineering", "4 years", "12th with Physics, Chemistry, Mathematics", 
             "Comprehensive program covering programming, algorithms, and software development"),
            ("Electronics Engineering", "Engineering", "4 years", "12th with Physics, Chemistry, Mathematics",
             "Focus on electronic systems, communication, and embedded systems"),
            ("MBA", "Management", "2 years", "Bachelor's degree in any field",
             "Master of Business Administration with specializations in various domains"),
            ("Physics", "Science", "3 years", "12th with Physics and Mathematics",
             "Undergraduate program in Physics with theoretical and practical components"),
        ]

        cursor.executemany(
            "INSERT INTO courses (course_name, department, duration, eligibility, description) VALUES (?, ?, ?, ?, ?)", 
            courses_data
        )

        # Sample facilities data
        facilities_data = [
            ("Central Library", "Academic", "Modern library with over 50,000 books and digital resources", 
             "Main Campus", "8 AM to 8 PM"),
            ("Computer Lab", "Academic", "State-of-the-art computer lab with latest hardware and software", 
             "Engineering Block", "9 AM to 6 PM"),
            ("Boys Hostel", "Accommodation", "500 rooms with modern amenities and Wi-Fi", 
             "Campus Hostel Block A", "24/7"),
            ("Girls Hostel", "Accommodation", "300 rooms with 24/7 security and modern facilities", 
             "Campus Hostel Block B", "24/7"),
            ("Sports Complex", "Recreation", "Indoor and outdoor sports facilities including gymnasium", 
             "Sports Block", "6 AM to 10 PM"),
        ]

        cursor.executemany(
            "INSERT INTO facilities (facility_name, category, description, location, timings) VALUES (?, ?, ?, ?, ?)", 
            facilities_data
        )

        # Sample contact information
        contact_data = [
            ("Admissions", "Dr. Smith", "+91-123-456-7890", "admissions@college.edu", "Admin Block, Room 101"),
            ("Academics", "Prof. Johnson", "+91-123-456-7891", "academics@college.edu", "Academic Block, Room 201"),
            ("Hostel", "Mr. Brown", "+91-123-456-7892", "hostel@college.edu", "Hostel Office"),
            ("Library", "Ms. Davis", "+91-123-456-7893", "library@college.edu", "Library Building"),
        ]

        cursor.executemany(
            "INSERT INTO contact_info (department, contact_person, phone, email, office_location) VALUES (?, ?, ?, ?, ?)", 
            contact_data
        )

        conn.commit()
        conn.close()

    def get_admission_info(self, category: str = None) -> List[Dict]:
        """Get admission information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute("SELECT * FROM admissions WHERE category = ?", (category,))
        else:
            cursor.execute("SELECT * FROM admissions")

        rows = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "category": row[1], "information": row[2], "details": row[3]} 
                for row in rows]

    def get_course_info(self, department: str = None) -> List[Dict]:
        """Get course information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if department:
            cursor.execute("SELECT * FROM courses WHERE department LIKE ?", (f"%{department}%",))
        else:
            cursor.execute("SELECT * FROM courses")

        rows = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "course_name": row[1], "department": row[2], 
                 "duration": row[3], "eligibility": row[4], "description": row[5]} 
                for row in rows]

    def get_facility_info(self, category: str = None) -> List[Dict]:
        """Get facility information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute("SELECT * FROM facilities WHERE category = ?", (category,))
        else:
            cursor.execute("SELECT * FROM facilities")

        rows = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "facility_name": row[1], "category": row[2], 
                 "description": row[3], "location": row[4], "timings": row[5]} 
                for row in rows]

    def get_contact_info(self, department: str = None) -> List[Dict]:
        """Get contact information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if department:
            cursor.execute("SELECT * FROM contact_info WHERE department LIKE ?", (f"%{department}%",))
        else:
            cursor.execute("SELECT * FROM contact_info")

        rows = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "department": row[1], "contact_person": row[2], 
                 "phone": row[3], "email": row[4], "office_location": row[5]} 
                for row in rows]

    def search_information(self, query: str) -> List[Dict]:
        """Search across all information"""
        results = []
        query_lower = query.lower()

        # Search in all tables
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Search admissions
        cursor.execute("SELECT 'admission' as type, information, details FROM admissions WHERE LOWER(information) LIKE ? OR LOWER(details) LIKE ?", 
                      (f"%{query_lower}%", f"%{query_lower}%"))
        results.extend([{"type": row[0], "info": row[1], "details": row[2]} for row in cursor.fetchall()])

        # Search courses
        cursor.execute("SELECT 'course' as type, course_name, description FROM courses WHERE LOWER(course_name) LIKE ? OR LOWER(description) LIKE ?", 
                      (f"%{query_lower}%", f"%{query_lower}%"))
        results.extend([{"type": row[0], "info": row[1], "details": row[2]} for row in cursor.fetchall()])

        # Search facilities
        cursor.execute("SELECT 'facility' as type, facility_name, description FROM facilities WHERE LOWER(facility_name) LIKE ? OR LOWER(description) LIKE ?", 
                      (f"%{query_lower}%", f"%{query_lower}%"))
        results.extend([{"type": row[0], "info": row[1], "details": row[2]} for row in cursor.fetchall()])

        # Search Q&A dataset
        cursor.execute("SELECT 'qa' as type, question, answer FROM qa_dataset WHERE LOWER(question) LIKE ? OR LOWER(answer) LIKE ?", 
                      (f"%{query_lower}%", f"%{query_lower}%"))
        results.extend([{"type": row[0], "info": row[1], "details": row[2]} for row in cursor.fetchall()])

        conn.close()
        return results

    def add_qa_pair(self, question: str, answer: str) -> int:
        """Add a question-answer pair to the dataset"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO qa_dataset (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def get_qa_pairs(self, question: str = None) -> List[Dict]:
        """Get question-answer pairs, optionally filtered by question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if question:
            cursor.execute("SELECT * FROM qa_dataset WHERE question LIKE ?", (f"%{question}%",))
        else:
            cursor.execute("SELECT * FROM qa_dataset")

        rows = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "question": row[1], "answer": row[2]} for row in rows]
