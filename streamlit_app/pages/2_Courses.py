import streamlit as st

def show():
    st.title("📚 Course Information")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Undergraduate Courses")
        st.markdown(""""
        **Engineering**
        - Computer Science & Engineering
        - Electronics & Communication
        - Mechanical Engineering
        - Civil Engineering
        - Electrical Engineering

        **Sciences**
        - Physics
        - Chemistry
        - Mathematics
        - Biology

        **Commerce & Management**
        - B.Com
        - BBA
        - Economics
        """)

    with col2:
        st.subheader("Postgraduate Courses")
        st.markdown(""""
        **Engineering**
        - M.Tech Computer Science
        - M.Tech Electronics
        - M.Tech Mechanical

        **Sciences**
        - M.Sc Physics
        - M.Sc Chemistry
        - M.Sc Mathematics

        **Management**
        - MBA
        - M.Com
        """)

    if st.button("Ask about Specific Course"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Can you tell me more about specific course details?"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
