import PyPDF2
import pdfplumber
import docx
import re

def extract_text_from_pdf_method1(file):
    """Extract text using PyPDF2"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"PyPDF2 failed: {str(e)}")
        return None

def extract_text_from_pdf_method2(file):
    """Extract text using pdfplumber (more reliable)"""
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"pdfplumber failed: {str(e)}")
        return None

def extract_text_from_pdf(file):
    """Extract text from PDF using best available method"""
    # Try pdfplumber first (more reliable)
    text = extract_text_from_pdf_method2(file)
    
    # If that fails, try PyPDF2
    if not text or len(text.strip()) < 50:
        file.seek(0)  # Reset file pointer
        text = extract_text_from_pdf_method1(file)
    
    return text if text else "Could not extract text from PDF"

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
    
    print(f"DEBUG: Processing file: {filename}")
    
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif filename.endswith('.txt'):  # ADD THIS
        text = file.read().decode('utf-8')  # ADD THIS
    else:
        return "Unsupported file format"
    
    print(f"DEBUG: Extracted {len(text)} characters")
    if len(text) > 0:
        print(f"DEBUG: Sample text: {text[:300]}")
    
    return text

def extract_email(text):
    """Extract email from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not found"

def extract_phone(text):
    """Extract phone number from text"""
    # Multiple phone patterns
    phone_patterns = [
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        r'\d{10}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',
        r'\(\d{3}\)\s*\d{3}[-.\s]\d{4}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            return phones[0]
    
    return "Not found"

def extract_skills(text):
    """Extract common skills from text"""
    # Expanded skill list
    common_skills = [
        # Programming Languages
        'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift',
        'kotlin', 'scala', 'r', 'matlab', 'perl',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node', 'nodejs', 'express',
        'django', 'flask', 'fastapi', 'spring', 'asp.net',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'data science', 'ai', 'artificial intelligence',
        'tensorflow', 'pytorch', 'scikit-learn', 'sklearn', 'keras', 'pandas', 'numpy',
        'nlp', 'computer vision', 'opencv', 'data analysis', 'data visualization',
        'statistics', 'mathematics', 'neural networks',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle',
        'sqlite', 'dynamodb', 'neo4j',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
        'ci/cd', 'devops', 'terraform', 'ansible', 'git', 'github', 'gitlab',
        
        # Data Tools
        'tableau', 'power bi', 'excel', 'spark', 'hadoop', 'kafka', 'airflow',
        'mlflow', 'dbt', 'snowflake',
        
        # APIs & Architecture
        'rest api', 'graphql', 'microservices', 'api', 'restful',
        
        # Other
        'agile', 'scrum', 'jira', 'linux', 'bash', 'shell scripting',
        'matplotlib', 'seaborn', 'plotly', 'jupyter'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        # Use word boundaries to avoid partial matches
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill.title())
    
    # Remove duplicates and return
    return list(set(found_skills))

def analyze_resume(file):
    """Complete resume analysis"""
    text = parse_resume(file)
    
    if "Error" in text or "Could not extract" in text or text == "Unsupported file format":
        return {"error": text}
    
    if len(text.strip()) < 50:
        return {"error": "Resume text is too short or empty. Please check your file."}
    
    skills = extract_skills(text)
    
    analysis = {
        "text": text,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "word_count": len(text.split())
    }
    
    print(f"DEBUG: Analysis complete - {len(skills)} skills found, {analysis['word_count']} words")
    
    return analysis