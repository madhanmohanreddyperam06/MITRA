import streamlit as st

def show():
    st.title("📋 Admissions Information")

    st.markdown(""""
    ## Admission Process

    ### Undergraduate Programs
    - **Eligibility**: 12th standard with minimum 60% marks
    - **Entrance Test**: College entrance exam or national level exams
    - **Application Period**: March - June

    ### Postgraduate Programs  
    - **Eligibility**: Bachelor's degree with minimum 55% marks
    - **Entrance Test**: Graduate aptitude test
    - **Application Period**: April - July

    ### Documents Required
    - Academic transcripts
    - Entrance test scores
    - Identity proof
    - Passport size photographs
    - Category certificate (if applicable)

    ### Important Dates
    - Application Start: March 1st
    - Last Date to Apply: June 30th
    - Entrance Test: July 15th
    - Result Declaration: July 30th
    - Counseling: August 1st - 15th
    """)

    if st.button("Ask about Admissions"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "I need detailed information about the admission process"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
