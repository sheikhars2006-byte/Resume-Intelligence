import re
from collections import Counter

class ATSAnalyzer:
    """Analyze resume for ATS (Applicant Tracking System) compatibility"""
    
    def __init__(self):
        # Weak action verbs that hurt ATS scores
        self.weak_verbs = [
            'responsible for', 'duties included', 'worked on', 'helped with',
            'assisted in', 'was involved', 'participated in', 'tasked with',
            'handled', 'dealt with', 'familiar with', 'knowledge of'
        ]
        
        # Strong action verbs that improve ATS scores
        self.strong_verbs = [
            'achieved', 'developed', 'created', 'designed', 'implemented',
            'built', 'launched', 'improved', 'increased', 'decreased',
            'reduced', 'optimized', 'managed', 'led', 'directed',
            'established', 'generated', 'delivered', 'executed', 'spearheaded',
            'pioneered', 'transformed', 'accelerated', 'streamlined', 'engineered'
        ]
        
        # ATS-unfriendly formatting elements
        self.formatting_issues = {
            'tables': r'┌|├|│|┐|┤|└|┘|─|╭|╮|╯|╰',  # Table characters
            'special_chars': r'[★☆♦●○◆◇■□▪▫]',  # Special bullets
            'headers_footers': r'Page \d+ of \d+|^\d+$',  # Page numbers
        }
    
    def analyze(self, resume_text, job_skills):
        """Main ATS analysis function"""
        
        # Individual checks
        formatting_score, formatting_issues = self._check_formatting(resume_text)
        verb_score, verb_issues = self._check_action_verbs(resume_text)
        keyword_score, keyword_issues = self._check_keywords(resume_text, job_skills)
        length_score, length_issues = self._check_length(resume_text)
        
        # Calculate overall ATS score (weighted average)
        ats_score = round(
            (formatting_score * 0.25) +
            (verb_score * 0.25) +
            (keyword_score * 0.35) +
            (length_score * 0.15)
        )
        
        # Compile all issues
        all_issues = {
            'formatting': formatting_issues,
            'verbs': verb_issues,
            'keywords': keyword_issues,
            'length': length_issues
        }
        
        # Generate suggestions
        suggestions = self._generate_suggestions(all_issues, resume_text, job_skills)
        
        # Calculate potential improvement
        potential_score = self._calculate_potential_score(ats_score, all_issues)
        
        return {
            'ats_score': ats_score,
            'potential_score': potential_score,
            'improvement': potential_score - ats_score,
            'formatting_score': formatting_score,
            'verb_score': verb_score,
            'keyword_score': keyword_score,
            'length_score': length_score,
            'issues': all_issues,
            'suggestions': suggestions,
            'category': self._get_category(ats_score)
        }
    
    def _check_formatting(self, text):
        """Check for ATS-unfriendly formatting"""
        issues = []
        score = 100
        
        # Check for table characters
        if re.search(self.formatting_issues['tables'], text):
            issues.append("Uses tables or unusual formatting (ATS may not parse correctly)")
            score -= 15
        
        # Check for special characters
        special_chars = re.findall(self.formatting_issues['special_chars'], text)
        if special_chars:
            issues.append(f"Contains {len(special_chars)} special bullet characters (use standard bullets)")
            score -= 10
        
        # Check for multiple columns indicators
        if text.count('\t') > 10 or '  ' * 5 in text:
            issues.append("May contain multiple columns (ATS prefers single column)")
            score -= 15
        
        # Check for headers/footers
        if re.search(self.formatting_issues['headers_footers'], text):
            issues.append("Contains page numbers or headers/footers (remove these)")
            score -= 5
        
        # Check for contact info at top
        first_100_chars = text[:100].lower()
        if '@' not in first_100_chars and not re.search(r'\d{10}', first_100_chars):
            issues.append("Contact information should be at the very top")
            score -= 10
        
        return max(0, score), issues
    
    def _check_action_verbs(self, text):
        """Check for weak vs strong action verbs"""
        issues = []
        text_lower = text.lower()
        
        # Count weak verbs
        weak_verb_count = 0
        weak_verbs_found = []
        for verb in self.weak_verbs:
            count = len(re.findall(r'\b' + re.escape(verb), text_lower))
            if count > 0:
                weak_verb_count += count
                weak_verbs_found.append(f"'{verb}' ({count}x)")
        
        # Count strong verbs
        strong_verb_count = 0
        for verb in self.strong_verbs:
            count = len(re.findall(r'\b' + re.escape(verb), text_lower))
            strong_verb_count += count
        
        # Calculate score based on ratio
        total_verbs = weak_verb_count + strong_verb_count
        if total_verbs == 0:
            score = 70  # Neutral if no verbs found
        else:
            strong_ratio = strong_verb_count / total_verbs
            score = int(strong_ratio * 100)
        
        # Add issues
        if weak_verb_count > 0:
            issues.append(f"Found {weak_verb_count} weak action verbs: {', '.join(weak_verbs_found[:3])}")
        
        if weak_verb_count > strong_verb_count:
            issues.append(f"Weak verbs ({weak_verb_count}) outnumber strong verbs ({strong_verb_count})")
        
        if strong_verb_count < 5:
            issues.append("Use more strong action verbs (Developed, Built, Achieved, etc.)")
        
        return max(0, min(100, score)), issues
    
    def _check_keywords(self, text, job_skills):
        """Check keyword density and relevance"""
        issues = []
        
        if not job_skills or len(job_skills) == 0:
            return 50, ["Cannot analyze keywords without job requirements"]
        
        text_lower = text.lower()
        
        # Count how many job skills appear in resume
        matching_keywords = 0
        missing_keywords = []
        keyword_density = {}
        
        for skill in job_skills:
            skill_lower = skill.lower()
            count = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', text_lower))
            
            if count > 0:
                matching_keywords += 1
                keyword_density[skill] = count
            else:
                missing_keywords.append(skill)
        
        # Calculate score
        if len(job_skills) > 0:
            match_ratio = matching_keywords / len(job_skills)
            score = int(match_ratio * 100)
        else:
            score = 50
        
        # Add issues
        if missing_keywords:
            top_missing = missing_keywords[:5]
            issues.append(f"Missing {len(missing_keywords)} key skills from job: {', '.join(top_missing)}")
        
        # Check for keyword stuffing
        for skill, count in keyword_density.items():
            if count > 5:
                issues.append(f"'{skill}' appears {count} times (may look like keyword stuffing)")
        
        if score < 50:
            issues.append(f"Only {matching_keywords}/{len(job_skills)} required skills mentioned")
        
        return max(0, min(100, score)), issues
    
    def _check_length(self, text):
        """Check resume length appropriateness"""
        issues = []
        word_count = len(text.split())
        
        # Ideal length: 400-800 words for students/entry-level
        if word_count < 300:
            issues.append(f"Resume too short ({word_count} words). Add more detail about projects/experience")
            score = 50
        elif word_count < 400:
            issues.append(f"Resume could be longer ({word_count} words). Add more achievements")
            score = 75
        elif word_count <= 800:
            score = 100  # Ideal length
        elif word_count <= 1000:
            issues.append(f"Resume slightly long ({word_count} words). Consider condensing")
            score = 85
        else:
            issues.append(f"Resume too long ({word_count} words). ATS may truncate. Keep under 800 words")
            score = 60
        
        return score, issues
    
    def _generate_suggestions(self, issues, resume_text, job_skills):
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Formatting suggestions
        if issues['formatting']:
            suggestions.append({
                'category': 'Formatting',
                'priority': 'High',
                'action': 'Remove tables and use simple bullet points',
                'impact': '+15 points',
                'details': 'Convert any tables to standard text format with bullet points'
            })
        
        # Verb suggestions
        if issues['verbs']:
            suggestions.append({
                'category': 'Action Verbs',
                'priority': 'High',
                'action': 'Replace weak verbs with strong action verbs',
                'impact': '+10-20 points',
                'details': 'Change "Responsible for" → "Developed", "Worked on" → "Built"'
            })
        
        # Keyword suggestions
        if issues['keywords']:
            # Extract missing keywords
            text_lower = resume_text.lower()
            missing = [skill for skill in job_skills if skill.lower() not in text_lower]
            
            if missing:
                top_missing = missing[:3]
                suggestions.append({
                    'category': 'Keywords',
                    'priority': 'Critical',
                    'action': f'Add missing skills: {", ".join(top_missing)}',
                    'impact': f'+{len(missing) * 3} points',
                    'details': 'Incorporate these skills naturally in your experience/projects section'
                })
        
        # Length suggestions
        if issues['length']:
            word_count = len(resume_text.split())
            if word_count < 400:
                suggestions.append({
                    'category': 'Content',
                    'priority': 'Medium',
                    'action': 'Add more detail and quantify achievements',
                    'impact': '+10 points',
                    'details': 'Include metrics: "Improved X by Y%", "Built system handling Z users"'
                })
        
        # General improvements
        suggestions.append({
            'category': 'Optimization',
            'priority': 'Medium',
            'action': 'Use standard section headers',
            'impact': '+5 points',
            'details': 'Use: EDUCATION, EXPERIENCE, SKILLS, PROJECTS (all caps, standard names)'
        })
        
        return suggestions
    
    def _calculate_potential_score(self, current_score, issues):
        """Calculate potential ATS score after improvements"""
        potential_gain = 0
        
        # Formatting improvements
        if issues['formatting']:
            potential_gain += min(15, len(issues['formatting']) * 5)
        
        # Verb improvements
        if issues['verbs']:
            potential_gain += min(20, len(issues['verbs']) * 7)
        
        # Keyword improvements
        if issues['keywords']:
            potential_gain += min(25, len(issues['keywords']) * 5)
        
        # Length improvements
        if issues['length']:
            potential_gain += 10
        
        # Cap at 95 (no resume is 100% perfect)
        return min(95, current_score + potential_gain)
    
    def _get_category(self, score):
        """Get ATS score category"""
        if score >= 80:
            return "Excellent - High ATS Pass Rate"
        elif score >= 65:
            return "Good - Likely to Pass ATS"
        elif score >= 50:
            return "Fair - May Pass ATS"
        else:
            return "Poor - Unlikely to Pass ATS"


# Helper function for easy use
def analyze_ats(resume_text, job_skills):
    """Analyze resume for ATS compatibility"""
    analyzer = ATSAnalyzer()
    return analyzer.analyze(resume_text, job_skills)