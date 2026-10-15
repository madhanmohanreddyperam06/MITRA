import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

    st.title("📚 Course Information")

    # Department Overview
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎓 Undergraduate", "📜 Postgraduate", "🔬 Specializations"])

    with tab1:
        st.subheader("Department-wise Course Distribution")
        
        dept_data = {
            'Department': ['Engineering', 'Sciences', 'Commerce', 'Management', 'Arts', 'Pharmacy'],
            'UG Courses': [5, 4, 3, 2, 3, 2],
            'PG Courses': [3, 3, 2, 2, 1, 1],
            'Total Seats': [440, 210, 180, 120, 100, 80]
        }
        df_dept = pd.DataFrame(dept_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_dept = px.bar(df_dept, x='Department', y=['UG Courses', 'PG Courses'],
                           title="UG vs PG Courses by Department",
                           barmode='group', color_discrete_sequence=['#6d28d9', '#8b5cf6'])
            st.plotly_chart(fig_dept, width='stretch')
        
        with col2:
            fig_seats = px.pie(df_dept, values='Total Seats', names='Department',
                             title="Seat Distribution Across Departments",
                             color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa', 
                                                     '#c4b5fd', '#7c3aed', '#5b21b6'])
            st.plotly_chart(fig_seats, width='stretch')
        
        st.subheader("Department Statistics")
        st.dataframe(df_dept, width='stretch', hide_index=True)

    with tab2:
        st.subheader("Undergraduate Programs")
        
        course_type = st.selectbox("Select Department", ["Engineering", "Sciences", "Commerce & Management", "Arts"])
        
        if course_type == "Engineering":
            eng_courses = {
                'Course': ['B.Tech CSE', 'B.Tech ECE', 'B.Tech Mechanical', 'B.Tech Civil', 'B.Tech Electrical'],
                'Duration': ['4 Years', '4 Years', '4 Years', '4 Years', '4 Years'],
                'Seats': [120, 100, 80, 70, 70],
                'Fee/Year (₹)': [150000, 145000, 140000, 135000, 135000],
                'Eligibility': ['60% in 12th Science', '60% in 12th Science', '60% in 12th Science', 
                               '60% in 12th Science', '60% in 12th Science']
            }
            df_eng = pd.DataFrame(eng_courses)
            st.dataframe(df_eng, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Engineering Curriculum Highlights
            - **Semester System**: 8 semesters with project work in final year
            - **Industry Exposure**: 6-month internship in 7th semester
            - **Lab Facilities**: State-of-the-art labs for each specialization
            - **Research Opportunities**: Undergraduate research program available
            - **Placement Support**: Dedicated placement cell with 90%+ placement rate
            """)
        
        elif course_type == "Sciences":
            science_courses = {
                'Course': ['B.Sc Physics', 'B.Sc Chemistry', 'B.Sc Mathematics', 'B.Sc Biology', 'B.Sc Computer Science'],
                'Duration': ['3 Years', '3 Years', '3 Years', '3 Years', '3 Years'],
                'Seats': [60, 60, 60, 50, 60],
                'Fee/Year (₹)': [80000, 80000, 80000, 85000, 90000],
                'Eligibility': ['55% in 12th Science', '55% in 12th Science', '55% in 12th Science',
                              '55% in 12th Science', '55% in 12th Science']
            }
            df_science = pd.DataFrame(science_courses)
            st.dataframe(df_science, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Sciences Program Features
            - **Research Focus**: Strong emphasis on experimental research
            - **Lab Work**: Extensive practical sessions with modern equipment
            - **Interdisciplinary**: Option to take electives from other departments
            - **Field Trips**: Regular visits to research institutes and industries
            """)
        
        elif course_type == "Commerce & Management":
            commerce_courses = {
                'Course': ['B.Com', 'B.Com (Honors)', 'BBA', 'BBA (Finance)', 'Economics'],
                'Duration': ['3 Years', '3 Years', '3 Years', '3 Years', '3 Years'],
                'Seats': [80, 40, 60, 40, 40],
                'Fee/Year (₹)': [75000, 85000, 85000, 90000, 75000],
                'Eligibility': ['50% in 12th', '55% in 12th', '50% in 12th', '55% in 12th', '50% in 12th']
            }
            df_commerce = pd.DataFrame(commerce_courses)
            st.dataframe(df_commerce, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Commerce & Management Highlights
            - **Industry Projects**: Live projects with corporate partners
            - **Case Studies**: Harvard-style case study methodology
            - **Soft Skills**: Emphasis on communication and leadership
            - **Certifications**: Additional certifications in finance and accounting
            """)
        
        else:
            arts_courses = {
                'Course': ['BA English', 'BA History', 'BA Political Science', 'BA Psychology', 'BA Sociology'],
                'Duration': ['3 Years', '3 Years', '3 Years', '3 Years', '3 Years'],
                'Seats': [40, 40, 40, 30, 30],
                'Fee/Year (₹)': [60000, 60000, 60000, 65000, 60000],
                'Eligibility': ['45% in 12th', '45% in 12th', '45% in 12th', '50% in 12th', '45% in 12th']
            }
            df_arts = pd.DataFrame(arts_courses)
            st.dataframe(df_arts, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Arts Program Features
            - **Interdisciplinary Approach**: Blend of traditional and modern subjects
            - **Critical Thinking**: Emphasis on analytical and research skills
            - **Cultural Activities**: Rich cultural and literary environment
            - **Career Support**: Preparation for civil services, media, and academia
            """)

    with tab3:
        st.subheader("Postgraduate Programs")
        
        pg_course_type = st.selectbox("Select PG Department", ["Engineering", "Sciences", "Management", "Commerce"])
        
        if pg_course_type == "Engineering":
            pg_eng = {
                'Course': ['M.Tech CSE', 'M.Tech ECE', 'M.Tech Mechanical', 'M.Tech VLSI', 'M.Tech Structural Engg'],
                'Duration': ['2 Years', '2 Years', '2 Years', '2 Years', '2 Years'],
                'Seats': [40, 35, 30, 25, 25],
                'Fee/Year (₹)': [180000, 175000, 170000, 185000, 170000],
                'Specialization': ['AI/ML', 'Wireless Comm', 'CAD/CAM', 'VLSI Design', 'Structural Analysis']
            }
            df_pg_eng = pd.DataFrame(pg_eng)
            st.dataframe(df_pg_eng, width='stretch', hide_index=True)
            
            st.markdown("""
            ### M.Tech Program Highlights
            - **Research Focus**: Mandatory thesis with original research
            - **Industry Collaboration**: Joint projects with leading tech companies
            - **Publications**: Encouraged to publish in international journals
            - **Funding**: Research grants available for promising projects
            """)
        
        elif pg_course_type == "Sciences":
            pg_science = {
                'Course': ['M.Sc Physics', 'M.Sc Chemistry', 'M.Sc Mathematics', 'M.Sc Biotechnology', 'M.Sc Data Science'],
                'Duration': ['2 Years', '2 Years', '2 Years', '2 Years', '2 Years'],
                'Seats': [30, 30, 30, 25, 40],
                'Fee/Year (₹)': [90000, 90000, 90000, 95000, 150000],
                'Specialization': ['Condensed Matter', 'Organic Chemistry', 'Applied Math', 'Molecular Biology', 'ML & Analytics']
            }
            df_pg_science = pd.DataFrame(pg_science)
            st.dataframe(df_pg_science, width='stretch', hide_index=True)
            
            st.markdown("""
            ### M.Sc Program Features
            - **Advanced Labs**: Access to sophisticated research equipment
            - **Seminars**: Regular seminars by eminent scientists
            - **Research Papers**: Preparation for research publications
            - **PhD Pathway**: Direct pathway to doctoral programs
            """)
        
        elif pg_course_type == "Management":
            mgmt_courses = {
                'Course': ['MBA', 'MBA (Finance)', 'MBA (Marketing)', 'MBA (HR)', 'MBA (Operations)'],
                'Duration': ['2 Years', '2 Years', '2 Years', '2 Years', '2 Years'],
                'Seats': [60, 40, 40, 30, 30],
                'Fee/Year (₹)': [200000, 210000, 210000, 190000, 200000],
                'Specialization': ['General Management', 'Financial Management', 'Marketing Strategy', 'HR Analytics', 'Supply Chain']
            }
            df_mgmt = pd.DataFrame(mgmt_courses)
            st.dataframe(df_mgmt, width='stretch', hide_index=True)
            
            st.markdown("""
            ### MBA Program Excellence
            - **Case Method**: Learning through real-world business cases
            - **Industry Interface**: Regular industry visits and guest lectures
            - **Internships**: 6-month summer internship with top companies
            - **Placement**: 100% placement record with average package 8-12 LPA
            """)
        
        else:
            pg_commerce = {
                'Course': ['M.Com', 'M.Com (Accounting)', 'M.Com (Finance)', 'M.Phil Commerce', 'PhD Commerce'],
                'Duration': ['2 Years', '2 Years', '2 Years', '1 Year', '3-5 Years'],
                'Seats': [40, 30, 30, 15, 10],
                'Fee/Year (₹)': [85000, 90000, 90000, 95000, 100000],
                'Specialization': ['General', 'Taxation', 'Investment Analysis', 'Research', 'Advanced Research']
            }
            df_pg_commerce = pd.DataFrame(pg_commerce)
            st.dataframe(df_pg_commerce, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Commerce PG Programs
            - **Advanced Accounting**: Focus on IFRS and US GAAP
            - **Financial Analysis**: Deep dive into corporate finance
            - **Research Orientation**: Preparation for academic and research careers
            - **Professional Certification**: Integration with CA, CS, CFA curriculum
            """)

    with tab4:
        st.subheader("Specializations & Electives")
        
        st.markdown("""
        ### Interdisciplinary Specializations
        
        **Data Science**
        - Available for: B.Tech CSE, M.Sc Mathematics, M.Sc Computer Science
        - Focus: Machine Learning, Big Data, Analytics
        
        **Biotechnology**
        - Available for: B.Sc Biology, M.Sc Biotechnology, B.Tech Biomedical
        - Focus: Genetic Engineering, Bioinformatics, Pharmaceutical Tech
        
        **Environmental Science**
        - Available for: B.Sc Chemistry, B.Sc Physics, Environmental Engineering
        - Focus: Climate Change, Sustainability, Renewable Energy
        
        **Digital Marketing**
        - Available for: BBA, MBA, B.Com, M.Com
        - Focus: SEO, Social Media Marketing, E-commerce
        """)
        
        st.subheader("Elective Course Distribution")
        elective_data = {
            'Category': ['Technical', 'Management', 'Humanities', 'Open Elective'],
            'UG Credits': [20, 15, 10, 8],
            'PG Credits': [18, 16, 8, 6]
        }
        df_elective = pd.DataFrame(elective_data)
        
        fig_elective = px.bar(df_elective, x='Category', y=['UG Credits', 'PG Credits'],
                             title="Credit Distribution for Electives",
                             barmode='group', color_discrete_sequence=['#6d28d9', '#8b5cf6'])
        st.plotly_chart(fig_elective, width='stretch')

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask About Specific Course", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "I need detailed information about a specific course"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()


