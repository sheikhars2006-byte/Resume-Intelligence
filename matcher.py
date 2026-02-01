from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_tfidf_match(resume_text, job_text):
    """Calculate match score using TF-IDF and cosine similarity"""
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        max_features=1000
    )
    
    # Fit and transform both texts
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to percentage
        match_score = round(similarity * 100, 2)
        
        return match_score
    except Exception as e:
        return 0.0

def calculate_skill_match(resume_skills, job_skills):
    """Calculate skill match percentage"""
    
    if not job_skills:
        return 0, [], []
    
    # Convert to lowercase for comparison
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_skills_lower = [s.lower() for s in job_skills]
    
    # Find matching and missing skills
    matching_skills = []
    missing_skills = []
    
    for job_skill in job_skills_lower:
        if job_skill in resume_skills_lower:
            matching_skills.append(job_skill.title())
        else:
            missing_skills.append(job_skill.title())
    
    # Calculate percentage
    if len(job_skills) > 0:
        skill_match_percentage = round((len(matching_skills) / len(job_skills)) * 100, 2)
    else:
        skill_match_percentage = 0
    
    return skill_match_percentage, matching_skills, missing_skills

def analyze_match(resume_data, job_data):
    """Complete match analysis between resume and job"""
    
    # Calculate TF-IDF based overall match
    overall_match = calculate_tfidf_match(
        resume_data['text'],
        job_data['text']
    )
    
    # Calculate skill match
    skill_match, matching_skills, missing_skills = calculate_skill_match(
        resume_data['skills'],
        job_data['skills_required']
    )
    
    # Calculate final score (weighted average)
    # 60% weight to overall match, 40% weight to skill match
    final_score = round((overall_match * 0.6) + (skill_match * 0.4), 2)
    
    # Determine match category
    if final_score >= 75:
        match_category = "Excellent Match"
        match_color = "🟢"
    elif final_score >= 60:
        match_category = "Good Match"
        match_color = "🟡"
    elif final_score >= 40:
        match_category = "Fair Match"
        match_color = "🟠"
    else:
        match_category = "Poor Match"
        match_color = "🔴"
    
    return {
        "final_score": final_score,
        "overall_match": overall_match,
        "skill_match": skill_match,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_category": match_category,
        "match_color": match_color,
        "total_skills_required": len(job_data['skills_required']),
        "skills_matched": len(matching_skills)
    }