import streamlit as st
from resume_parser import analyze_resume
from job_parser import parse_job_description
from matcher import analyze_match
from ats_analyzer import analyze_ats
from skills_gap_analyzer import analyze_skills_gap

# Page config
st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - FIXED TAB VISIBILITY
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding: 1rem 0;
    }
    
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .score-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .ats-score-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(252, 182, 159, 0.3);
        margin: 1.5rem 0;
    }
    
    .learning-card {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(150, 230, 161, 0.3);
    }
    
    .skill-impact-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .skill-impact-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .impact-high {
        border-left-color: #ff6b6b;
    }
    
    .impact-medium {
        border-left-color: #ffa502;
    }
    
    .impact-low {
        border-left-color: #4caf50;
    }
    
    .score-emoji {
        font-size: 4rem;
    }
    
    .score-number {
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .ats-score-number {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .score-label {
        font-size: 1.5rem;
        color: #555;
        font-weight: 500;
    }
    
    .ats-improvement {
        display: inline-block;
        background: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .suggestion-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .priority-high {
        border-left-color: #ff6b6b;
    }
    
    .priority-critical {
        border-left-color: #ee5a24;
    }
    
    .priority-medium {
        border-left-color: #ffa502;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #667eea;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 500;
    }
    
    [data-testid="stFileUploader"] {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 1.5rem;
        background: rgba(102, 126, 234, 0.02);
    }
    
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* FIXED TABS STYLING - NOW VISIBLE! */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        color: #333333 !important;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        border: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e8ebf0;
        color: #667eea !important;
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🧠 Resume Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-Powered Resume Optimization with Career Guidance</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📊 Dashboard")
    st.markdown("---")
    
    st.subheader("🎯 Features")
    st.write("✅ Resume Parsing")
    st.write("✅ Job Analysis")
    st.write("✅ AI Matching")
    st.write("✅ Skills Comparison")
    st.write("✅ ATS Killer Mode ⭐")
    st.write("✅ Learning Path Guide ⭐")
    st.write("🔜 Market Insights")
    
    st.markdown("---")
    
    st.subheader("📈 Progress")
    progress = 0.60
    st.progress(progress)
    st.caption(f"{int(progress*100)}% Complete")
    
    st.markdown("---")
    
    st.subheader("💡 What's New?")
    st.caption("🎓 Skills Gap Analyzer now available! Get personalized learning recommendations.")
    
    st.markdown("---")
    
    st.subheader("👥 Team")
    st.caption("Main Developer")
    st.caption("Team Member")
    
    st.markdown("---")
    
    st.caption("Built with ❤️ for CSE Project")
    st.caption("Resume Intelligence v2.1")

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, Word, Text"
    )
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

with col2:
    st.markdown("### 📋 Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="Copy and paste the complete job description...",
        help="Include the full job posting for best results"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Analyze button
analyze_btn = st.button("🚀 Complete Analysis (Match + ATS + Learning Path)", use_container_width=True)

if analyze_btn:
    if uploaded_file and job_description:
        with st.spinner("🔍 Running complete analysis..."):
            resume_result = analyze_resume(uploaded_file)
            job_result = parse_job_description(job_description)
            
            if "error" in resume_result:
                st.error(f"❌ Resume Error: {resume_result['error']}")
            elif "error" in job_result:
                st.error(f"❌ Job Error: {job_result['error']}")
            else:
                match_result = analyze_match(resume_result, job_result)
                ats_result = analyze_ats(resume_result['text'], job_result['skills_required'])
                skills_gap_result = analyze_skills_gap(
                    resume_result['skills'],
                    job_result['skills_required'],
                    match_result['final_score']
                )
                
                st.success("✅ Complete Analysis Done!")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Create tabs
                tab1, tab2, tab3 = st.tabs([
                    "🎯 Job Match Analysis",
                    "🤖 ATS Killer Mode",
                    "🎓 Learning Path"
                ])
                
                with tab1:
                    st.markdown("## 🎯 Job Match Results")
                    
                    score_html = f"""
                    <div class="score-card">
                        <div class="score-emoji">{match_result['match_color']}</div>
                        <div class="score-number">{match_result['final_score']}%</div>
                        <div class="score-label">{match_result['match_category']}</div>
                    </div>
                    """
                    st.markdown(score_html, unsafe_allow_html=True)
                    
                    st.markdown("### 📊 Breakdown")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    
                    with metric_col1:
                        st.metric("Overall Match", f"{match_result['overall_match']}%")
                    with metric_col2:
                        st.metric("Skills Match", f"{match_result['skill_match']}%")
                    with metric_col3:
                        st.metric("Skills Found", f"{match_result['skills_matched']}/{match_result['total_skills_required']}")
                    
                    st.divider()
                    
                    st.markdown("### 🎯 Skills Analysis")
                    skill_col1, skill_col2 = st.columns(2)
                    
                    with skill_col1:
                        st.markdown("#### ✅ Matching Skills")
                        if match_result['matching_skills']:
                            for skill in match_result['matching_skills']:
                                st.markdown(f"✅ **{skill}**")
                        else:
                            st.warning("No matching skills found")
                    
                    with skill_col2:
                        st.markdown("#### ❌ Missing Skills")
                        if match_result['missing_skills']:
                            for skill in match_result['missing_skills']:
                                st.markdown(f"❌ {skill}")
                        else:
                            st.success("You have all required skills!")
                    
                    st.divider()
                    st.markdown("### 💡 Recommendations")
                    
                    if match_result['final_score'] >= 75:
                        st.success(f"""**🎉 Excellent Match!** 
                        
Your resume aligns very well with this position. 
✅ Apply confidently - You meet the requirements  
✅ Highlight matching skills in your cover letter  
✅ Prepare project examples using these technologies  

**Match Score: {match_result['final_score']}% - Strong candidate!**""")
                    elif match_result['final_score'] >= 60:
                        st.info(f"""**👍 Good Match!**
                        
You meet most requirements. Consider:
📝 Add projects demonstrating missing skills  
📝 Emphasize transferable experience  
📝 Show willingness to learn  

**Match Score: {match_result['final_score']}% - Solid chance!**""")
                    elif match_result['final_score'] >= 40:
                        st.warning(f"""**⚠️ Fair Match**
                        
Some gaps exist. To improve:
📚 Learn missing critical skills first  
📚 Add relevant projects  
📚 Consider similar roles  

**Match Score: {match_result['final_score']}% - Improvement needed**""")
                    else:
                        st.error(f"""**❌ Significant Gaps**
                        
This role may not be suitable now:
🎯 Build missing foundational skills  
🎯 Look for entry-level matching roles  
🎯 Create learning plan  

**Match Score: {match_result['final_score']}% - Consider other opportunities**""")
                
                with tab2:
                    st.markdown("## 🤖 ATS Killer Mode")
                    st.info("💡 ATS (Applicant Tracking Systems) scan resumes before humans see them. This analyzes if your resume will pass.")
                    
                    col_ats1, col_ats2 = st.columns([3, 2])
                    
                    with col_ats1:
                        ats_score_html = f"""
                        <div class="ats-score-card">
                            <div style="font-size: 1.2rem; color: #555; margin-bottom: 0.5rem;">Current ATS Score</div>
                            <div class="ats-score-number">{ats_result['ats_score']}%</div>
                            <div style="font-size: 1rem; color: #666;">{ats_result['category']}</div>
                            <div class="ats-improvement">
                                ↗️ Potential: {ats_result['potential_score']}% (+{ats_result['improvement']} points)
                            </div>
                        </div>
                        """
                        st.markdown(ats_score_html, unsafe_allow_html=True)
                    
                    with col_ats2:
                        st.markdown("### 📊 Score Breakdown")
                        st.metric("Formatting", f"{ats_result['formatting_score']}%")
                        st.metric("Action Verbs", f"{ats_result['verb_score']}%")
                        st.metric("Keywords", f"{ats_result['keyword_score']}%")
                        st.metric("Length", f"{ats_result['length_score']}%")
                    
                    st.divider()
                    st.markdown("### ⚠️ Issues Detected")
                    
                    issues_found = False
                    
                    if ats_result['issues']['formatting']:
                        issues_found = True
                        with st.expander("🔧 Formatting Issues", expanded=True):
                            for issue in ats_result['issues']['formatting']:
                                st.warning(f"⚠️ {issue}")
                    
                    if ats_result['issues']['verbs']:
                        issues_found = True
                        with st.expander("💪 Action Verb Issues", expanded=True):
                            for issue in ats_result['issues']['verbs']:
                                st.warning(f"⚠️ {issue}")
                    
                    if ats_result['issues']['keywords']:
                        issues_found = True
                        with st.expander("🔑 Keyword Issues", expanded=True):
                            for issue in ats_result['issues']['keywords']:
                                st.warning(f"⚠️ {issue}")
                    
                    if ats_result['issues']['length']:
                        issues_found = True
                        with st.expander("📏 Length Issues", expanded=False):
                            for issue in ats_result['issues']['length']:
                                st.warning(f"⚠️ {issue}")
                    
                    if not issues_found:
                        st.success("✅ No major issues detected! Your resume is ATS-friendly.")
                    
                    st.divider()
                    st.markdown("### 💡 Actionable Suggestions")
                    
                    if ats_result['suggestions']:
                        for i, suggestion in enumerate(ats_result['suggestions'], 1):
                            priority_class = f"priority-{suggestion['priority'].lower()}"
                            suggestion_html = f"""
                            <div class="suggestion-card {priority_class}">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                    <strong style="font-size: 1.1rem;">{i}. {suggestion['action']}</strong>
                                    <span style="background: #e3f2fd; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.85rem;">
                                        {suggestion['impact']}
                                    </span>
                                </div>
                                <div style="color: #666; margin-bottom: 0.3rem;">
                                    <strong>Category:</strong> {suggestion['category']} | 
                                    <strong>Priority:</strong> {suggestion['priority']}
                                </div>
                                <div style="color: #555; font-size: 0.95rem;">
                                    💡 {suggestion['details']}
                                </div>
                            </div>
                            """
                            st.markdown(suggestion_html, unsafe_allow_html=True)
                
                with tab3:
                    st.markdown("## 🎓 Personalized Learning Path")
                    
                    if skills_gap_result['missing_skills_count'] == 0:
                        st.success("🎉 **Perfect! You have all required skills!**")
                        st.info("Focus on building projects and gaining experience to demonstrate your expertise.")
                    else:
                        learning_card_html = f"""
                        <div class="learning-card">
                            <h3 style="margin: 0; color: #2d3436;">📚 Skills to Learn: {skills_gap_result['missing_skills_count']}</h3>
                            <p style="font-size: 1.1rem; color: #636e72; margin: 0.5rem 0 0 0;">
                                Estimated Time: {skills_gap_result['total_time_estimate']}
                            </p>
                        </div>
                        """
                        st.markdown(learning_card_html, unsafe_allow_html=True)
                        
                        st.divider()
                        st.markdown("### 🎯 Prioritized Skills (By Impact)")
                        
                        for i, skill_data in enumerate(skills_gap_result['prioritized_skills'][:5], 1):
                            impact_class = "impact-high" if skill_data['impact_score'] >= 12 else \
                                          "impact-medium" if skill_data['impact_score'] >= 8 else "impact-low"
                            
                            skill_html = f"""
                            <div class="skill-impact-card {impact_class}">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                                    <h4 style="margin: 0; color: #2d3436;">{i}. {skill_data['skill']}</h4>
                                    <span style="background: #667eea; color: white; padding: 0.4rem 0.9rem; border-radius: 15px; font-weight: 600;">
                                        +{skill_data['impact_score']} points
                                    </span>
                                </div>
                                
                                <div style="display: flex; gap: 1rem; margin-bottom: 0.8rem; flex-wrap: wrap;">
                                    <span style="background: #f1f3f5; padding: 0.3rem 0.7rem; border-radius: 8px; font-size: 0.9rem;">
                                        ⏱️ {skill_data['time_to_learn']}
                                    </span>
                                    <span style="background: #f1f3f5; padding: 0.3rem 0.7rem; border-radius: 8px; font-size: 0.9rem;">
                                        📊 {skill_data['difficulty']}
                                    </span>
                                    <span style="background: #f1f3f5; padding: 0.3rem 0.7rem; border-radius: 8px; font-size: 0.9rem;">
                                        🔥 {skill_data['priority']} Priority
                                    </span>
                                </div>
                                
                                <div style="background: #e3f2fd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem;">
                                    <strong style="color: #1976d2;">💰 Career Impact:</strong>
                                    <p style="margin: 0.3rem 0 0 0; color: #424242;">{skill_data['salary_impact']}</p>
                                </div>
                                
                                <div>
                                    <strong style="color: #2d3436;">📚 Learning Resources:</strong>
                                    <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
                                        {"".join([f"<li style='margin: 0.3rem 0;'>{resource}</li>" for resource in skill_data['resources']])}
                                    </ul>
                                </div>
                            </div>
                            """
                            st.markdown(skill_html, unsafe_allow_html=True)
                        
                        if len(skills_gap_result['prioritized_skills']) > 5:
                            with st.expander(f"📋 View All {len(skills_gap_result['prioritized_skills'])} Skills"):
                                for skill_data in skills_gap_result['prioritized_skills'][5:]:
                                    st.write(f"**{skill_data['skill']}** - {skill_data['time_to_learn']} - Impact: +{skill_data['impact_score']} points")
                        
                        st.divider()
                        st.markdown("### 📅 Suggested Learning Plan")
                        
                        plan_col1, plan_col2, plan_col3 = st.columns(3)
                        
                        with plan_col1:
                            st.markdown("#### 🥇 Phase 1: Foundation")
                            st.caption("Start here (Critical skills)")
                            if skills_gap_result['learning_plan']['phase_1']:
                                for skill in skills_gap_result['learning_plan']['phase_1']:
                                    st.write(f"• {skill['skill']}")
                            else:
                                st.write("All foundation skills covered!")
                        
                        with plan_col2:
                            st.markdown("#### 🥈 Phase 2: Enhancement")
                            st.caption("Build on foundation")
                            if skills_gap_result['learning_plan']['phase_2']:
                                for skill in skills_gap_result['learning_plan']['phase_2']:
                                    st.write(f"• {skill['skill']}")
                            else:
                                st.write("No enhancement skills needed")
                        
                        with plan_col3:
                            st.markdown("#### 🥉 Phase 3: Advanced")
                            st.caption("Nice to have")
                            if skills_gap_result['learning_plan']['phase_3']:
                                for skill in skills_gap_result['learning_plan']['phase_3']:
                                    st.write(f"• {skill['skill']}")
                            else:
                                st.write("No advanced skills needed")
                        
                        st.divider()
                        st.markdown("### 💡 Personalized Recommendations")
                        
                        for rec in skills_gap_result['recommendations']:
                            st.info(rec)
                
                st.divider()
                
                with st.expander("📄 Resume Details"):
                    detail_col1, detail_col2 = st.columns(2)
                    with detail_col1:
                        st.write(f"**📊 Word Count:** {resume_result['word_count']}")
                        st.write(f"**📧 Email:** {resume_result['email']}")
                    with detail_col2:
                        st.write(f"**📱 Phone:** {resume_result['phone']}")
                        st.write(f"**🎯 Skills Found:** {len(resume_result['skills'])}")
                
                with st.expander("💼 Job Details"):
                    job_col1, job_col2 = st.columns(2)
                    with job_col1:
                        st.write(f"**📊 Word Count:** {job_result['word_count']}")
                        st.write(f"**⏱️ Experience:** {job_result['experience_level']}")
                    with job_col2:
                        st.write(f"**🎓 Education:** {job_result['education_required']}")
                        st.write(f"**🎯 Skills Required:** {len(job_result['skills_required'])}")
                
    elif not uploaded_file:
        st.warning("⚠️ Please upload your resume")
    else:
        st.warning("⚠️ Please paste the job description")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<p style='text-align: center; color: #888; font-size: 0.9rem;'>
    Resume Intelligence - AI-Powered Resume Optimization with Career Guidance<br>
    Built with Streamlit • Python • Machine Learning • NLP<br>
    CSE Data Science Project 2026
</p>
""", unsafe_allow_html=True)