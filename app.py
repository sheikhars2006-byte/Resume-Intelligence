import streamlit as st

# Page config
st.set_page_config(
    page_title="ResuMatch",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 ResuMatch")
st.subheader("AI-Powered Resume Optimization Platform")

# Sidebar
st.sidebar.header("About")
st.sidebar.info("""
ResuMatch helps you optimize your resume for job applications.
Upload your resume and paste a job description to get started.
""")

# Main content
st.write("### Upload Your Resume")
uploaded_file = st.file_uploader("Choose a PDF or Word file", type=['pdf', 'docx'])

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    
st.write("### Job Description")
job_description = st.text_area("Paste the job description here", height=200)

if st.button("Analyze Match"):
    if uploaded_file and job_description:
        st.info("🚀 Analysis feature coming soon!")
    else:
        st.warning("⚠️ Please upload a resume and enter a job description")

# Footer
st.divider()
st.caption("ResuMatch v0.1 - Built with ❤️ using Streamlit")