import streamlit as st
import pdfplumber
from fpdf import FPDF

st.set_page_config(page_title="Resume Builder", page_icon="📄")

st.title("📄 Resume Generator from LinkedIn Export")

st.write("Upload your exported LinkedIn PDF or paste the content manually.")

input_type = st.radio("Choose input method:", ["Upload LinkedIn PDF", "Paste Text"])

text_data = ""

if input_type == "Upload LinkedIn PDF":
    uploaded_file = st.file_uploader("Upload LinkedIn PDF file", type=["pdf"])
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text_data += page.extract_text() or ""
elif input_type == "Paste Text":
    text_data = st.text_area("Paste your LinkedIn content here")

if text_data:
    st.subheader("📝 Preview of Your Resume")

    lines = text_data.strip().split("\n")
    name = lines[0] if lines else "Your Name"
    title = lines[1] if len(lines) > 1 else "Your Title"

    st.markdown(f"### {name}")
    st.markdown(f"#### {title}")
    st.write("**Summary:**")
    st.write("\n".join(lines[2:8]))

    st.write("**Experience:**")
    for line in lines[8:]:
        if any(x in line.lower() for x in ["company", "-", "•", "engineer", "developer"]):
            st.markdown(f"- {line}")

    if st.button("📥 Download Resume as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output("resume.pdf")
        with open("resume.pdf", "rb") as file:
            st.download_button("Download PDF", file, file_name="resume.pdf")
