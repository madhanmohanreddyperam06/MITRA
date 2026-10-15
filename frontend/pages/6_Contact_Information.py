import streamlit as st
import sys
import os
import pandas as pd

# Ensure components directory is in sys.path when run directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.theme import apply_global_theme

def show():
    apply_global_theme()

    if not st.session_state.get("authenticated", False):
        st.warning("🔒 Please log in or continue as guest from the main landing page to access this section.")
        if st.button("⬅️ Go to Landing Page", width='stretch', type="primary"):
            st.switch_page("main.py")
        st.stop()

    st.title("📞 Contact Information")

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Administration", "🎓 Departments", "🏠 Student Services", "🚨 Emergency"])

    with tab1:
        st.subheader("Administration & Academic Offices")
        
        admin_contacts = {
            'Department': ['Admissions Office', 'Academic Affairs', 'Registrar Office', 'Finance Office', 
                          'Examination Cell', 'Research & Development'],
            'Contact Person': ['Mr. John Smith', 'Dr. Sarah Johnson', 'Dr. Michael Brown', 'Finance Officer',
                             'Dr. Emily Davis', 'Dr. Robert Wilson'],
            'Phone': ['+91-123-456-7890', '+91-123-456-7891', '+91-123-456-7892', '+91-123-456-7893',
                     '+91-123-456-7894', '+91-123-456-7895'],
            'Email': ['admissions@college.edu', 'academics@college.edu', 'registrar@college.edu', 'accounts@college.edu',
                    'exams@college.edu', 'research@college.edu'],
            'Office': ['Room 101, Admin Block', 'Room 105, Admin Block', 'Room 110, Admin Block', 'Room 108, Admin Block',
                      'Room 115, Admin Block', 'Room 120, Research Block'],
            'Timings': ['Mon-Fri, 9AM-5PM', 'Mon-Fri, 9AM-5PM', 'Mon-Fri, 9AM-5PM', 'Mon-Fri, 9:30AM-4PM',
                       'Mon-Fri, 10AM-4PM', 'Mon-Fri, 9AM-6PM']
        }
        df_admin = pd.DataFrame(admin_contacts)
        st.dataframe(df_admin, width='stretch', hide_index=True)
        
        st.markdown("""
        ### Important Notes
        - All offices are closed on Sundays and public holidays
        - Prior appointment recommended for in-person visits
        - Online services available through student portal
        - Email responses within 24-48 hours
        """)

    with tab2:
        st.subheader("Department-wise Contact Information")
        
        dept = st.selectbox("Select Department", 
                           ['Engineering', 'Sciences', 'Commerce & Management', 'Arts', 'Pharmacy'])
        
        if dept == 'Engineering':
            eng_contacts = {
                'Department': ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical'],
                'HOD': ['Dr. A. Kumar', 'Dr. B. Sharma', 'Dr. C. Patel', 'Dr. D. Singh', 'Dr. E. Gupta'],
                'Office': ['Block A, Floor 2', 'Block A, Floor 3', 'Block B, Floor 1', 'Block B, Floor 2', 'Block B, Floor 3'],
                'Phone': ['+91-123-456-8001', '+91-123-456-8002', '+91-123-456-8003', '+91-123-456-8004', '+91-123-456-8005'],
                'Email': ['cse@college.edu', 'ece@college.edu', 'mech@college.edu', 'civil@college.edu', 'eee@college.edu']
            }
            df_eng = pd.DataFrame(eng_contacts)
            st.dataframe(df_eng, width='stretch', hide_index=True)
        
        elif dept == 'Sciences':
            science_contacts = {
                'Department': ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Biotechnology'],
                'HOD': ['Dr. F. Rao', 'Dr. G. Nair', 'Dr. H. Iyer', 'Dr. I. Menon', 'Dr. J. Pillai'],
                'Office': ['Block C, Floor 1', 'Block C, Floor 2', 'Block C, Floor 3', 'Block C, Floor 4', 'Block D, Floor 1'],
                'Phone': ['+91-123-456-8101', '+91-123-456-8102', '+91-123-456-8103', '+91-123-456-8104', '+91-123-456-8105'],
                'Email': ['physics@college.edu', 'chemistry@college.edu', 'maths@college.edu', 'biology@college.edu', 'biotech@college.edu']
            }
            df_science = pd.DataFrame(science_contacts)
            st.dataframe(df_science, width='stretch', hide_index=True)
        
        elif dept == 'Commerce & Management':
            commerce_contacts = {
                'Department': ['Commerce', 'Management', 'Economics', 'Accounting'],
                'HOD': ['Dr. K. Verma', 'Dr. L. Agarwal', 'Dr. M. Joshi', 'Dr. N. Sharma'],
                'Office': ['Block E, Floor 1', 'Block E, Floor 2', 'Block E, Floor 3', 'Block E, Floor 4'],
                'Phone': ['+91-123-456-8201', '+91-123-456-8202', '+91-123-456-8203', '+91-123-456-8204'],
                'Email': ['commerce@college.edu', 'management@college.edu', 'economics@college.edu', 'accounting@college.edu']
            }
            df_commerce = pd.DataFrame(commerce_contacts)
            st.dataframe(df_commerce, width='stretch', hide_index=True)
        
        elif dept == 'Arts':
            arts_contacts = {
                'Department': ['English', 'History', 'Political Science', 'Psychology', 'Sociology'],
                'HOD': ['Dr. O. Thomas', 'Dr. P. Kumar', 'Dr. Q. Singh', 'Dr. R. Das', 'Dr. S. Gupta'],
                'Office': ['Block F, Floor 1', 'Block F, Floor 2', 'Block F, Floor 3', 'Block F, Floor 4', 'Block F, Floor 5'],
                'Phone': ['+91-123-456-8301', '+91-123-456-8302', '+91-123-456-8303', '+91-123-456-8304', '+91-123-456-8305'],
                'Email': ['english@college.edu', 'history@college.edu', 'polscience@college.edu', 'psychology@college.edu', 'sociology@college.edu']
            }
            df_arts = pd.DataFrame(arts_contacts)
            st.dataframe(df_arts, width='stretch', hide_index=True)
        
        else:
            pharmacy_contacts = {
                'Department': ['Pharmaceutics', 'Pharmacology', 'Pharmaceutical Chemistry', 'Pharmacy Practice'],
                'HOD': ['Dr. T. Reddy', 'Dr. U. Patel', 'Dr. V. Kumar', 'Dr. W. Singh'],
                'Office': ['Block G, Floor 1', 'Block G, Floor 2', 'Block G, Floor 3', 'Block G, Floor 4'],
                'Phone': ['+91-123-456-8401', '+91-123-456-8402', '+91-123-456-8403', '+91-123-456-8404'],
                'Email': ['pharmaceutics@college.edu', 'pharmacology@college.edu', 'pharmchem@college.edu', 'pharmacypractice@college.edu']
            }
            df_pharmacy = pd.DataFrame(pharmacy_contacts)
            st.dataframe(df_pharmacy, width='stretch', hide_index=True)

    with tab3:
        st.subheader("Student Services")
        
        student_services = {
            'Service': ['Hostel & Accommodation', 'Central Library', 'Sports Complex', 'Health Center', 
                       'Career & Placement Cell', 'Counseling Center', 'Student Welfare', 'Grievance Cell'],
            'Contact Person': ['Chief Warden', 'Head Librarian', 'Sports Director', 'Medical Officer',
                             'Dr. Anderson', 'Dr. P. Sharma', 'Dr. Q. Patel', 'Dr. R. Kumar'],
            'Phone': ['+91-123-456-7001', '+91-123-456-7002', '+91-123-456-7003', '+91-123-456-7004',
                     '+91-123-456-7894', '+91-123-456-7005', '+91-123-456-7006', '+91-123-456-7007'],
            'Email': ['hostel@college.edu', 'library@college.edu', 'sports@college.edu', 'health@college.edu',
                     'placements@college.edu', 'counseling@college.edu', 'welfare@college.edu', 'grievance@college.edu'],
            'Office': ['Student Center', 'Library Building', 'Sports Complex', 'Health Center',
                      'CDC, Block B', 'Student Center', 'Admin Block', 'Admin Block'],
            'Timings': ['24/7', '8AM-8PM', '6AM-9PM', '24/7', '9AM-6PM', '9AM-5PM', '9AM-5PM', '9AM-5PM']
        }
        df_services = pd.DataFrame(student_services)
        st.dataframe(df_services, width='stretch', hide_index=True)
        
        st.markdown("""
        ### Student Support Services
        - **24/7 Hostel Support**: Wardens available round the clock
        - **Library**: Extended hours during exam periods
        - **Health Center**: Emergency services available 24/7
        - **Counseling**: Free psychological counseling for students
        - **Placement Support**: Career guidance and placement assistance
        """)

    with tab4:
        st.subheader("Emergency Contacts")
        
        st.error("🚨 **24/7 Emergency Helplines**")
        
        emergency_contacts = {
            'Service': ['Campus Security', 'Health Center/Ambulance', 'Anti-Ragging Helpline', 
                       'Women Safety Cell', 'Fire Emergency', 'Mental Health Crisis'],
            'Phone': ['+91-123-456-7899', '+91-123-456-7898', '1800-180-5522 / +91-123-456-7897',
                     '+91-123-456-7896', '101 / +91-123-456-7890', '+91-123-456-7895'],
            'Available': ['24/7', '24/7', '24/7', '24/7', '24/7', '24/7'],
            'Location': ['Main Gate', 'Health Center', 'Student Center', 'Women Hostel', 'Campus-wide', 'Health Center']
        }
        df_emergency = pd.DataFrame(emergency_contacts)
        st.dataframe(df_emergency, width='stretch', hide_index=True)
        
        st.markdown("---")
        st.subheader("📍 Campus Address")
        
        st.markdown("""
        **MITRA Institute of Technology & Science**
        
        Knowledge Park, Education Hub
        State - 500001
        
        **How to Reach:**
        - **By Train**: Nearest railway station - Central Station (5 km)
        - **By Bus**: City bus service available from all major points
        - **By Air**: Airport - 15 km from campus
        - **GPS Coordinates**: 17.3850° N, 78.4867° E
        
        **Google Maps Link**: [Click to view on map](https://maps.google.com)
        """)
        
        st.markdown("---")
        st.subheader("📧 Quick Contact Form")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            department = st.selectbox("Department", ["Admissions", "Academics", "Finance", "Hostel", "Placements", "Other"])
            subject = st.text_input("Subject")
            message = st.text_area("Your Message", height=150)
            
            submitted = st.form_submit_button("Send Message")
            if submitted:
                st.success("✅ Your message has been sent successfully! We will respond within 24-48 hours.")

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask for Contact Information", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user",
            "content": "I need contact information for a specific department"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
