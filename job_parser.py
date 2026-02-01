import re

def parse_job_description(job_text):
    """Parse job description and extract key information"""
    
    if not job_text or len(job_text.strip()) < 50:
        return {"error": "Job description is too short or empty"}
    
    # Extract skills (same logic as resume)
    skills = extract_skills_from_job(job_text)
    
    # Extract requirements
    requirements = extract_requirements(job_text)
    
    # Extract experience level
    experience = extract_experience_level(job_text)
    
    # Extract education
    education = extract_education(job_text)
    
    return {
        "text": job_text,
        "skills_required": skills,
        "requirements": requirements,
        "experience_level": experience,
        "education_required": education,
        "word_count": len(job_text.split())
    }

def extract_skills_from_job(text):
    """Extract required skills from job description"""
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'r',
        'react', 'angular', 'vue', 'node', 'nodejs', 'django', 'flask', 'fastapi',
        'machine learning', 'deep learning', 'data science', 'ai', 'artificial intelligence',
        'tensorflow', 'pytorch', 'scikit-learn', 'sklearn', 'pandas', 'numpy',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github',
        'tableau', 'power bi', 'excel', 'statistics', 'mathematics',
        'nlp', 'computer vision', 'data analysis', 'data visualization',
        'rest api', 'graphql', 'mongodb', 'postgresql', 'mysql',
        'agile', 'scrum', 'jira', 'ci/cd', 'devops',
        'hadoop', 'spark', 'kafka', 'airflow', 'mlflow',
        'opencv', 'matplotlib', 'seaborn', 'plotly',
        'linux', 'bash', 'shell scripting'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            # Capitalize properly
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def extract_requirements(text):
    """Extract key requirements from job description"""
    requirements = []
    
    # Common requirement patterns
    requirement_patterns = [
        r'(?:required|must have|mandatory)[\s:]+([^\n\.]+)',
        r'(?:responsibilities|duties)[\s:]+([^\n]+)',
        r'(?:qualifications)[\s:]+([^\n]+)'
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        requirements.extend(matches[:3])  # Take first 3 matches
    
    return requirements[:5] if requirements else ["Could not extract specific requirements"]

def extract_experience_level(text):
    """Extract required experience level"""
    text_lower = text.lower()
    
    # Check for experience patterns
    if re.search(r'(\d+)\+?\s*(?:years?|yrs?).*experience', text_lower):
        match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', text_lower)
        return f"{match.group(1)}+ years"
    elif 'fresher' in text_lower or 'entry level' in text_lower:
        return "Fresher/Entry Level"
    elif 'senior' in text_lower:
        return "Senior Level"
    elif 'mid' in text_lower or 'intermediate' in text_lower:
        return "Mid Level"
    else:
        return "Not specified"

def extract_education(text):
    """Extract education requirements"""
    text_lower = text.lower()
    
    education_keywords = {
        "PhD": ["phd", "ph.d", "doctorate"],
        "Master's": ["master", "m.s", "m.tech", "mca", "mba"],
        "Bachelor's": ["bachelor", "b.tech", "b.e", "bca", "b.sc"]
    }
    
    for degree, keywords in education_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return degree
    
    return "Not specified"