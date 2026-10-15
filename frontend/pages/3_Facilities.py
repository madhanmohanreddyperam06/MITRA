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

    st.title("🏫 Campus Facilities")

    # Overview Dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📖 Library", "🏠 Hostels", "⚽ Sports", "🔬 Labs"])

    with tab1:
        st.subheader("Campus Infrastructure Overview")
        
        facility_data = {
            'Facility': ['Library', 'Hostels', 'Sports Complex', 'Laboratories', 'Auditorium', 'Cafeteria'],
            'Area (sq ft)': [25000, 50000, 45000, 30000, 15000, 8000],
            'Capacity': [500, 2000, 1500, 800, 2000, 500],
            'Investment (₹ Lakhs)': [500, 2000, 1500, 3000, 800, 300]
        }
        df_facility = pd.DataFrame(facility_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_area = px.bar(df_facility, x='Facility', y='Area (sq ft)',
                           title="Facility Area Distribution",
                           color='Area (sq ft)', color_continuous_scale='Purples')
            st.plotly_chart(fig_area, width='stretch')
        
        with col2:
            fig_capacity = px.pie(df_facility, values='Capacity', names='Facility',
                                 title="Total Capacity Distribution",
                                 color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa', 
                                                         '#c4b5fd', '#7c3aed', '#5b21b6'])
            st.plotly_chart(fig_capacity, width='stretch')
        
        st.subheader("Facility Statistics")
        st.dataframe(df_facility, width='stretch', hide_index=True)

    with tab2:
        st.subheader("📖 Central Library")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Library Resources
            - **Books**: 50,000+ volumes across all disciplines
            - **Journals**: 200+ national and international journals
            - **E-Resources**: Access to IEEE, Springer, Elsevier databases
            - **Newspapers**: 50+ daily newspapers and magazines
            - **Audio-Visual**: 1000+ CDs and DVDs
            
            ### Sections
            - Reference Section
            - Circulation Section
            - Digital Library
            - Reading Rooms (Air-conditioned)
            - Group Study Rooms
            - Research Scholar Room
            """)
        
        with col2:
            library_stats = {
                'Category': ['Books', 'Journals', 'E-Books', 'CDs/DVDs', 'Seats'],
                'Count': [50000, 200, 15000, 1000, 500]
            }
            df_library = pd.DataFrame(library_stats)
            
            fig_library = px.bar(df_library, x='Category', y='Count',
                               title="Library Resource Statistics",
                               color='Count', color_continuous_scale='Purples')
            st.plotly_chart(fig_library, width='stretch')
        
        st.markdown("""
        ### Library Services
        - **Issue Duration**: 15 days for UG, 30 days for PG
        - **Renewal**: 2 times (if no reservation)
        - **Fine**: ₹1 per day per book
        - **Timings**: Monday-Saturday, 8 AM to 8 PM
        - **Online Catalog**: OPAC system for book search
        - **Inter-library Loan**: Access to other libraries
        """)

    with tab3:
        st.subheader("🏠 Hostel Accommodation")
        
        hostel_type = st.selectbox("Select Hostel", ["Boys Hostel", "Girls Hostel"])
        
        if hostel_type == "Boys Hostel":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Boys Hostel Facilities
                - **Total Rooms**: 500
                - **Capacity**: 1500 students
                - **Room Types**: Single, Double, Triple
                - **Wi-Fi**: 24/7 high-speed internet
                - **Mess**: Central mess with nutritious food
                - **Security**: 24/7 CCTV surveillance
                - **Laundry**: In-house laundry service
                - **Recreation**: TV room, games room
                
                ### Amenities
                - Attached bathrooms
                - 24/7 hot water
                - Study tables and chairs
                - Wardrobe
                - Bed with mattress
                """)
            
            with col2:
                boys_hostel_data = {
                    'Room Type': ['Single', 'Double', 'Triple'],
                    'Number of Rooms': [100, 200, 200],
                    'Fee/Year (₹)': [120000, 80000, 60000],
                    'Occupancy': [95, 90, 85]
                }
                df_boys = pd.DataFrame(boys_hostel_data)
                st.dataframe(df_boys, width='stretch', hide_index=True)
                
                fig_boys = px.pie(df_boys, values='Number of Rooms', names='Room Type',
                                title="Room Type Distribution",
                                color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa'])
                st.plotly_chart(fig_boys, width='stretch')
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Girls Hostel Facilities
                - **Total Rooms**: 300
                - **Capacity**: 900 students
                - **Room Types**: Single, Double, Triple
                - **Wi-Fi**: 24/7 high-speed internet
                - **Mess**: Central mess with nutritious food
                - **Security**: 24/7 security guard + CCTV
                - **Laundry**: In-house laundry service
                - **Recreation**: TV room, reading room
                
                ### Special Features
                - Ladies warden available 24/7
                - Medical room with first aid
                - Prayer room
                - Beauty parlor
                - Gynecologist visit weekly
                """)
            
            with col2:
                girls_hostel_data = {
                    'Room Type': ['Single', 'Double', 'Triple'],
                    'Number of Rooms': [60, 120, 120],
                    'Fee/Year (₹)': [130000, 90000, 70000],
                    'Occupancy': [98, 95, 90]
                }
                df_girls = pd.DataFrame(girls_hostel_data)
                st.dataframe(df_girls, width='stretch', hide_index=True)
                
                fig_girls = px.pie(df_girls, values='Number of Rooms', names='Room Type',
                                title="Room Type Distribution",
                                color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa'])
                st.plotly_chart(fig_girls, width='stretch')

    with tab4:
        st.subheader("⚽ Sports & Recreation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Outdoor Sports
            - **Cricket Ground**: International standard
            - **Football Field**: FIFA standard
            - **Basketball Courts**: 3 cement courts
            - **Tennis Courts**: 2 clay courts
            - **Volleyball Courts**: 4 courts
            - **Athletics Track**: 400m synthetic track
            
            ### Indoor Sports
            - **Badminton**: 4 wooden courts
            - **Table Tennis**: 8 tables
            - **Chess/Carrom**: Dedicated room
            - **Gymnasium**: Modern equipment
            - **Yoga Room**: Meditation space
            """)
        
        with col2:
            sports_data = {
                'Sport': ['Cricket', 'Football', 'Basketball', 'Badminton', 'Table Tennis', 'Athletics'],
                'Teams': [4, 4, 6, 8, 10, 1],
                'Coaches': [2, 2, 2, 2, 1, 3],
                'Awards Won': [15, 12, 10, 18, 14, 8]
            }
            df_sports = pd.DataFrame(sports_data)
            
            fig_sports = px.bar(df_sports, x='Sport', y=['Teams', 'Coaches', 'Awards Won'],
                              title="Sports Department Statistics",
                              barmode='group', color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa'])
            st.plotly_chart(fig_sports, width='stretch')
        
        st.markdown("""
        ### Additional Facilities
        - **Swimming Pool**: Olympic size (50m x 25m)
        - **Multipurpose Hall**: For indoor games and events
        - **Equipment Room**: Sports equipment available on request
        - **Coach Availability**: Professional coaches for all sports
        - **Annual Sports Meet**: Inter-college competitions
        """)

    with tab5:
        st.subheader("🔬 Laboratory Facilities")
        
        lab_type = st.selectbox("Select Lab Category", ["Computer Labs", "Science Labs", "Engineering Labs", "Research Centers"])
        
        if lab_type == "Computer Labs":
            comp_labs = {
                'Lab Name': ['Main Lab', 'Programming Lab', 'AI/ML Lab', 'Network Lab', 'Graphics Lab'],
                'Systems': [100, 80, 50, 40, 30],
                'Software': ['All', 'All', 'Python/TensorFlow', 'Cisco Packet Tracer', 'AutoCAD/Matlab'],
                'Specialization': ['General Purpose', 'Programming', 'AI Projects', 'Networking', 'Design']
            }
            df_comp = pd.DataFrame(comp_labs)
            st.dataframe(df_comp, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Computer Lab Features
            - **OS**: Windows 11 & Linux (Dual Boot)
            - **Internet**: 1 Gbps dedicated line
            - **Backup**: UPS + Generator backup
            - **Timing**: 8 AM to 10 PM (all days)
            - **Printers**: Laser printers available
            """)
        
        elif lab_type == "Science Labs":
            science_labs = {
                'Lab': ['Physics Lab', 'Chemistry Lab', 'Biology Lab', 'Biotechnology Lab'],
                'Equipment': ['Advanced optical instruments', 'Spectrophotometer, Chromatography', 'Microscopes, PCR', 'Fermenters, Centrifuges'],
                'Students/Batch': [30, 25, 25, 20],
                'Research Projects': [15, 12, 18, 20]
            }
            df_science_labs = pd.DataFrame(science_labs)
            st.dataframe(df_science_labs, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Science Lab Highlights
            - **Safety**: Fully equipped with safety equipment
            - **Modern Equipment**: State-of-the-art instruments
            - **Research**: UG and PG research projects
            - **Staff**: Dedicated lab technicians
            """)
        
        elif lab_type == "Engineering Labs":
            eng_labs = {
                'Department': ['Mechanical', 'Electrical', 'Civil', 'ECE'],
                'Labs': [8, 6, 7, 6],
                'Machines/Equipment': ['CNC, Lathe, Milling', 'Transformers, Motors', 'UTM, Surveying', 'Oscilloscopes, Signal Generators'],
                'Software': ['AutoCAD, SolidWorks', 'MATLAB, Simulink', 'STAAD, Revit', 'MATLAB, Cadence']
            }
            df_eng_labs = pd.DataFrame(eng_labs)
            st.dataframe(df_eng_labs, width='stretch', hide_index=True)
            
            st.markdown("""
            ### Engineering Lab Excellence
            - **Industry Standard**: Equipment matching industry standards
            - **Project Work**: Final year project facilities
            - **Consultancy**: Industry consultancy projects
            - **Training**: Short-term training programs
            """)
        
        else:
            research_centers = {
                'Center': ['AI Research Lab', 'IoT Lab', 'Material Science Lab', 'Energy Research Lab'],
                'Faculty': [8, 6, 5, 4],
                'Projects': [25, 18, 15, 12],
                'Funding (₹ Lakhs)': [200, 150, 120, 100]
            }
            df_research = pd.DataFrame(research_centers)
            st.dataframe(df_research, width='stretch', hide_index=True)
            
            fig_research = px.bar(df_research, x='Center', y='Funding (₹ Lakhs)',
                                title="Research Funding Distribution",
                                color='Funding (₹ Lakhs)', color_continuous_scale='Purples')
            st.plotly_chart(fig_research, width='stretch')
            
            st.markdown("""
            ### Research Center Features
            - **Publications**: High-impact journal publications
            - **Collaborations**: National and international collaborations
            - **Patents**: Patent filing support
            - **PhD Programs**: Doctoral research facilities
            """)

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask About Specific Facility", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "I need detailed information about campus facilities"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()


