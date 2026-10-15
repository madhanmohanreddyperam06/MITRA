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

    st.title("💼 Placements & Training")

    # Key statistics row
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Placement Rate", "92%")
    with metric_col2:
        st.metric("Highest Package", "₹32 LPA")
    with metric_col3:
        st.metric("Average Package", "₹7.5 LPA")
    with metric_col4:
        st.metric("Visiting Companies", "180+")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "🏢 Top Recruiters", "📚 Training", "📈 Year-wise Trends"])

    with tab1:
        st.subheader("Placement Statistics by Department")
        
        dept_stats = {
            'Department': ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Electrical', 'MBA'],
            'Placement Rate (%)': [95, 90, 85, 80, 82, 94],
            'Highest Package (LPA)': [32, 28, 22, 18, 20, 25],
            'Average Package (LPA)': [9.5, 7.8, 6.2, 5.5, 6.0, 8.5],
            'Students Placed': [115, 95, 70, 58, 60, 58]
        }
        df_dept = pd.DataFrame(dept_stats)
        st.dataframe(df_dept, width='stretch', hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_placement_rate = px.bar(df_dept, x='Department', y='Placement Rate (%)',
                                      title="Placement Rate by Department",
                                      color='Placement Rate (%)', color_continuous_scale='Purples')
            st.plotly_chart(fig_placement_rate, width='stretch')
        
        with col2:
            fig_packages = px.bar(df_dept, x='Department', y=['Highest Package (LPA)', 'Average Package (LPA)'],
                                title="Package Statistics by Department",
                                barmode='group', color_discrete_sequence=['#6d28d9', '#8b5cf6'])
            st.plotly_chart(fig_packages, width='stretch')
        
        st.subheader("Package Distribution")
        package_distribution = {
            'Package Range (LPA)': ['< 5', '5-8', '8-12', '12-15', '15-20', '20-25', '> 25'],
            'Number of Students': [45, 120, 180, 95, 60, 40, 25],
            'Percentage': [8, 21, 32, 17, 11, 7, 4]
        }
        df_package = pd.DataFrame(package_distribution)
        
        fig_package_dist = px.bar(df_package, x='Package Range (LPA)', y='Number of Students',
                                title="Package Distribution",
                                color='Number of Students', color_continuous_scale='Purples')
        st.plotly_chart(fig_package_dist, width='stretch')

    with tab2:
        st.subheader("Top Recruiters by Sector")
        
        sector = st.selectbox("Select Sector", ["Product & Tech", "IT & Consulting", "Core & Manufacturing", "Finance & Analytics"])
        
        if sector == "Product & Tech":
            tech_companies = {
                'Company': ['Amazon', 'Google', 'Microsoft', 'Adobe', 'Oracle', 'Salesforce', 'Flipkart', 'Uber'],
                'Offers': [25, 15, 20, 12, 10, 8, 15, 10],
                'Avg Package (LPA)': [18, 25, 20, 16, 14, 15, 17, 19],
                'Designations': ['SDE-1/2', 'Software Engineer', 'SDE', 'Software Engineer', 'Developer', 'Sales Dev', 'SDE', 'SDE']
            }
            df_tech = pd.DataFrame(tech_companies)
            st.dataframe(df_tech, width='stretch', hide_index=True)
            
            fig_tech = px.scatter(df_tech, x='Offers', y='Avg Package (LPA)', size='Offers',
                                hover_name='Company', title="Tech Companies: Offers vs Package",
                                color='Avg Package (LPA)', color_continuous_scale='Purples')
            st.plotly_chart(fig_tech, width='stretch')
        
        elif sector == "IT & Consulting":
            it_companies = {
                'Company': ['TCS', 'Infosys', 'Wipro', 'Cognizant', 'Accenture', 'Capgemini', 'HCL Tech', 'Tech Mahindra'],
                'Offers': [80, 75, 65, 55, 50, 45, 40, 35],
                'Avg Package (LPA)': [5.5, 6.0, 5.8, 6.5, 7.0, 6.2, 5.9, 5.7],
                'Designations': ['System Engineer', 'Systems Engineer', 'Project Engineer', 'Programmer Analyst', 'Analyst', 'Consultant', 'Software Engineer', 'Associate Engineer']
            }
            df_it = pd.DataFrame(it_companies)
            st.dataframe(df_it, width='stretch', hide_index=True)
            
            fig_it = px.bar(df_it, x='Company', y='Offers',
                          title="IT Companies: Number of Offers",
                          color='Offers', color_continuous_scale='Purples')
            st.plotly_chart(fig_it, width='stretch')
        
        elif sector == "Core & Manufacturing":
            core_companies = {
                'Company': ['L&T', 'Tata Motors', 'Bosch', 'Siemens', 'Mahindra', 'ABB', 'Schneider', 'Godrej'],
                'Offers': [25, 20, 18, 15, 15, 12, 10, 10],
                'Avg Package (LPA)': [8.5, 7.5, 9.0, 8.0, 7.0, 8.5, 7.5, 7.0],
                'Designations': ['Graduate Engineer', 'GET', 'Graduate Trainee', 'Engineer', 'GET', 'Engineer', 'Engineer', 'GET']
            }
            df_core = pd.DataFrame(core_companies)
            st.dataframe(df_core, width='stretch', hide_index=True)
        
        else:
            finance_companies = {
                'Company': ['Deloitte', 'EY', 'HDFC Bank', 'ICICI', 'KPMG', 'PwC', 'Goldman Sachs', 'JPMorgan'],
                'Offers': [35, 30, 25, 22, 20, 18, 12, 10],
                'Avg Package (LPA)': [9.0, 9.5, 8.0, 7.5, 10.0, 9.8, 18, 16],
                'Designations': ['Analyst', 'Consultant', 'Analyst', 'Analyst', 'Associate', 'Associate', 'Analyst', 'Analyst']
            }
            df_finance = pd.DataFrame(finance_companies)
            st.dataframe(df_finance, width='stretch', hide_index=True)
            
            fig_finance = px.scatter(df_finance, x='Offers', y='Avg Package (LPA)', size='Offers',
                                   hover_name='Company', title="Finance Companies: Offers vs Package",
                                   color='Avg Package (LPA)', color_continuous_scale='Purples')
            st.plotly_chart(fig_finance, width='stretch')

    with tab3:
        st.subheader("Training & Career Development Programs")
        
        training_data = {
            'Program': ['Coding Bootcamp', 'Aptitude Training', 'Mock Interviews', 'GD Preparation', 
                       'Resume Building', 'Technical Skills', 'Soft Skills', 'Industry Visits'],
            'Duration (Hours)': [60, 40, 20, 15, 10, 50, 30, 40],
            'Students Trained': [450, 550, 480, 520, 500, 420, 550, 400],
            'Success Rate (%)': [85, 90, 88, 82, 95, 80, 85, 75]
        }
        df_training = pd.DataFrame(training_data)
        st.dataframe(df_training, width='stretch', hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_training_hours = px.bar(df_training, x='Program', y='Duration (Hours)',
                                      title="Training Duration by Program",
                                      color='Duration (Hours)', color_continuous_scale='Purples')
            st.plotly_chart(fig_training_hours, width='stretch')
        
        with col2:
            fig_training_success = px.bar(df_training, x='Program', y='Success Rate (%)',
                                        title="Training Success Rate",
                                        color='Success Rate (%)', color_continuous_scale='Purples')
            st.plotly_chart(fig_training_success, width='stretch')
        
        st.markdown("""
        ### Training Schedule
        - **Semester 3-4**: Foundation training (Aptitude, Coding basics)
        - **Semester 5-6**: Advanced training (Domain-specific, Mock interviews)
        - **Semester 7-8**: Placement preparation (Company-specific training)
        
        ### Placement Cell Office
        - **Placement Officer**: Dr. Anderson
        - **Office**: Career Development Center (CDC), Block B
        - **Email**: placements@college.edu
        - **Phone**: +91-123-456-7894
        - **Timings**: Monday-Friday, 9 AM to 6 PM
        """)

    with tab4:
        st.subheader("Year-wise Placement Trends")
        
        year_data = {
            'Year': ['2020', '2021', '2022', '2023', '2024'],
            'Placement Rate (%)': [78, 82, 85, 89, 92],
            'Highest Package (LPA)': [18, 20, 24, 28, 32],
            'Average Package (LPA)': [5.2, 5.8, 6.5, 7.0, 7.5],
            'Companies Visited': [120, 135, 150, 165, 180]
        }
        df_year = pd.DataFrame(year_data)
        st.dataframe(df_year, width='stretch', hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_year_rate = px.line(df_year, x='Year', y='Placement Rate (%)',
                                  title="Placement Rate Trend",
                                  markers=True, line_shape='linear')
            fig_year_rate.update_traces(line_color='#6d28d9')
            st.plotly_chart(fig_year_rate, width='stretch')
        
        with col2:
            fig_year_companies = px.line(df_year, x='Year', y='Companies Visited',
                                        title="Companies Visited Trend",
                                        markers=True, line_shape='linear')
            fig_year_companies.update_traces(line_color='#8b5cf6')
            st.plotly_chart(fig_year_companies, width='stretch')
        
        fig_year_packages = px.line(df_year, x='Year', y=['Highest Package (LPA)', 'Average Package (LPA)'],
                                   title="Package Trends",
                                   markers=True, line_shape='linear')
        fig_year_packages.update_traces(line_color=['#6d28d9', '#8b5cf6'])
        st.plotly_chart(fig_year_packages, width='stretch')

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask About Placements", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user",
            "content": "I need detailed information about placements and training"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
