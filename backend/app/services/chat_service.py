"""Service layer for chat functionality."""
from typing import Dict, List, Any
from app.core.logging import logger
from app.core.exceptions import NLPProcessingError
from app.database.repositories.admissions import AdmissionRepository
from app.database.repositories.courses import CourseRepository
from app.database.repositories.facilities import FacilityRepository
from app.database.repositories.contacts import ContactRepository
from app.database.repositories.qa import QARepository


class ChatService:
    """Service for handling chat logic and coordinating data access."""

    def __init__(
        self,
        admission_repo: AdmissionRepository,
        course_repo: CourseRepository,
        facility_repo: FacilityRepository,
        contact_repo: ContactRepository,
        qa_repo: QARepository
    ):
        self.admission_repo = admission_repo
        self.course_repo = course_repo
        self.facility_repo = facility_repo
        self.contact_repo = contact_repo
        self.qa_repo = qa_repo

    def process_query(
        self,
        intent: str,
        entities: List[Dict[str, str]],
        user_input: str,
        user_context: Dict[str, Any],
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """
        Process user query based on intent and retrieve relevant information.

        Args:
            intent: Detected intent from NLP pipeline
            entities: Extracted entities from NLP pipeline
            user_input: Original user input
            user_context: Additional user context
            conversation_history: Conversation history

        Returns:
            Generated response string
        """
        logger.info(f"Processing query with intent: {intent}")

        try:
            if intent == "admission_info":
                return self._handle_admission_query(entities, user_input)
            elif intent == "course_info":
                return self._handle_course_query(entities, user_input)
            elif intent == "fee_inquiry":
                return self._handle_fee_query(entities, user_input)
            elif intent == "hostel_info":
                return self._handle_hostel_query(entities, user_input)
            elif intent == "library_info":
                return self._handle_library_query(entities, user_input)
            elif intent == "placement_info":
                return self._handle_placement_query(entities, user_input)
            elif intent == "contact_info":
                return self._handle_contact_query(entities, user_input)
            else:  # general_info or unknown
                return self._handle_general_query(user_input)

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise NLPProcessingError(f"Failed to process query: {e}")

    def _handle_admission_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle admission-related queries."""
        admission_info = self.admission_repo.get_all()

        if admission_info:
            info_text = "\n\n"
            for info in admission_info:
                info_text += f"**{info['category']} - {info['information']}**: {info['details']}\n"

            return f"Here's information about admissions: {info_text}"

        return "For detailed admission information, please visit the admissions office or check our website. The admissions team is available Monday-Friday, 9 AM to 5 PM."

    def _handle_course_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle course-related queries."""
        # Check if specific department mentioned
        department = None
        for entity in entities:
            if entity.get("label") == "DEPARTMENT":
                department = entity.get("text")
                break

        if department:
            courses = self.course_repo.get_by_department(department)
        else:
            courses = self.course_repo.get_all()

        if courses:
            info_text = "\n\n"
            for course in courses:
                info_text += f"**{course['course_name']}** ({course['department']})\n"
                info_text += f"Duration: {course['duration']}\n"
                info_text += f"Eligibility: {course['eligibility']}\n"
                info_text += f"Description: {course['description']}\n\n"

            return f"Here are the course details: {info_text}"

        return "For specific course details, please contact the academic department or visit the course catalog on our website."

    def _handle_fee_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle fee-related queries."""
        fee_info = '''
        **Fee Structure:**

        **Undergraduate Programs:**
        - Engineering: ₹1,50,000 per year
        - Science: ₹80,000 per year
        - Commerce: ₹60,000 per year

        **Postgraduate Programs:**
        - M.Tech: ₹2,00,000 per year
        - MBA: ₹3,00,000 per year
        - M.Sc: ₹1,00,000 per year

        **Additional Costs:**
        - Hostel: ₹80,000 per year
        - Mess: ₹40,000 per year
        - Library & Lab Fee: ₹10,000 per year

        **Payment Options:**
        - Online payment through college portal
        - Bank transfer or demand draft
        - Installment facility available

        **Scholarships Available:**
        - Merit-based scholarships
        - Need-based financial aid
        - Government scholarships
        '''

        return f"Regarding fees and payments: {fee_info}"

    def _handle_hostel_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle hostel-related queries."""
        hostel_facilities = self.facility_repo.get_by_category("Accommodation")

        if hostel_facilities:
            info_text = "\n\n"
            for facility in hostel_facilities:
                info_text += f"**{facility['facility_name']}**\n"
                info_text += f"Description: {facility['description']}\n"
                info_text += f"Location: {facility['location']}\n"
                info_text += f"Timings: {facility['timings']}\n\n"

            info_text += '''
            **Hostel Rules & Facilities:**
            - Wi-Fi connectivity in all rooms
            - Laundry facilities
            - Recreation room with TV and games
            - 24/7 security
            - Mess facilities with nutritious meals
            - Study rooms for group discussions
            '''

            return f"Hostel information: {info_text}"

        return "For hostel accommodation details, please contact the hostel administration office during working hours."

    def _handle_library_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle library-related queries."""
        library_info = '''
        **Library Facilities:**

        **Collection:**
        - Over 50,000 books covering all disciplines
        - 200+ national and international journals
        - Digital library with e-books and online resources
        - Reference section with encyclopedias and dictionaries

        **Services:**
        - Book lending service
        - Inter-library loan facility
        - Photocopy and printing services
        - Research assistance
        - Online catalog search

        **Facilities:**
        - Spacious reading halls with 500+ seats
        - Computer lab with high-speed internet
        - Group study rooms
        - Audio-visual section
        - Air-conditioned environment

        **Timings:**
        - Monday to Saturday: 8:00 AM to 8:00 PM
        - Sunday: 10:00 AM to 6:00 PM
        - Extended hours during exams
        '''

        return f"Library details: {library_info}"

    def _handle_placement_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle placement-related queries."""
        placement_info = '''
        **Placement Information:**

        **Placement Statistics:**
        - Overall placement rate: 85%
        - Average package: ₹6.5 LPA
        - Highest package: ₹25 LPA
        - Top recruiters: TCS, Infosys, Wipro, Amazon, Google

        **Training Programs:**
        - Aptitude training
        - Technical skill development
        - Interview preparation
        - Personality development
        - Mock interviews and group discussions

        **Placement Process:**
        - Pre-placement talks by companies
        - Online/written tests
        - Technical interviews
        - HR interviews
        - Final selection

        **Contact:**
        - Placement Officer: Dr. Anderson
        - Phone: +91-123-456-7894
        - Email: placements@college.edu
        - Office: Career Development Center
        '''

        return f"Here's information about placements: {placement_info}"

    def _handle_contact_query(self, entities: List[Dict[str, str]], user_input: str) -> str:
        """Handle contact information queries."""
        contact_info = self.contact_repo.get_all()

        if contact_info:
            info_text = "\n\n"
            for contact in contact_info:
                info_text += f"**{contact['department']} Department**\n"
                info_text += f"Contact Person: {contact['contact_person']}\n"
                info_text += f"Phone: {contact['phone']}\n"
                info_text += f"Email: {contact['email']}\n"
                info_text += f"Office: {contact['office_location']}\n\n"

            return f"Contact information: {info_text}"

        return "For general inquiries, you can contact the main office at +91-123-456-7890 or email info@college.edu"

    def _handle_general_query(self, user_input: str) -> str:
        """Handle general queries."""
        # Search across all repositories
        results = []

        # Search in admissions
        for item in self.admission_repo.get_all():
            if user_input.lower() in str(item.values()).lower():
                results.append({"table": "admissions", **item})

        # Search in courses
        for item in self.course_repo.get_all():
            if user_input.lower() in str(item.values()).lower():
                results.append({"table": "courses", **item})

        # Search in facilities
        for item in self.facility_repo.get_all():
            if user_input.lower() in str(item.values()).lower():
                results.append({"table": "facilities", **item})

        # Search in contacts
        for item in self.contact_repo.get_all():
            if user_input.lower() in str(item.values()).lower():
                results.append({"table": "contact_info", **item})

        # Search in Q&A
        for item in self.qa_repo.get_all():
            if user_input.lower() in str(item.values()).lower():
                results.append({"table": "qa_dataset", **item})

        if results:
            info_text = "\n\n"
            for result in results[:3]:  # Limit to top 3 results
                table = result.get('table', 'unknown')
                if table == 'admissions':
                    info_text += f"**{result['category']} - {result['information']}**: {result['details']}\n\n"
                elif table == 'courses':
                    info_text += f"**{result['course_name']}** ({result['department']}): {result['description']}\n\n"
                elif table == 'facilities':
                    info_text += f"**{result['facility_name']}**: {result['description']}\n\n"
                elif table == 'contact_info':
                    info_text += f"**{result['department']}**: {result['contact_person']} - {result['phone']}\n\n"
                elif table == 'qa_dataset':
                    info_text += f"**Q: {result['question']}**: {result['answer']}\n\n"
                else:
                    info_text += f"Information from {table}\n\n"

            return f"Here's what I found: {info_text}"

        return "I'm here to help with your college-related queries! You can ask me about admissions, courses, fees, facilities, and more."
