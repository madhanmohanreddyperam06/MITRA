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

    st.title("💰 Fees & Scholarships")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Fee Structure", "🎓 Scholarships", "💳 Payment", "📊 Cost Calculator"])

    with tab1:
        st.subheader("Program-wise Fee Structure")
        
        program_level = st.selectbox("Select Program Level", ["Undergraduate", "Postgraduate"])
        
        if program_level == "Undergraduate":
            ug_fees = {
                'Program': ['B.Tech CSE', 'B.Tech ECE', 'B.Tech Mechanical', 'B.Tech Civil', 
                          'B.Sc Physics', 'B.Sc Chemistry', 'B.Com', 'BBA', 'BA English'],
                'Tuition Fee/Year (₹)': [150000, 145000, 140000, 135000, 80000, 80000, 75000, 85000, 60000],
                'Duration (Years)': [4, 4, 4, 4, 3, 3, 3, 3, 3],
                'Total Fee (₹)': [600000, 580000, 560000, 540000, 240000, 240000, 225000, 255000, 180000]
            }
            df_ug = pd.DataFrame(ug_fees)
            st.dataframe(df_ug, width='stretch', hide_index=True)
            
            fig_ug = px.bar(df_ug, x='Program', y='Total Fee (₹)',
                          title="Total Program Fee (UG)",
                          color='Total Fee (₹)', color_continuous_scale='Purples')
            st.plotly_chart(fig_ug, width='stretch')
            
            st.markdown("""
            ### Additional Fees (Annual)
            - **Hostel**: ₹80,000 (optional)
            - **Mess**: ₹40,000 (optional)
            - **Library & Lab**: ₹10,000
            - **Exam Fee**: ₹5,000
            - **Insurance**: ₹2,000
            - **Total Additional**: ₹137,000 (₹47,000 without hostel)
            """)
        
        else:
            pg_fees = {
                'Program': ['M.Tech CSE', 'M.Tech ECE', 'M.Tech Mechanical', 'M.Sc Physics', 
                          'M.Sc Chemistry', 'MBA', 'M.Com', 'M.Phil'],
                'Tuition Fee/Year (₹)': [180000, 175000, 170000, 90000, 90000, 200000, 85000, 95000],
                'Duration (Years)': [2, 2, 2, 2, 2, 2, 2, 1],
                'Total Fee (₹)': [360000, 350000, 340000, 180000, 180000, 400000, 170000, 95000]
            }
            df_pg = pd.DataFrame(pg_fees)
            st.dataframe(df_pg, width='stretch', hide_index=True)
            
            fig_pg = px.bar(df_pg, x='Program', y='Total Fee (₹)',
                          title="Total Program Fee (PG)",
                          color='Total Fee (₹)', color_continuous_scale='Purples')
            st.plotly_chart(fig_pg, width='stretch')
            
            st.markdown("""
            ### Additional Fees (Annual)
            - **Hostel**: ₹90,000 (optional)
            - **Mess**: ₹45,000 (optional)
            - **Library & Lab**: ₹15,000
            - **Exam Fee**: ₹6,000
            - **Thesis Fee**: ₹10,000 (PG only)
            - **Total Additional**: ₹166,000 (₹31,000 without hostel)
            """)

    with tab2:
        st.subheader("Scholarship Programs")
        
        scholarship_data = {
            'Scholarship Type': ['Merit-Based (100%)', 'Merit-Based (75%)', 'Merit-Based (50%)', 
                               'Need-Based', 'Sports Excellence', 'Cultural Excellence', 
                               'Alumni Scholarship', 'Research Grant'],
            'Coverage': ['Full Tuition', '75% Tuition', '50% Tuition', 
                        'Up to 50% Tuition', 'Up to 50% Tuition', 'Up to 50% Tuition',
                        '20% Tuition', '₹50,000-₹2,00,000'],
            'Eligibility': ['Top 5% in Entrance', 'Top 10% in Entrance', 'Top 15% in Entrance',
                          'Family Income < ₹2.5L', 'State/National Medalist', 'State/National Medalist',
                          'Alumni Children', 'Research Scholars'],
            'Number Awarded': [25, 50, 75, 100, 30, 20, 50, 40]
        }
        df_scholarship = pd.DataFrame(scholarship_data)
        st.dataframe(df_scholarship, width='stretch', hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_scholarship_count = px.bar(df_scholarship, x='Scholarship Type', y='Number Awarded',
                                         title="Number of Scholarships Awarded",
                                         color='Number Awarded', color_continuous_scale='Purples')
            st.plotly_chart(fig_scholarship_count, width='stretch')
        
        with col2:
            fig_scholarship_coverage = px.pie(df_scholarship, values='Number Awarded', names='Scholarship Type',
                                            title="Scholarship Distribution",
                                            color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa', 
                                                                    '#c4b5fd', '#7c3aed', '#5b21b6',
                                                                    '#8b5cf6', '#a78bfa'])
            st.plotly_chart(fig_scholarship_coverage, width='stretch')
        
        st.markdown("""
        ### Scholarship Application Process
        1. **Application**: Submit scholarship form with required documents
        2. **Verification**: College verifies eligibility criteria
        3. **Interview**: Need-based scholarships require interview
        4. **Approval**: Scholarship committee approves deserving candidates
        5. **Disbursement**: Fee waiver applied in next semester
        
        ### Required Documents
        - Income certificate (for need-based)
        - Sports certificates (for sports scholarship)
        - Cultural achievement certificates
        - Entrance exam rank card (for merit-based)
        - Previous academic records
        """)

    with tab3:
        st.subheader("Payment Methods & Schedule")
        
        st.markdown("""
        ### Payment Methods
        - **Online Portal**: Credit Cards, Debit Cards, Net Banking, UPI
        - **Bank Transfer**: NEFT/RTGS/IMPS to college account
        - **Demand Draft**: In favor of College Registrar
        - **Cash**: At college counter (not recommended)
        
        ### Payment Schedule
        - **Semester 1**: Before July 15th
        - **Semester 2**: Before December 15th
        - **Late Fee**: ₹1,000 per month after deadline
        """)
        
        payment_schedule = {
            'Installment': ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 
                          'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8'],
            'Due Date': ['July 15', 'Dec 15', 'July 15', 'Dec 15', 
                       'July 15', 'Dec 15', 'July 15', 'Dec 15'],
            'Amount (₹)': [150000, 150000, 150000, 150000, 150000, 150000, 150000, 150000],
            'Status': ['Open', 'Upcoming', 'Upcoming', 'Upcoming', 'Upcoming', 'Upcoming', 'Upcoming', 'Upcoming']
        }
        df_payment = pd.DataFrame(payment_schedule)
        st.dataframe(df_payment, width='stretch', hide_index=True)
        
        st.markdown("""
        ### Installment Facility
        - **Available**: On prior application
        - **Processing Fee**: ₹500
        - **Split**: 2 installments per semester
        - **First Installment**: 60% before semester start
        - **Second Installment**: 40% before mid-semester
        """)

    with tab4:
        st.subheader("Total Cost Calculator")
        
        col1, col2 = st.columns(2)
        with col1:
            program = st.selectbox("Select Program", 
                                  ['B.Tech CSE', 'B.Tech ECE', 'B.Tech Mechanical', 'B.Sc Physics', 
                                   'B.Com', 'BBA', 'M.Tech CSE', 'MBA'])
            duration = st.number_input("Duration (Years)", min_value=1, max_value=5, value=4)
            hostel_required = st.checkbox("Require Hostel Accommodation")
            mess_required = st.checkbox("Require Mess Facility")
        
        with col2:
            scholarship_percent = st.slider("Scholarship Percentage", 0, 100, 0)
            scholarship_type = st.selectbox("Scholarship Type", 
                                         ['None', 'Merit-Based', 'Need-Based', 'Sports', 'Cultural'])
        
        # Fee calculation
        fee_map = {
            'B.Tech CSE': 150000, 'B.Tech ECE': 145000, 'B.Tech Mechanical': 140000,
            'B.Sc Physics': 80000, 'B.Com': 75000, 'BBA': 85000,
            'M.Tech CSE': 180000, 'MBA': 200000
        }
        
        base_fee = fee_map[program] * duration
        hostel_fee = 80000 * duration if hostel_required else 0
        mess_fee = 40000 * duration if mess_required else 0
        additional_fees = 17000 * duration  # Library, lab, exam, insurance
        
        total_before_scholarship = base_fee + hostel_fee + mess_fee + additional_fees
        scholarship_amount = (base_fee * scholarship_percent) / 100
        total_after_scholarship = total_before_scholarship - scholarship_amount
        
        st.markdown("---")
        st.subheader("Cost Breakdown")
        
        cost_data = {
            'Component': ['Tuition Fee', 'Hostel', 'Mess', 'Additional Fees', 'Scholarship', 'Total Cost'],
            'Amount (₹)': [base_fee, hostel_fee, mess_fee, additional_fees, -scholarship_amount, total_after_scholarship]
        }
        df_cost = pd.DataFrame(cost_data)
        st.dataframe(df_cost, width='stretch', hide_index=True)
        
        # Visual breakdown
        components = ['Tuition', 'Hostel', 'Mess', 'Additional']
        values = [base_fee, hostel_fee, mess_fee, additional_fees]
        values = [v for v in values if v > 0]
        components = [c for c, v in zip(components, values) if v > 0]
        
        fig_cost = px.pie(values=values, names=components, title="Cost Distribution",
                         color_discrete_sequence=['#6d28d9', '#8b5cf6', '#a78bfa', '#c4b5fd'])
        st.plotly_chart(fig_cost, width='stretch')
        
        st.success(f"💰 **Total Estimated Cost: ₹{total_after_scholarship:,.0f}**")

    # Interactive Ask Button
    st.markdown("---")
    if st.button("💬 Ask About Fees & Scholarships", width='stretch', type="primary"):
        st.session_state.messages.append({
            "role": "user",
            "content": "I need detailed information about fee structure and scholarships"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
