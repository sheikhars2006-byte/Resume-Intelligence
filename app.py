import streamlit as st
from resume_parser import analyze_resume
from job_parser import parse_job_description
from matcher import analyze_match
# from styles import get_custom_css

# Page config
st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="🧠",
    layout="wide"
)
# Apply custom CSS
# st.markdown(get_custom_css(), unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🧠 Resume Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Resume Optimization Platform</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Project Info")
st.sidebar.info("""
**Resume Intelligence** analyzes your resume against job descriptions using AI and provides actionable insights.

**Current Features:**
- ✅ Resume parsing (PDF/Word)
- ✅ Job description analysis
- ✅ Skills extraction
- ✅ TF-IDF based matching
- ✅ Match score calculation
""")

st.sidebar.divider()
st.sidebar.caption("**Week 1 Progress:** 75%")
st.sidebar.progress(0.75)

st.sidebar.divider()
st.sidebar.caption("**Team:**")
st.sidebar.write("• Main Developer: [Your Name]")
st.sidebar.write("• Team Member: [Teammate Name]")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
    "Choose a PDF, Word, or TXT file",
    type=['pdf', 'docx', 'txt'],  # Added 'txt'
    help="Upload your resume in PDF, Word, or plain text format"
    )
    
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

with col2:
    st.write("### 📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the full job description including requirements, qualifications, and responsibilities...",
        help="Copy and paste the complete job posting"
    )

st.divider()

# Analyze button
if st.button("🚀 Analyze Match", type="primary", use_container_width=True):
    if uploaded_file and job_description:
        with st.spinner("🔍 Analyzing your resume and job match..."):
            
            # Parse resume
            resume_result = analyze_resume(uploaded_file)
            
            # Parse job description
            job_result = parse_job_description(job_description)
            
            # Check for errors
            if "error" in resume_result:
                st.error(f"❌ Resume Error: {resume_result['error']}")
            elif "error" in job_result:
                st.error(f"❌ Job Description Error: {job_result['error']}")
            else:
                # Calculate match
                match_result = analyze_match(resume_result, job_result)
                
                st.success("✅ Analysis completed successfully!")
                
                # Display match score prominently
                st.write("## 🎯 Match Analysis")
                
                score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
                
                with score_col2:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;">
                        <h1 style="font-size: 4rem; margin: 0;">{match_result['match_color']}</h1>
                        <h2 style="color: #1f77b4; margin: 0.5rem 0;">{match_result['final_score']}%</h2>
                        <p style="color: #666; font-size: 1.2rem; margin: 0;">{match_result['match_category']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                # Detailed scores
                st.write("### 📊 Detailed Scores")
                
                detail_col1, detail_col2, detail_col3 = st.columns(3)
                
                with detail_col1:
                    st.metric("Overall Content Match", f"{match_result['overall_match']}%")
                
                with detail_col2:
                    st.metric("Skills Match", f"{match_result['skill_match']}%")
                
                with detail_col3:
                    st.metric(
                        "Skills Matched",
                        f"{match_result['skills_matched']}/{match_result['total_skills_required']}"
                    )
                
                st.divider()
                
                # Skills comparison
                st.write("### 🎯 Skills Analysis")
                
                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.write("**✅ Matching Skills**")
                    if match_result['matching_skills']:
                        for skill in match_result['matching_skills']:
                            st.markdown(f"- ✅ {skill}")
                    else:
                        st.warning("No matching skills found")
                
                with skill_col2:
                    st.write("**❌ Missing Skills**")
                    if match_result['missing_skills']:
                        for skill in match_result['missing_skills']:
                            st.markdown(f"- ❌ {skill}")
                    else:
                        st.success("You have all required skills!")
                
                st.divider()
                
                # Recommendations
                st.write("### 💡 Recommendations")
                
                if match_result['final_score'] >= 75:
                    st.success("""
                    **Excellent match! Your resume aligns very well with this job.**
                    - ✅ Apply with confidence
                    - ✅ Highlight matching skills in your cover letter
                    - ✅ Prepare to discuss projects using these technologies
                    """)
                elif match_result['final_score'] >= 60:
                    st.info("""
                    **Good match! You meet most requirements.**
                    - 📝 Consider adding projects demonstrating missing skills
                    - 📝 Emphasize transferable experience
                    - 📝 Mention willingness to learn missing technologies
                    """)
                elif match_result['final_score'] >= 40:
                    st.warning("""
                    **Fair match. Some gaps exist.**
                    - 📚 Learn the missing critical skills before applying
                    - 📚 Add relevant projects to your resume
                    - 📚 Consider similar roles that match better
                    """)
                else:
                    st.error("""
                    **Poor match. Significant gaps exist.**
                    - 🎯 This role may not be suitable at this time
                    - 🎯 Focus on building missing skills first
                    - 🎯 Look for roles matching your current skill set
                    """)
                
                st.divider()
                
                # Expandable sections
                with st.expander("📄 Resume Details"):
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.write(f"**Word Count:** {resume_result['word_count']}")
                        st.write(f"**Email:** {resume_result['email']}")
                    with res_col2:
                        st.write(f"**Phone:** {resume_result['phone']}")
                        st.write(f"**Skills Found:** {len(resume_result['skills'])}")
                
                with st.expander("💼 Job Details"):
                    job_col1, job_col2 = st.columns(2)
                    with job_col1:
                        st.write(f"**Word Count:** {job_result['word_count']}")
                        st.write(f"**Experience Required:** {job_result['experience_level']}")
                    with job_col2:
                        st.write(f"**Education Required:** {job_result['education_required']}")
                        st.write(f"**Skills Required:** {len(job_result['skills_required'])}")
                
    elif not uploaded_file:
        st.warning("⚠️ Please upload your resume")
    elif not job_description:
        st.warning("⚠️ Please paste a job description")
    else:
        st.warning("⚠️ Please upload a resume and paste a job description")

# Footer
st.divider()
st.caption("Resume Intelligence v0.3 - Built with ❤️ for CSE Data Science Project | Week 1")