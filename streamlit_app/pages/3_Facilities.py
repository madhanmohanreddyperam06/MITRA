import streamlit as st

def show():
    st.title("🏫 Campus Facilities")

    tab1, tab2, tab3, tab4 = st.tabs(["Library", "Hostels", "Sports", "Labs"])

    with tab1:
        st.subheader("📖 Library")
        st.markdown(""""
        - **Collection**: Over 50,000 books and journals
        - **Digital Resources**: Online databases and e-books
        - **Reading Rooms**: Spacious and well-lit study areas
        - **Computer Lab**: High-speed internet access
        - **Timings**: Monday-Saturday, 8 AM to 8 PM
        """)

    with tab2:
        st.subheader("🏠 Hostels")
        st.markdown(""""
        - **Boys Hostel**: 500 rooms with modern amenities
        - **Girls Hostel**: 300 rooms with 24/7 security
        - **Facilities**: Wi-Fi, mess, laundry, recreation room
        - **Room Types**: Single, double, and triple occupancy
        """)

    with tab3:
        st.subheader("⚽ Sports")
        st.markdown(""""
        - **Outdoor**: Cricket, football, basketball courts
        - **Indoor**: Badminton, table tennis, gymnasium
        - **Swimming Pool**: Olympic size with coaching
        - **Athletics Track**: 400m synthetic track
        """)

    with tab4:
        st.subheader("🔬 Laboratories")
        st.markdown(""""
        - **Computer Labs**: Latest hardware and software
        - **Science Labs**: Well-equipped physics, chemistry, biology
        - **Engineering Labs**: Specialized equipment for all branches
        - **Research Centers**: Advanced research facilities
        """)

    if st.button("Ask about Facilities"):
        st.session_state.messages.append({
            "role": "user", 
            "content": "Tell me more about campus facilities"
        })
        st.switch_page("main.py")

if __name__ == "__main__":
    show()
