from fpdf import FPDF
import streamlit as st
from io import BytesIO

# Function to generate PDF from chat history
def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Use built-in font instead of Arial Unicode
    pdf.set_font("Times", style="B", size=14)
    pdf.cell(200, 10, "MAGS ANS's AI Chatbot - Chat History", ln=True, align="L")
    pdf.ln(5)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Add a line separator
    pdf.ln(5)

    # Process chat history
    pdf.set_font("Times", size=12)
    for index, (role, text) in enumerate(st.session_state.chat_history, start=1):
        if role == "User":
            pdf.set_font("Times", style="B", size=12)
            pdf.multi_cell(0, 8, f"Q{index}: {text}", align="J")
            pdf.set_font("Times", size=12)
        else:
            pdf.set_font("Times", style="B", size=12)
            pdf.multi_cell(0, 8, f"A{index}:", align="J")
            pdf.set_font("Times", size=12)
            pdf.multi_cell(0, 8, text, align="J")

        pdf.ln(5)

    # Save PDF to BytesIO
    pdf_buffer = BytesIO()
    pdf_output = pdf.output(dest="S").encode("latin-1")  # Ensures correct encoding
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)

    return pdf_buffer

# Download Button (To be used in `chat.py`)
if "chat_history" in st.session_state and st.session_state.chat_history:
    if st.button("📥 Download Chat History as PDF"):
        pdf_file = generate_pdf()
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="chat_history.pdf",
            mime="application/pdf",
        )
