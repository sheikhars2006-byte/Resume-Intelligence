import PyPDF2
import docx
import re

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file):
    """Extract text from Word document"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def parse_resume(file):
    """Main function to parse resume based on file type"""
    filename = file.name.lower()
    
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    else:
        return "Unsupported file format"
    
    return text

def extract_email(text):
    """Extract email from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not found"

def extract_phone(text):
    """Extract phone number from text"""
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else "Not found"

def extract_skills(text):
    """Extract common skills from text"""
    # Common tech skills (we'll expand this later)
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
        'react', 'angular', 'vue', 'node', 'django', 'flask', 'fastapi',
        'machine learning', 'deep learning', 'data science', 'ai',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git',
        'tableau', 'power bi', 'excel', 'statistics'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def analyze_resume(file):
    """Complete resume analysis"""
    text = parse_resume(file)
    
    if "Error" in text or text == "Unsupported file format":
        return {"error": text}
    
    analysis = {
        "text": text,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "word_count": len(text.split())
    }
    
    return analysis