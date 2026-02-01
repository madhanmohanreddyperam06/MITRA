from typing import Dict, List, Any
import random

class ResponseGenerator:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

        # Response templates
        self.templates = {
            "admission_info": [
                "Here's information about admissions: {info}",
                "Regarding admissions: {info}",
                "For admission details: {info}"
            ],
            "course_info": [
                "Here are the course details: {info}",
                "About the courses: {info}",
                "Course information: {info}"
            ],
            "fee_inquiry": [
                "Regarding fees and payments: {info}",
                "Fee information: {info}",
                "About the fee structure: {info}"
            ],
            "hostel_info": [
                "Hostel information: {info}",
                "About accommodation facilities: {info}",
                "Regarding hostel facilities: {info}"
            ],
            "library_info": [
                "Library details: {info}",
                "About library facilities: {info}",
                "Library information: {info}"
            ],
            "contact_info": [
                "Contact information: {info}",
                "You can reach out to: {info}",
                "Here are the contact details: {info}"
            ],
            "general_info": [
                "Here's what I found: {info}",
                "General information: {info}",
                "About your query: {info}"
            ]
        }

        # Fallback responses
        self.fallback_responses = {
            "admission_info": "For detailed admission information, please visit the admissions office or check our website. The admissions team is available Monday-Friday, 9 AM to 5 PM.",
            "course_info": "For specific course details, please contact the academic department or visit the course catalog on our website.",
            "fee_inquiry": "For fee-related queries, please contact the accounts department. Fee payment can be made online or at the college accounts office.",
            "hostel_info": "For hostel accommodation details, please contact the hostel administration office during working hours.",
            "library_info": "The library is open Monday-Saturday, 8 AM to 8 PM. For specific resources, please contact the library staff.",
            "contact_info": "For general inquiries, you can contact the main office at +91-123-456-7890 or email info@college.edu",
            "general_info": "I'm here to help with your college-related queries! You can ask me about admissions, courses, fees, facilities, and more."
        }

    def generate_response(self, intent: str, entities: List[Dict], user_input: str, 
                         user_context: Dict, conversation_history: List[Dict]) -> str:
        """Generate response based on intent and context"""

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
            return f"I apologize, but I encountered an error while processing your request. Please try rephrasing your question. Error: {str(e)}"

    def _handle_admission_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle admission-related queries"""
        admission_info = self.kb.get_admission_info()

        if admission_info:
            info_text = "\n\n"
            for info in admission_info:
                info_text += f"**{info['information']}**: {info['details']}\n"

            template = random.choice(self.templates["admission_info"])
            return template.format(info=info_text)

        return self.fallback_responses["admission_info"]

    def _handle_course_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle course-related queries"""
        # Check if specific department mentioned
        department = None
        for entity in entities:
            if entity.get("label") == "DEPARTMENT":
                department = entity.get("text")
                break

        courses = self.kb.get_course_info(department)

        if courses:
            info_text = "\n\n"
            for course in courses:
                info_text += f"**{course['course_name']}** ({course['department']})\n"
                info_text += f"Duration: {course['duration']}\n"
                info_text += f"Eligibility: {course['eligibility']}\n"
                info_text += f"Description: {course['description']}\n\n"

            template = random.choice(self.templates["course_info"])
            return template.format(info=info_text)

        return self.fallback_responses["course_info"]

    def _handle_fee_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle fee-related queries"""
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

        template = random.choice(self.templates["fee_inquiry"])
        return template.format(info=fee_info)

    def _handle_hostel_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle hostel-related queries"""
        hostel_facilities = self.kb.get_facility_info("Accommodation")

        if hostel_facilities:
            info_text = "\n\n"
            for facility in hostel_facilities:
                info_text += f"**{facility['facility_name']}**\n"
                info_text += f"Description: {facility['description']}\n"
                info_text += f"Location: {facility['location']}\n"
                info_text += f"Availability: {facility['timings']}\n\n"

            info_text += '''
            **Hostel Rules & Facilities:**
            - Wi-Fi connectivity in all rooms
            - Laundry facilities
            - Recreation room with TV and games
            - 24/7 security
            - Mess facilities with nutritious meals
            - Study rooms for group discussions
            '''

            template = random.choice(self.templates["hostel_info"])
            return template.format(info=info_text)

        return self.fallback_responses["hostel_info"]

    def _handle_library_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle library-related queries"""
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

        template = random.choice(self.templates["library_info"])
        return template.format(info=library_info)

    def _handle_placement_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle placement-related queries"""
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

    def _handle_contact_query(self, entities: List[Dict], user_input: str) -> str:
        """Handle contact information queries"""
        contact_info = self.kb.get_contact_info()

        if contact_info:
            info_text = "\n\n"
            for contact in contact_info:
                info_text += f"**{contact['department']} Department**\n"
                info_text += f"Contact Person: {contact['contact_person']}\n"
                info_text += f"Phone: {contact['phone']}\n"
                info_text += f"Email: {contact['email']}\n"
                info_text += f"Office: {contact['office_location']}\n\n"

            template = random.choice(self.templates["contact_info"])
            return template.format(info=info_text)

        return self.fallback_responses["contact_info"]

    def _handle_general_query(self, user_input: str) -> str:
        """Handle general queries"""
        # Search for relevant information
        search_results = self.kb.search_information(user_input)

        if search_results:
            info_text = "\n\n"
            for result in search_results[:3]:  # Limit to top 3 results
                info_text += f"**{result['info']}**: {result['details']}\n\n"

            template = random.choice(self.templates["general_info"])
            return template.format(info=info_text)

        return self.fallback_responses["general_info"]
