"""
Essay Writing Service for Clang Chatbot
Generates well-structured essays on any topic within 200 words
"""

import re
from typing import Dict, List

class EssayWritingService:
    def __init__(self):
        self.essay_templates = self._load_essay_templates()
        self.topic_keywords = self._load_topic_keywords()
        
    def _load_essay_templates(self) -> Dict:
        """Load different essay structure templates"""
        return {
            'argumentative': {
                'structure': ['introduction', 'argument_1', 'argument_2', 'counterargument', 'conclusion'],
                'intro_starters': ['In today\'s world', 'The debate surrounding', 'Many people believe', 'It is widely argued'],
                'argument_starters': ['Firstly', 'Moreover', 'Additionally', 'Furthermore'],
                'conclusion_starters': ['In conclusion', 'To summarize', 'Therefore', 'In summary']
            },
            'descriptive': {
                'structure': ['introduction', 'main_features', 'detailed_description', 'conclusion'],
                'intro_starters': ['Imagine', 'Picture', 'Consider', 'Envision'],
                'description_starters': ['Notably', 'Particularly', 'Remarkably', 'Significantly'],
                'conclusion_starters': ['In essence', 'Ultimately', 'Overall', 'In summary']
            },
            'expository': {
                'structure': ['introduction', 'explanation_1', 'explanation_2', 'examples', 'conclusion'],
                'intro_starters': ['Understanding', 'To comprehend', 'It is important to know', 'Learning about'],
                'explanation_starters': ['First', 'Next', 'Then', 'Subsequently'],
                'conclusion_starters': ['In conclusion', 'Thus', 'Therefore', 'As a result']
            },
            'narrative': {
                'structure': ['setting', 'characters', 'conflict', 'resolution', 'conclusion'],
                'intro_starters': ['Once upon a time', 'In a distant land', 'Long ago', 'There was once'],
                'transition_starters': ['Suddenly', 'Meanwhile', 'At that moment', 'Just then'],
                'conclusion_starters': ['Finally', 'In the end', 'Eventually', 'At last']
            }
        }
    
    def _load_topic_keywords(self) -> Dict:
        """Load topic categories and related keywords"""
        return {
            'technology': {
                'keywords': ['artificial intelligence', 'computer', 'internet', 'smartphone', 'social media', 'automation', 'digital'],
                'essay_type': 'argumentative',
                'key_points': ['benefits', 'drawbacks', 'future implications', 'societal impact']
            },
            'environment': {
                'keywords': ['climate change', 'pollution', 'conservation', 'renewable energy', 'sustainability', 'global warming'],
                'essay_type': 'expository',
                'key_points': ['causes', 'effects', 'solutions', 'importance']
            },
            'education': {
                'keywords': ['learning', 'school', 'university', 'knowledge', 'teaching', 'students', 'curriculum'],
                'essay_type': 'argumentative',
                'key_points': ['importance', 'challenges', 'improvements', 'methods']
            },
            'health': {
                'keywords': ['exercise', 'nutrition', 'wellness', 'mental health', 'fitness', 'lifestyle', 'medicine'],
                'essay_type': 'expository',
                'key_points': ['benefits', 'importance', 'recommendations', 'research']
            },
            'history': {
                'keywords': ['ancient', 'medieval', 'war', 'civilization', 'culture', 'historical', 'past'],
                'essay_type': 'narrative',
                'key_points': ['background', 'events', 'consequences', 'significance']
            },
            'literature': {
                'keywords': ['novel', 'poetry', 'author', 'character', 'theme', 'symbolism', 'analysis'],
                'essay_type': 'descriptive',
                'key_points': ['themes', 'characters', 'style', 'significance']
            },
            'science': {
                'keywords': ['research', 'experiment', 'discovery', 'theory', 'scientific', 'hypothesis', 'innovation'],
                'essay_type': 'expository',
                'key_points': ['explanation', 'evidence', 'applications', 'importance']
            },
            'social_issues': {
                'keywords': ['society', 'community', 'inequality', 'justice', 'rights', 'social', 'culture'],
                'essay_type': 'argumentative',
                'key_points': ['problems', 'causes', 'solutions', 'implications']
            },
            'business': {
                'keywords': ['business', 'economy', 'marketing', 'entrepreneurship', 'leadership', 'management', 'finance'],
                'essay_type': 'expository',
                'key_points': ['strategies', 'challenges', 'opportunities', 'trends']
            },
            'psychology': {
                'keywords': ['psychology', 'behavior', 'mental', 'cognitive', 'emotional', 'therapy', 'personality'],
                'essay_type': 'descriptive',
                'key_points': ['theories', 'research', 'applications', 'implications']
            },
            'philosophy': {
                'keywords': ['philosophy', 'ethics', 'morality', 'existence', 'truth', 'knowledge', 'reality'],
                'essay_type': 'argumentative',
                'key_points': ['arguments', 'perspectives', 'implications', 'analysis']
            },
            'art_culture': {
                'keywords': ['art', 'culture', 'music', 'painting', 'sculpture', 'theater', 'dance', 'creativity'],
                'essay_type': 'descriptive',
                'key_points': ['significance', 'influence', 'techniques', 'impact']
            },
            'sports_fitness': {
                'keywords': ['sports', 'fitness', 'exercise', 'athletics', 'competition', 'physical', 'training'],
                'essay_type': 'expository',
                'key_points': ['benefits', 'techniques', 'importance', 'development']
            },
            'travel': {
                'keywords': ['travel', 'tourism', 'culture', 'adventure', 'exploration', 'vacation', 'journey'],
                'essay_type': 'narrative',
                'key_points': ['experiences', 'benefits', 'challenges', 'discoveries']
            },
            'food_nutrition': {
                'keywords': ['food', 'nutrition', 'diet', 'cooking', 'health', 'recipe', 'eating'],
                'essay_type': 'expository',
                'key_points': ['benefits', 'importance', 'choices', 'impact']
            },
            'family_relationships': {
                'keywords': ['family', 'relationships', 'friendship', 'love', 'marriage', 'parenting', 'communication'],
                'essay_type': 'descriptive',
                'key_points': ['importance', 'challenges', 'benefits', 'dynamics']
            },
            'current_events': {
                'keywords': ['current events', 'news', 'politics', 'government', 'elections', 'policy', 'society'],
                'essay_type': 'argumentative',
                'key_points': ['analysis', 'implications', 'perspectives', 'solutions']
            },
            'space_astronomy': {
                'keywords': ['space', 'astronomy', 'universe', 'planets', 'stars', 'exploration', 'NASA'],
                'essay_type': 'expository',
                'key_points': ['discoveries', 'exploration', 'significance', 'future']
            },
            'personal_development': {
                'keywords': ['personal development', 'self-improvement', 'goals', 'success', 'motivation', 'habits'],
                'essay_type': 'expository',
                'key_points': ['strategies', 'importance', 'methods', 'benefits']
            }
        }
    
    def identify_topic_category(self, topic: str) -> str:
        """Identify the category of the essay topic"""
        topic_lower = topic.lower()
        
        for category, info in self.topic_keywords.items():
            if any(keyword in topic_lower for keyword in info['keywords']):
                return category
        
        # Default to expository if no specific category found
        return 'general'
    
    def generate_essay(self, topic: str, word_limit: int = 200) -> str:
        """Generate a well-structured essay on the given topic"""
        topic_category = self.identify_topic_category(topic)
        
        # Determine essay type
        if topic_category in self.topic_keywords:
            essay_type = self.topic_keywords[topic_category]['essay_type']
            key_points = self.topic_keywords[topic_category]['key_points']
        else:
            essay_type = 'expository'
            key_points = ['overview', 'details', 'examples', 'significance']
        
        template = self.essay_templates[essay_type]
        
        # Generate essay content
        essay_parts = []
        
        # Introduction (40-50 words)
        intro = self._generate_introduction(topic, template, topic_category)
        essay_parts.append(intro)
        
        # Body paragraphs (100-120 words)
        body = self._generate_body(topic, template, key_points, topic_category)
        essay_parts.extend(body)
        
        # Conclusion (40-50 words)
        conclusion = self._generate_conclusion(topic, template, topic_category)
        essay_parts.append(conclusion)
        
        # Combine and format
        full_essay = '\n\n'.join(essay_parts)
        
        # Ensure word limit
        full_essay = self._adjust_word_count(full_essay, word_limit)
        
        return full_essay
    
    def _generate_introduction(self, topic: str, template: Dict, category: str) -> str:
        """Generate the introduction paragraph"""
        starters = template.get('intro_starters', ['In today\'s world', 'It is important to understand'])
        starter = starters[hash(topic) % len(starters)]
        
        if category == 'technology':
            return f"{starter}, technology plays an increasingly vital role in our daily lives. {topic.title()} has become a significant aspect of modern society, influencing how we work, communicate, and live. Understanding its impact is crucial for navigating our digital future."
        
        elif category == 'environment':
            return f"{starter}, environmental concerns have become more pressing than ever. {topic.title()} represents one of the most critical challenges facing humanity today. Addressing this issue requires immediate attention and collective action."
        
        elif category == 'education':
            return f"{starter}, education remains the cornerstone of human development and societal progress. {topic.title()} plays a fundamental role in shaping minds and building the foundation for future success and innovation."
        
        elif category == 'health':
            return f"{starter}, maintaining good health has become increasingly important in our fast-paced world. {topic.title()} is essential for achieving optimal well-being and improving quality of life for individuals and communities."
        
        elif category == 'business':
            return f"{starter}, the modern business landscape continues to evolve rapidly. {topic.title()} represents a crucial aspect of contemporary commerce and organizational success. Understanding these dynamics is essential for effective leadership and strategic planning."
        
        elif category == 'psychology':
            return f"{starter}, human behavior and mental processes fascinate researchers and practitioners alike. {topic.title()} offers valuable insights into the complexities of the human mind and its impact on individual and social functioning."
        
        elif category == 'philosophy':
            return f"{starter}, philosophical inquiry has shaped human thought for millennia. {topic.title()} raises fundamental questions about existence, knowledge, and values that continue to challenge and inspire contemporary thinkers."
        
        elif category == 'art_culture':
            return f"{starter}, artistic expression serves as a mirror to society and human experience. {topic.title()} represents an important cultural phenomenon that enriches our understanding of creativity, beauty, and human expression."
        
        elif category == 'sports_fitness':
            return f"{starter}, physical activity and athletic pursuits play vital roles in human development and society. {topic.title()} demonstrates the profound impact of sports and fitness on individual health, character development, and community building."
        
        else:
            return f"{starter}, {topic.lower()} is a topic that deserves careful consideration and analysis. Understanding its various aspects and implications helps us gain valuable insights into this important subject matter."
    
    def _generate_body(self, topic: str, template: Dict, key_points: List[str], category: str) -> List[str]:
        """Generate body paragraphs"""
        body_paragraphs = []
        
        # Generate 2 main body paragraphs
        if category == 'technology':
            para1 = f"Firstly, {topic.lower()} offers numerous benefits that enhance productivity and connectivity. It streamlines processes, improves communication, and provides access to vast amounts of information. These advantages have revolutionized industries and transformed how we approach daily tasks."
            
            para2 = f"However, {topic.lower()} also presents certain challenges and concerns. Issues such as privacy, security, and potential job displacement require careful consideration. Balancing technological advancement with ethical considerations remains an ongoing challenge for society."
            
        elif category == 'environment':
            para1 = f"The causes of {topic.lower()} are multifaceted and interconnected. Human activities, industrial processes, and lifestyle choices all contribute to this issue. Understanding these root causes is essential for developing effective solutions."
            
            para2 = f"The effects of {topic.lower()} are far-reaching and impact both current and future generations. From ecosystem disruption to economic consequences, the implications extend across multiple sectors. Immediate action is necessary to mitigate these effects."
            
        elif category == 'education':
            para1 = f"The importance of {topic.lower()} cannot be overstated in personal and professional development. It provides individuals with knowledge, skills, and critical thinking abilities necessary for success. Quality education opens doors to opportunities and empowers people to contribute meaningfully to society."
            
            para2 = f"Modern approaches to {topic.lower()} have evolved to meet changing needs and technological advances. Interactive learning methods, personalized instruction, and digital resources have transformed the educational landscape, making learning more accessible and effective."
            
        elif category == 'health':
            para1 = f"Research consistently demonstrates the significant benefits of {topic.lower()} for physical and mental well-being. Regular attention to this aspect of health can prevent various diseases, improve energy levels, and enhance overall quality of life."
            
            para2 = f"Implementing {topic.lower()} into daily routines requires commitment and practical strategies. Setting realistic goals, creating supportive environments, and seeking professional guidance when needed are key factors for long-term success."
            
        elif category == 'business':
            para1 = f"In the competitive business environment, {topic.lower()} has emerged as a critical factor for organizational success. Companies that effectively implement these strategies often experience improved performance, increased profitability, and enhanced market positioning."
            
            para2 = f"However, {topic.lower()} also presents unique challenges and considerations. Businesses must carefully balance innovation with risk management, ensuring sustainable growth while adapting to rapidly changing market conditions and consumer expectations."
            
        elif category == 'philosophy':
            para1 = f"Philosophical examination of {topic.lower()} reveals fundamental questions about human nature and existence. Various schools of thought offer different perspectives, each contributing valuable insights to our understanding of this complex subject."
            
            para2 = f"The practical implications of {topic.lower()} extend beyond academic discourse into everyday decision-making and moral reasoning. These philosophical principles influence how individuals and societies approach ethical dilemmas and life choices."
            
        elif category == 'art_culture':
            para1 = f"The artistic significance of {topic.lower()} reflects broader cultural values and social movements. Through creative expression, artists communicate complex emotions, challenge conventions, and inspire audiences to see the world from new perspectives."
            
            para2 = f"Furthermore, {topic.lower()} serves as a bridge between different cultures and generations. It preserves historical narratives while simultaneously pushing boundaries and exploring innovative forms of human expression and creativity."
            
        elif category == 'sports_fitness':
            para1 = f"The physical benefits of {topic.lower()} are well-documented and extensive. Regular participation improves cardiovascular health, builds strength and endurance, enhances coordination, and contributes to overall physical fitness and longevity."
            
            para2 = f"Beyond physical advantages, {topic.lower()} develops important life skills and character traits. Discipline, teamwork, perseverance, and goal-setting abilities gained through athletic pursuits translate into success in academic, professional, and personal endeavors."
            
        else:
            para1 = f"Examining {topic.lower()} reveals several important aspects that merit attention. The complexity of this subject requires thorough analysis to understand its various dimensions and implications for different stakeholders involved."
            
            para2 = f"Furthermore, {topic.lower()} has significant practical applications and real-world relevance. Its influence extends beyond theoretical understanding, affecting daily life and decision-making processes in meaningful ways."
        
        body_paragraphs.extend([para1, para2])
        return body_paragraphs
    
    def _generate_conclusion(self, topic: str, template: Dict, category: str) -> str:
        """Generate the conclusion paragraph"""
        starters = template.get('conclusion_starters', ['In conclusion', 'To summarize'])
        starter = starters[hash(topic) % len(starters)]
        
        if category == 'technology':
            return f"{starter}, {topic.lower()} represents both tremendous opportunities and significant challenges for society. While it offers unprecedented capabilities and convenience, responsible development and implementation are crucial. Moving forward, striking the right balance between innovation and ethical considerations will determine its ultimate impact on humanity."
        
        elif category == 'environment':
            return f"{starter}, addressing {topic.lower()} requires urgent and coordinated global action. The stakes are too high to delay meaningful intervention. Through collective effort, sustainable practices, and innovative solutions, we can work toward a healthier planet for future generations."
        
        elif category == 'education':
            return f"{starter}, {topic.lower()} remains fundamental to human progress and societal development. Investing in quality education and adapting to modern needs ensures that individuals and communities can thrive in an ever-changing world. The future depends on our commitment to educational excellence."
        
        elif category == 'health':
            return f"{starter}, prioritizing {topic.lower()} is an investment in long-term well-being and happiness. The benefits extend beyond individual health to impact families, communities, and society as a whole. Making informed choices today creates the foundation for a healthier tomorrow."
        
        elif category == 'business':
            return f"{starter}, {topic.lower()} remains essential for business success in an increasingly competitive marketplace. Organizations that embrace these principles while maintaining ethical standards are best positioned for sustainable growth and positive societal impact."
        
        elif category == 'philosophy':
            return f"{starter}, {topic.lower()} continues to offer profound insights into the human condition and our place in the universe. These timeless questions challenge us to think critically and live more thoughtfully, enriching both individual lives and collective understanding."
        
        elif category == 'art_culture':
            return f"{starter}, {topic.lower()} enriches human experience and fosters deeper understanding across diverse communities. Its power to inspire, challenge, and unite makes it an invaluable component of a vibrant and meaningful society."
        
        elif category == 'sports_fitness':
            return f"{starter}, {topic.lower()} contributes significantly to individual development and social cohesion. The lessons learned through athletic pursuits create healthier individuals and stronger communities, making sports and fitness essential elements of modern life."
        
        else:
            return f"{starter}, {topic.lower()} is a multifaceted subject that requires continued exploration and understanding. Its relevance to our lives and society makes it worthy of ongoing attention and study. Through careful analysis and thoughtful consideration, we can better appreciate its significance."
    
    def _adjust_word_count(self, essay: str, target_words: int) -> str:
        """Adjust essay to meet word count requirements"""
        words = essay.split()
        current_count = len(words)
        
        if current_count <= target_words:
            return essay
        
        # If too long, trim while maintaining structure
        # Keep introduction and conclusion, trim body paragraphs
        paragraphs = essay.split('\n\n')
        
        if len(paragraphs) >= 4:  # intro + 2 body + conclusion
            # Trim body paragraphs proportionally
            words_to_remove = current_count - target_words
            
            # Trim from body paragraphs (index 1 and 2)
            for i in [1, 2]:
                if i < len(paragraphs) and words_to_remove > 0:
                    para_words = paragraphs[i].split()
                    trim_amount = min(len(para_words) // 4, words_to_remove // 2)
                    if trim_amount > 0:
                        paragraphs[i] = ' '.join(para_words[:-trim_amount])
                        words_to_remove -= trim_amount
            
            return '\n\n'.join(paragraphs)
        
        # If structure is different, just trim from the end
        return ' '.join(words[:target_words])
    
    def is_essay_request(self, query: str) -> bool:
        """Check if the query is requesting an essay"""
        essay_keywords = [
            'write an essay', 'essay on', 'essay about', 'write about',
            'composition on', 'article on', 'piece about', 'essay'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in essay_keywords)
    
    def extract_essay_topic(self, query: str) -> str:
        """Extract the topic from an essay request"""
        query_lower = query.lower()
        
        # Common patterns for essay requests
        patterns = [
            r'write an essay (?:on|about) (.+)',
            r'essay (?:on|about) (.+)',
            r'write about (.+)',
            r'composition (?:on|about) (.+)',
            r'article (?:on|about) (.+)',
            r'essay (.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, remove common essay keywords and use the rest
        essay_keywords = ['write an essay', 'essay on', 'essay about', 'write about', 'essay']
        topic = query_lower
        for keyword in essay_keywords:
            topic = topic.replace(keyword, '').strip()
        
        return topic if topic else 'general topic'
    
    def get_essay_response(self, query: str) -> str:
        """Get essay response - this is the main method expected by views.py"""
        topic = self.extract_essay_topic(query)
        return self.generate_essay(topic)

# Global instance
essay_writing_service = EssayWritingService()
