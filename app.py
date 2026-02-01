import streamlit as st
from resume_parser import analyze_resume

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

**Current Features:**
- ✅ Resume parsing (PDF/Word)
- ✅ Skills extraction
- 🚧 Job matching (coming soon)
""")

st.sidebar.divider()
st.sidebar.caption("Week 1 Progress: 40%")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 📤 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF or Word file", type=['pdf', 'docx'])
    
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

with col2:
    st.write("### 📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the full job description including requirements, qualifications, and responsibilities..."
    )

st.divider()

if st.button("🚀 Analyze Resume", type="primary"):
    if uploaded_file:
        with st.spinner("Analyzing your resume..."):
            # Parse resume
            result = analyze_resume(uploaded_file)
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.success("✅ Resume analyzed successfully!")
                
                # Display results
                st.write("## 📊 Resume Analysis")
                
                # Metrics row
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric("Word Count", result['word_count'])
                
                with metric_col2:
                    st.metric("Skills Found", len(result['skills']))
                
                with metric_col3:
                    email_status = "✅" if result['email'] != "Not found" else "❌"
                    st.metric("Email Detected", email_status)
                
                st.divider()
                
                # Skills section
                st.write("### 🎯 Detected Skills")
                if result['skills']:
                    # Display skills as tags
                    skills_html = ""
                    for skill in result['skills']:
                        skills_html += f'<span style="background-color: #e3f2fd; padding: 5px 10px; margin: 3px; border-radius: 5px; display: inline-block;">{skill}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("No common skills detected. Make sure your resume includes technical skills.")
                
                st.divider()
                
                # Contact info
                st.write("### 📧 Contact Information")
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    st.write(f"**Email:** {result['email']}")
                
                with info_col2:
                    st.write(f"**Phone:** {result['phone']}")
                
                # Expandable section for full text
                with st.expander("📄 View Full Resume Text"):
                    st.text(result['text'][:2000] + "..." if len(result['text']) > 2000 else result['text'])
                
                # Job matching section (placeholder)
                if job_description:
                    st.divider()
                    st.write("### 🎯 Job Match Analysis")
                    st.info("🚧 Job matching feature coming in Week 2! For now, we're focusing on perfecting the resume parser.")
    else:
        st.warning("⚠️ Please upload a resume first")

# Footer
st.divider()
st.caption("ResuMatch v0.2 - Built with ❤️ using Streamlit | Week 1 Progress")