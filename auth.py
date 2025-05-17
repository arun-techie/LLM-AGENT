import streamlit as st

# Dummy user credentials
USER_CREDENTIALS = {
    "aadvik": "password123",
    "user2": "pass456",
    "122012169357@pmu.edu": "122012169357"
}

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    """Styled Login Page for User Authentication"""
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🔒 Login to MAGS ANS AI Chatbot</h1>", unsafe_allow_html=True)

    # Create login inputs without modifying session state immediately
    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔑 Password", type="password", key="login_password")
    
    if st.button("🚀 Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            # Modify session state *after* user submits credentials
            st.session_state.authenticated = True
            st.session_state["username"] = username  # Use dictionary syntax to avoid errors
            st.success(f"🎉 Welcome, {username}!")
            st.rerun()  # Refresh the app to update UI
        else:
            st.error("❌ Invalid username or password. Please try again.")

def check_auth():
    """Ensure user authentication before accessing the chatbot"""
    if not st.session_state.get("authenticated", False):  # Check session state safely
        login()
        st.stop()
