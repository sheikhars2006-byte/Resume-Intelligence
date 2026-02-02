class SkillsGapAnalyzer:
    """Analyze skill gaps and provide learning recommendations"""
    
    def __init__(self):
        # Learning resources database
        self.learning_resources = {
            # Programming Languages
            'python': {
                'resources': [
                    'Python for Everybody (Coursera) - Free',
                    'Automate the Boring Stuff (Book) - Free online',
                    'Python.org Official Tutorial - Free'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Beginner',
                'priority': 'Critical',
                'salary_impact': '₹3-5L base for entry-level'
            },
            'java': {
                'resources': [
                    'Java Programming (Coursera)',
                    'Head First Java (Book)',
                    'Java Tutorial (Oracle) - Free'
                ],
                'time_to_learn': '3-4 months',
                'difficulty': 'Intermediate',
                'priority': 'High',
                'salary_impact': '₹4-6L for Java developers'
            },
            'javascript': {
                'resources': [
                    'freeCodeCamp JavaScript Course - Free',
                    'JavaScript.info - Free',
                    'The Modern JavaScript Tutorial'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Beginner',
                'priority': 'High',
                'salary_impact': '₹4-7L for web developers'
            },
            
            # Data Science & ML
            'machine learning': {
                'resources': [
                    'Andrew Ng Machine Learning (Coursera) - Free audit',
                    'FastAI Practical Deep Learning - Free',
                    'Kaggle Learn - Free'
                ],
                'time_to_learn': '4-6 months',
                'difficulty': 'Intermediate',
                'priority': 'Critical',
                'salary_impact': '₹6-12L for ML roles'
            },
            'deep learning': {
                'resources': [
                    'Deep Learning Specialization (Coursera)',
                    'FastAI Course - Free',
                    'Deep Learning Book (Goodfellow) - Free online'
                ],
                'time_to_learn': '4-6 months',
                'difficulty': 'Advanced',
                'priority': 'High',
                'salary_impact': '₹8-15L for DL specialists'
            },
            'tensorflow': {
                'resources': [
                    'TensorFlow in Practice (Coursera)',
                    'TensorFlow Official Tutorials - Free',
                    'Hands-on Machine Learning (Book)'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Intermediate',
                'priority': 'High',
                'salary_impact': '+₹2-4L over base ML salary'
            },
            'pytorch': {
                'resources': [
                    'PyTorch Official Tutorials - Free',
                    'FastAI Course (uses PyTorch) - Free',
                    'Deep Learning with PyTorch (Book)'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Intermediate',
                'priority': 'High',
                'salary_impact': '+₹2-4L over base ML salary'
            },
            'pandas': {
                'resources': [
                    'Pandas Documentation - Free',
                    'Python for Data Analysis (Book)',
                    'Kaggle Pandas Course - Free'
                ],
                'time_to_learn': '3-4 weeks',
                'difficulty': 'Beginner',
                'priority': 'Critical',
                'salary_impact': 'Essential for data roles'
            },
            'numpy': {
                'resources': [
                    'NumPy Documentation - Free',
                    'NumPy Quickstart Tutorial - Free',
                    'Kaggle Learn - Free'
                ],
                'time_to_learn': '2-3 weeks',
                'difficulty': 'Beginner',
                'priority': 'High',
                'salary_impact': 'Foundation skill'
            },
            
            # Cloud & DevOps
            'aws': {
                'resources': [
                    'AWS Free Tier (Hands-on) - Free',
                    'AWS Certified Cloud Practitioner Course',
                    'AWS Documentation - Free'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Intermediate',
                'priority': 'High',
                'salary_impact': '+₹3-6L with AWS certification'
            },
            'docker': {
                'resources': [
                    'Docker Documentation - Free',
                    'Docker for Beginners (YouTube) - Free',
                    'Play with Docker - Free hands-on'
                ],
                'time_to_learn': '2-4 weeks',
                'difficulty': 'Beginner',
                'priority': 'High',
                'salary_impact': '+₹1-3L for DevOps skills'
            },
            'kubernetes': {
                'resources': [
                    'Kubernetes Documentation - Free',
                    'Kubernetes the Hard Way - Free',
                    'Kubernetes for Beginners (Udemy)'
                ],
                'time_to_learn': '3-4 months',
                'difficulty': 'Advanced',
                'priority': 'Medium',
                'salary_impact': '+₹4-8L for K8s expertise'
            },
            
            # Databases
            'sql': {
                'resources': [
                    'SQLBolt - Free interactive',
                    'Mode SQL Tutorial - Free',
                    'W3Schools SQL - Free'
                ],
                'time_to_learn': '3-4 weeks',
                'difficulty': 'Beginner',
                'priority': 'Critical',
                'salary_impact': 'Essential for data/backend roles'
            },
            'mongodb': {
                'resources': [
                    'MongoDB University - Free courses',
                    'MongoDB Documentation - Free',
                    'The Little MongoDB Book - Free'
                ],
                'time_to_learn': '2-3 weeks',
                'difficulty': 'Beginner',
                'priority': 'Medium',
                'salary_impact': '+₹1-2L for NoSQL knowledge'
            },
            
            # Data Visualization
            'tableau': {
                'resources': [
                    'Tableau Public - Free version',
                    'Tableau Training Videos - Free',
                    'Tableau Desktop Specialist Certification'
                ],
                'time_to_learn': '1-2 months',
                'difficulty': 'Beginner',
                'priority': 'High',
                'salary_impact': '+₹2-4L for BI skills'
            },
            'power bi': {
                'resources': [
                    'Microsoft Power BI Training - Free',
                    'Power BI Documentation - Free',
                    'Power BI Desktop - Free software'
                ],
                'time_to_learn': '1-2 months',
                'difficulty': 'Beginner',
                'priority': 'High',
                'salary_impact': '+₹2-4L for BI skills'
            },
            
            # Web Development
            'react': {
                'resources': [
                    'React Official Tutorial - Free',
                    'freeCodeCamp React - Free',
                    'React Documentation - Free'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Intermediate',
                'priority': 'High',
                'salary_impact': '₹5-10L for React developers'
            },
            'node': {
                'resources': [
                    'Node.js Documentation - Free',
                    'freeCodeCamp Node.js - Free',
                    'The Node.js Handbook - Free'
                ],
                'time_to_learn': '2-3 months',
                'difficulty': 'Intermediate',
                'priority': 'Medium',
                'salary_impact': '₹4-8L for Node developers'
            },
            
            # Version Control
            'git': {
                'resources': [
                    'Git Official Documentation - Free',
                    'GitHub Learning Lab - Free',
                    'Pro Git Book - Free online'
                ],
                'time_to_learn': '1-2 weeks',
                'difficulty': 'Beginner',
                'priority': 'Critical',
                'salary_impact': 'Essential for all dev roles'
            },
            
            # Default for skills not in database
            'default': {
                'resources': [
                    'Search on Coursera, Udemy, YouTube',
                    'Check official documentation',
                    'Practice on Kaggle/GitHub projects'
                ],
                'time_to_learn': '1-3 months',
                'difficulty': 'Varies',
                'priority': 'Medium',
                'salary_impact': 'Skill-dependent'
            }
        }
    
    def analyze(self, resume_skills, job_skills, match_score):
        """Analyze skill gaps and provide learning recommendations"""
        
        # Calculate missing skills
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        missing_skills = []
        for skill in job_skills_lower:
            if skill not in resume_skills_lower:
                missing_skills.append(skill)
        
        # Prioritize and score each missing skill
        prioritized_skills = self._prioritize_skills(missing_skills, match_score)
        
        # Generate learning plan
        learning_plan = self._create_learning_plan(prioritized_skills)
        
        # Calculate total time investment
        total_time = self._calculate_total_time(prioritized_skills)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            prioritized_skills,
            match_score,
            len(missing_skills)
        )
        
        return {
            'missing_skills_count': len(missing_skills),
            'prioritized_skills': prioritized_skills,
            'learning_plan': learning_plan,
            'total_time_estimate': total_time,
            'recommendations': recommendations,
            'skill_categories': self._categorize_skills(prioritized_skills)
        }
    
    def _prioritize_skills(self, missing_skills, current_match_score):
        """Prioritize skills by impact on match score"""
        prioritized = []
        
        for skill in missing_skills:
            skill_info = self.learning_resources.get(
                skill.lower(),
                self.learning_resources['default']
            )
            
            # Calculate impact score (0-100)
            impact_score = self._calculate_impact(skill, skill_info, current_match_score)
            
            prioritized.append({
                'skill': skill.title(),
                'impact_score': impact_score,
                'priority': skill_info['priority'],
                'resources': skill_info['resources'],
                'time_to_learn': skill_info['time_to_learn'],
                'difficulty': skill_info['difficulty'],
                'salary_impact': skill_info['salary_impact']
            })
        
        # Sort by impact score (descending)
        prioritized.sort(key=lambda x: x['impact_score'], reverse=True)
        
        return prioritized
    
    def _calculate_impact(self, skill, skill_info, current_score):
        """Calculate how much learning this skill would improve match score"""
        
        # Base impact on priority
        priority_scores = {
            'Critical': 15,
            'High': 10,
            'Medium': 6,
            'Low': 3
        }
        
        base_impact = priority_scores.get(skill_info['priority'], 5)
        
        # Adjust based on current match score (lower score = higher impact)
        if current_score < 50:
            multiplier = 1.5
        elif current_score < 70:
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        # Additional weight for commonly required skills
        critical_skills = ['python', 'sql', 'machine learning', 'git']
        if skill.lower() in critical_skills:
            base_impact += 5
        
        return min(20, int(base_impact * multiplier))
    
    def _create_learning_plan(self, prioritized_skills):
        """Create a structured learning plan"""
        
        if not prioritized_skills:
            return {
                'phase_1': [],
                'phase_2': [],
                'phase_3': []
            }
        
        # Divide into 3 phases based on priority and difficulty
        critical_beginner = []
        high_priority = []
        medium_low = []
        
        for skill_data in prioritized_skills:
            if skill_data['priority'] == 'Critical' or skill_data['difficulty'] == 'Beginner':
                critical_beginner.append(skill_data)
            elif skill_data['priority'] == 'High':
                high_priority.append(skill_data)
            else:
                medium_low.append(skill_data)
        
        return {
            'phase_1': critical_beginner[:3],  # Start with top 3 critical/beginner
            'phase_2': high_priority[:3],      # Next 3 high priority
            'phase_3': medium_low[:3]          # Finally medium/low priority
        }
    
    def _calculate_total_time(self, prioritized_skills):
        """Calculate total time needed to learn missing skills"""
        
        if not prioritized_skills:
            return "No skills to learn"
        
        # Parse time estimates and sum up (roughly)
        time_mapping = {
            'weeks': 7,    # days
            'week': 7,
            'months': 30,  # days
            'month': 30
        }
        
        total_days = 0
        for skill_data in prioritized_skills[:5]:  # Top 5 skills
            time_str = skill_data['time_to_learn'].lower()
            
            for unit, days_per_unit in time_mapping.items():
                if unit in time_str:
                    # Extract number
                    import re
                    numbers = re.findall(r'\d+', time_str)
                    if numbers:
                        avg_num = sum(map(int, numbers)) / len(numbers)
                        total_days += avg_num * days_per_unit
                        break
        
        # Convert to months
        total_months = round(total_days / 30, 1)
        
        if total_months < 1:
            return "2-3 weeks (focusing on top priorities)"
        elif total_months < 2:
            return "1-2 months (focused learning)"
        elif total_months < 4:
            return f"{int(total_months)} months (part-time study)"
        else:
            return f"{int(total_months)} months (comprehensive upskilling)"
    
    def _generate_recommendations(self, prioritized_skills, match_score, missing_count):
        """Generate personalized recommendations"""
        
        recommendations = []
        
        if not prioritized_skills:
            return ["✅ You have all required skills! Focus on building projects to demonstrate expertise."]
        
        # Recommendation based on gap size
        if missing_count > 5:
            recommendations.append(
                f"🎯 You're missing {missing_count} skills. Focus on the top 3-5 high-impact skills first."
            )
        elif missing_count > 2:
            recommendations.append(
                f"📚 Learn the {missing_count} missing skills to significantly boost your match score."
            )
        else:
            recommendations.append(
                f"🚀 Only {missing_count} skill(s) missing! You're very close to being a perfect fit."
            )
        
        # Recommendation based on current score
        if match_score < 50:
            recommendations.append(
                "⚠️ Current match is low. Prioritize Critical and High priority skills for maximum impact."
            )
        elif match_score < 70:
            recommendations.append(
                "📈 Good foundation! Learning top 3 missing skills could push you to 80%+ match."
            )
        else:
            recommendations.append(
                "💪 Strong match already! These additional skills would make you an ideal candidate."
            )
        
        # Specific action items
        if prioritized_skills:
            top_skill = prioritized_skills[0]
            recommendations.append(
                f"🎓 Start with: {top_skill['skill']} - Highest impact (+{top_skill['impact_score']} points)"
            )
        
        # Time-based recommendation
        recommendations.append(
            "⏱️ Set aside 5-10 hours per week for focused learning to see progress in 1-2 months."
        )
        
        # Project-based learning
        recommendations.append(
            "💡 Build projects using new skills - this helps with learning AND strengthens your resume."
        )
        
        return recommendations
    
    def _categorize_skills(self, prioritized_skills):
        """Categorize skills by type"""
        
        categories = {
            'Programming': [],
            'Data Science/ML': [],
            'Cloud/DevOps': [],
            'Databases': [],
            'Web Development': [],
            'Tools': [],
            'Other': []
        }
        
        skill_categories = {
            'python': 'Programming',
            'java': 'Programming',
            'javascript': 'Programming',
            'c++': 'Programming',
            'machine learning': 'Data Science/ML',
            'deep learning': 'Data Science/ML',
            'tensorflow': 'Data Science/ML',
            'pytorch': 'Data Science/ML',
            'pandas': 'Data Science/ML',
            'numpy': 'Data Science/ML',
            'aws': 'Cloud/DevOps',
            'azure': 'Cloud/DevOps',
            'docker': 'Cloud/DevOps',
            'kubernetes': 'Cloud/DevOps',
            'sql': 'Databases',
            'mongodb': 'Databases',
            'postgresql': 'Databases',
            'react': 'Web Development',
            'node': 'Web Development',
            'angular': 'Web Development',
            'git': 'Tools',
            'tableau': 'Tools',
            'power bi': 'Tools'
        }
        
        for skill_data in prioritized_skills:
            skill_lower = skill_data['skill'].lower()
            category = skill_categories.get(skill_lower, 'Other')
            categories[category].append(skill_data)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}


# Helper function
def analyze_skills_gap(resume_skills, job_skills, match_score):
    """Analyze skill gaps and get learning recommendations"""
    analyzer = SkillsGapAnalyzer()
    return analyzer.analyze(resume_skills, job_skills, match_score)