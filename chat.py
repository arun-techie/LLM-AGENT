import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pdf_generator import generate_pdf
from auth import check_auth  # Import authentication check

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Check user authentication
check_auth()

# Function to get AI response
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(question)
    return response.text

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.set_page_config(page_title="MAGS ANS AI Chatbot", page_icon="🤖", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>🤖 MAGS ANS AI Chatbot</h1>",
    unsafe_allow_html=True
)

st.write("💬 **Ask me anything, and I'll do my best to assist you!**")
input_text = st.text_input("✏️ Type your question here...", placeholder="Example: What is AI?")
submit = st.button("🚀 Ask Me")

if submit:
    if input_text.strip():
        response = get_gemini_response(input_text)

        # Store in chat history
        st.session_state.chat_history.append(("User", input_text))
        st.session_state.chat_history.append(("Bot", response))

        # Display chat history with styling
        st.markdown("### 📜 Chat History:")
        for role, text in st.session_state.chat_history:
            if role == "User":
                st.markdown(f"<p style='color: blue;'><strong>{role}:</strong> {text}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: green;'><strong>{role}:</strong> {text}</p>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a question before submitting.")

# Display PDF download button
if st.session_state.chat_history:
    st.markdown("---")
    pdf_file = generate_pdf()

    st.download_button(
        label="📥 Download Chat History as PDF",
        data=pdf_file,
        file_name="chat_history.pdf",
        mime="application/pdf"
    )

# Logout button
if st.button("🔓 Logout"):
    st.session_state.authenticated = False
    st.session_state.chat_history = []  # Clear chat history on logout
    st.rerun()
