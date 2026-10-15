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

    st.title("📋 Admissions Information")

    # Program Overview with Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎓 Programs", "📅 Timeline", "📄 Documents"])

    with tab1:
        st.subheader("Admission Statistics")
        
        # Sample data for visualization
        stats_data = {
            'Year': ['2021', '2022', '2023', '2024'],
            'Applications': [4500, 5200, 6100, 6800],
            'Admissions': [1200, 1350, 1500, 1650]
        }
        df_stats = pd.DataFrame(stats_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(df_stats, x='Year', y=['Applications', 'Admissions'],
                           title="Applications vs Admissions Trend",
                           barmode='group', color_discrete_sequence=['#6d28d9', '#8b5cf6'])
            st.plotly_chart(fig_bar, width='stretch')
        
        with col2:
            fig_pie = px.pie(values=[df_stats['Applications'].sum(), df_stats['Admissions'].sum()],
                            names=['Total Applications', 'Total Admissions'],
                            title="Success Rate Overview",
                            color_discrete_sequence=['#6d28d9', '#8b5cf6'])
            st.plotly_chart(fig_pie, width='stretch')
        
        # Success rate table
        df_stats['Success Rate (%)'] = (df_stats['Admissions'] / df_stats['Applications'] * 100).round(2)
        st.subheader("Year-wise Success Rate")
        st.dataframe(df_stats[['Year', 'Applications', 'Admissions', 'Success Rate (%)']], 
                    width='stretch', hide_index=True)

    with tab2:
        st.subheader("Program Details")
        
        program_type = st.selectbox("Select Program Type", ["Undergraduate", "Postgraduate"])
        
        if program_type == "Undergraduate":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Eligibility Criteria
                - **Academic**: 12th standard with minimum 60% marks
                - **Stream**: Science, Commerce, or Arts
                - **Age**: 17-25 years
                - **Nationality**: Indian citizens & NRI eligible
                
                ### Entrance Requirements
                - College Entrance Test (CET) - 60% weightage
                - 12th Grade Marks - 30% weightage
                - Interview - 10% weightage
                """)
            
            with col2:
                ug_programs = {
                    'Program': ['B.Tech CSE', 'B.Tech ECE', 'B.Tech Mech', 'B.Sc Physics', 'B.Com', 'BBA'],
                    'Seats': [120, 100, 80, 60, 80, 60],
                    'Fee (₹)': [150000, 145000, 140000, 80000, 75000, 85000],
                    'Duration (Years)': [4, 4, 4, 3, 3, 3]
                }
                df_ug = pd.DataFrame(ug_programs)
                st.subheader("Undergraduate Programs & Seats")
                st.dataframe(df_ug, width='stretch', hide_index=True)
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### Eligibility Criteria
                - **Academic**: Bachelor's degree with minimum 55% marks
                - **GATE Score**: Valid GATE score (for engineering)
                - **Work Experience**: 0-2 years preferred
                - **Research**: Research proposal required for M.Tech research
                
                ### Specializations Available
                - Computer Science & Engineering
                - Electronics & Communication
                - Mechanical Engineering
                - Applied Sciences
                - Business Administration
                """)
            
            with col2:
                pg_programs = {
                    'Program': ['M.Tech CSE', 'M.Tech ECE', 'M.Sc Physics', 'MBA', 'M.Com'],
                    'Seats': [40, 35, 30, 60, 40],
                    'Fee (₹)': [180000, 175000, 90000, 200000, 85000],
                    'Duration (Years)': [2, 2, 2, 2, 2]
                }
                df_pg = pd.DataFrame(pg_programs)
                st.subheader("Postgraduate Programs & Seats")
                st.dataframe(df_pg, width='stretch', hide_index=True)

    with tab3:
        st.subheader("Important Admission Timeline")
        
        # Timeline data
        timeline_data = {
            'Event': ['Application Opens', 'Early Bird Deadline', 'Regular Deadline', 
                     'Entrance Test', 'Result Declaration', 'Counseling Starts', 
                     'Counseling Ends', 'Classes Begin'],
            'Date': ['March 1st', 'April 15th', 'June 30th', 'July 15th', 
                    'July 30th', 'August 1st', 'August 15th', 'September 1st'],
            'Status': ['Completed', 'Completed', 'Upcoming', 'Upcoming', 
                     'Upcoming', 'Upcoming', 'Upcoming', 'Upcoming']
        }
        df_timeline = pd.DataFrame(timeline_data)
        
        # Color-coded status
        def highlight_status(val):
            if val == 'Completed':
                return 'background-color: #065f46'
            elif val == 'Upcoming':
                return 'background-color: #7c2d12'
            return ''
        
        styled_timeline = df_timeline.style.map(highlight_status, subset=['Status'])
        st.dataframe(styled_timeline, width='stretch', hide_index=True)
        
        # Gantt-style timeline visualization
        st.subheader("Visual Timeline")
        fig_timeline = go.Figure()
        
        events = ['Application Opens', 'Early Bird', 'Regular Deadline', 
                 'Entrance Test', 'Results', 'Counseling', 'Classes Begin']
        dates = [1, 2, 3, 4, 5, 6, 7]  # Simplified months
        
        fig_timeline.add_trace(go.Scatter(
            x=dates,
            y=events,
            mode='markers+lines',
            marker=dict(size=20, color='#6d28d9'),
            line=dict(color='#8b5cf6', width=3),
            name='Timeline'
        ))
        
        fig_timeline.update_layout(
            title="Admission Process Timeline",
            xaxis_title="Timeline",
            yaxis_title="Events",
            height=400
        )
        st.plotly_chart(fig_timeline, width='stretch')

    with tab4:
        st.subheader("Required Documents Checklist")
        
        document_checklist = {
            'Document': ['10th Marksheet', '12th Marksheet', 'Degree Certificate', 
                        'Transfer Certificate', 'Migration Certificate', 
                        'Entrance Exam Score Card', 'GATE Score (if applicable)',
                        'Category Certificate', 'Income Certificate', 
                        'Passport Size Photos', 'Aadhar Card', 'PAN Card'],
            'Required': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Conditional', 
                        'Conditional', 'Conditional', 'Yes', 'Yes', 'Yes'],
            'Format': ['Original + 2 copies', 'Original + 2 copies', 'Original + 2 copies',
                      'Original', 'Original', 'Original', 'Original', 'Original',
                      'Original', '6 copies', 'Original', 'Original']
        }
        df_docs = pd.DataFrame(document_checklist)
        
        st.dataframe(df_docs, width='stretch', hide_index=True)
        
        st.markdown("""
        ### Document Submission Guidelines
        - All documents must be self-attested
        - Original documents verified at time of admission
        - Digital copies can be uploaded online for preliminary verification
        - Scanned documents should be in PDF format (max 2MB each)
        - Foreign students need additional documents (passport, visa)
        """)

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask Specific Admission Question", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "I have a specific question about admissions"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()


