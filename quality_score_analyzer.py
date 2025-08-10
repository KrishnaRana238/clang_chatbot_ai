#!/usr/bin/env python3
"""
Quality Score Analysis Tool
Analyzes why the chatbot isn't achieving perfect 10/10 scores
and identifies specific improvement areas
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class QualityAnalyzer:
    def __init__(self):
        self.session_id = f"quality_analysis_{int(time.time())}"
    
    def make_request(self, prompt):
        """Make API request and return response"""
        try:
            response = requests.post(f"{BASE_URL}/api/chat/", 
                                   json={'message': prompt, 'session_id': self.session_id}, 
                                   timeout=30)
            if response.status_code == 200:
                content = response.json()
                return content.get('response', str(content))
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def detailed_quality_analysis(self, text, test_name, keywords=None):
        """Perform detailed quality analysis showing each scoring criterion"""
        print(f"\n{'='*80}")
        print(f"🔍 DETAILED QUALITY ANALYSIS: {test_name}")
        print(f"{'='*80}")
        
        analysis = {
            'length_score': 0,
            'relevance_score': 0,
            'structure_score': 0,
            'technical_score': 0,
            'completeness_score': 0,
            'total_score': 0,
            'max_score': 10,
            'issues': [],
            'strengths': []
        }
        
        print(f"📝 Response Text ({len(text)} characters):")
        print(f"   {text[:200]}{'...' if len(text) > 200 else ''}")
        print()
        
        # 1. Length Assessment (2 points max)
        print("1️⃣  LENGTH ASSESSMENT (2 points max):")
        if len(text) >= 150:  # Good length threshold
            analysis['length_score'] = 2
            print("   ✅ +2 points: Response has appropriate length")
            analysis['strengths'].append("Appropriate response length")
        elif len(text) >= 50:
            analysis['length_score'] = 1
            print("   ⚠️  +1 point: Response is acceptable but could be more detailed")
            analysis['issues'].append(f"Could be more detailed ({len(text)} chars)")
        else:
            analysis['length_score'] = 0
            print("   ❌ +0 points: Response is too short")
            analysis['issues'].append(f"Too short ({len(text)} chars)")
        
        # 2. Relevance Assessment (2 points max)
        print("\n2️⃣  RELEVANCE ASSESSMENT (2 points max):")
        if keywords:
            found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
            relevance_ratio = len(found_keywords) / len(keywords)
            
            if relevance_ratio >= 0.7:  # 70% keywords found
                analysis['relevance_score'] = 2
                print(f"   ✅ +2 points: High relevance ({len(found_keywords)}/{len(keywords)} keywords found)")
                analysis['strengths'].append(f"High keyword relevance ({len(found_keywords)}/{len(keywords)})")
            elif relevance_ratio >= 0.4:  # 40% keywords found
                analysis['relevance_score'] = 1
                print(f"   ⚠️  +1 point: Moderate relevance ({len(found_keywords)}/{len(keywords)} keywords found)")
                analysis['issues'].append(f"Missing some key terms ({len(found_keywords)}/{len(keywords)})")
            else:
                analysis['relevance_score'] = 0
                print(f"   ❌ +0 points: Low relevance ({len(found_keywords)}/{len(keywords)} keywords found)")
                analysis['issues'].append(f"Low keyword relevance ({len(found_keywords)}/{len(keywords)})")
            
            print(f"   📋 Expected keywords: {keywords}")
            print(f"   ✓ Found keywords: {found_keywords}")
        else:
            analysis['relevance_score'] = 1  # Default for no keywords
            print("   ➖ +1 point: No specific keywords to check")
        
        # 3. Structure Assessment (2 points max)
        print("\n3️⃣  STRUCTURE ASSESSMENT (2 points max):")
        structure_indicators = [
            ('\n\n', 'paragraph breaks'),
            ('**', 'bold formatting'),
            ('#', 'headers'),
            ('1.', 'numbered lists'),
            ('•', 'bullet points'),
            ('-', 'dash lists')
        ]
        
        found_structure = []
        for indicator, name in structure_indicators:
            if indicator in text:
                found_structure.append(name)
        
        if len(found_structure) >= 2:
            analysis['structure_score'] = 2
            print(f"   ✅ +2 points: Well-structured with {', '.join(found_structure)}")
            analysis['strengths'].append("Well-structured response")
        elif len(found_structure) >= 1:
            analysis['structure_score'] = 1
            print(f"   ⚠️  +1 point: Some structure with {', '.join(found_structure)}")
            analysis['issues'].append("Could improve structure formatting")
        else:
            analysis['structure_score'] = 0
            print("   ❌ +0 points: Lacks clear structure")
            analysis['issues'].append("Lacks clear structure (no paragraphs, headers, or lists)")
        
        # 4. Technical Accuracy (2 points max)
        print("\n4️⃣  TECHNICAL ACCURACY (2 points max):")
        technical_indicators = [
            ('disclaimer', 'disclaimers'),
            ('note:', 'important notes'),
            ('def ', 'code functions'),
            ('function', 'function definitions'),
            ('=', 'equations/assignments'),
            ('important:', 'safety warnings'),
            ('however', 'balanced analysis'),
            ('therefore', 'logical conclusions')
        ]
        
        found_technical = []
        for indicator, name in technical_indicators:
            if indicator.lower() in text.lower():
                found_technical.append(name)
        
        if len(found_technical) >= 2:
            analysis['technical_score'] = 2
            print(f"   ✅ +2 points: Good technical elements: {', '.join(found_technical[:3])}")
            analysis['strengths'].append("Appropriate technical elements")
        elif len(found_technical) >= 1:
            analysis['technical_score'] = 1
            print(f"   ⚠️  +1 point: Some technical elements: {', '.join(found_technical)}")
            analysis['issues'].append("Could include more technical details")
        else:
            analysis['technical_score'] = 0
            print("   ❌ +0 points: Lacks technical accuracy indicators")
            analysis['issues'].append("Missing technical accuracy indicators")
        
        # 5. Completeness Assessment (2 points max)
        print("\n5️⃣  COMPLETENESS ASSESSMENT (2 points max):")
        if len(text) > 100 and not text.strip().endswith('...'):
            analysis['completeness_score'] = 2
            print("   ✅ +2 points: Response appears complete")
            analysis['strengths'].append("Complete response")
        elif len(text) > 50:
            analysis['completeness_score'] = 1
            print("   ⚠️  +1 point: Response seems mostly complete")
            analysis['issues'].append("Response could be more comprehensive")
        else:
            analysis['completeness_score'] = 0
            print("   ❌ +0 points: Response appears incomplete")
            analysis['issues'].append("Response appears incomplete or truncated")
        
        # Calculate total score
        analysis['total_score'] = (analysis['length_score'] + 
                                 analysis['relevance_score'] + 
                                 analysis['structure_score'] + 
                                 analysis['technical_score'] + 
                                 analysis['completeness_score'])
        
        percentage = (analysis['total_score'] / analysis['max_score']) * 100
        
        print(f"\n📊 SCORING BREAKDOWN:")
        print(f"   Length Score:      {analysis['length_score']}/2")
        print(f"   Relevance Score:   {analysis['relevance_score']}/2")
        print(f"   Structure Score:   {analysis['structure_score']}/2")
        print(f"   Technical Score:   {analysis['technical_score']}/2")
        print(f"   Completeness Score: {analysis['completeness_score']}/2")
        print(f"   ────────────────────────────")
        print(f"   TOTAL SCORE:       {analysis['total_score']}/10 ({percentage:.1f}%)")
        
        # Grade assignment
        if percentage >= 90:
            grade = "🥇 EXCELLENT"
        elif percentage >= 80:
            grade = "🥈 VERY GOOD"
        elif percentage >= 70:
            grade = "🥉 GOOD"
        elif percentage >= 60:
            grade = "✅ SATISFACTORY"
        else:
            grade = "❌ NEEDS IMPROVEMENT"
        
        print(f"   GRADE:             {grade}")
        
        if analysis['issues']:
            print(f"\n⚠️  AREAS FOR IMPROVEMENT:")
            for i, issue in enumerate(analysis['issues'], 1):
                print(f"   {i}. {issue}")
        
        if analysis['strengths']:
            print(f"\n💪 STRENGTHS:")
            for i, strength in enumerate(analysis['strengths'], 1):
                print(f"   {i}. {strength}")
        
        return analysis
    
    def analyze_sample_responses(self):
        """Analyze several responses to show why scores aren't perfect"""
        print("🔍 QUALITY SCORE ANALYSIS - Why Not 10/10?")
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*100)
        
        test_cases = [
            {
                'name': 'Simple Math Question',
                'prompt': '25 + 37 = ?',
                'keywords': ['62', 'answer', 'result', 'equals']
            },
            {
                'name': 'Essay Writing',
                'prompt': 'Write a short essay about the benefits of exercise.',
                'keywords': ['exercise', 'health', 'benefits', 'physical', 'fitness']
            },
            {
                'name': 'Technical Question',
                'prompt': 'Explain how machine learning works.',
                'keywords': ['machine learning', 'algorithms', 'data', 'training', 'model']
            },
            {
                'name': 'Creative Writing',
                'prompt': 'Write a short story about a robot discovering emotions.',
                'keywords': ['robot', 'emotions', 'story', 'discovery']
            },
            {
                'name': 'Medical Question',
                'prompt': 'What are the symptoms of diabetes?',
                'keywords': ['diabetes', 'symptoms', 'blood sugar', 'disclaimer']
            }
        ]
        
        total_scores = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 TEST CASE {i}: {test_case['name']}")
            print(f"📝 Prompt: {test_case['prompt']}")
            
            # Get response
            response_text = self.make_request(test_case['prompt'])
            
            if response_text.startswith('Error:'):
                print(f"❌ Failed to get response: {response_text}")
                continue
            
            # Analyze quality
            analysis = self.detailed_quality_analysis(
                response_text, 
                test_case['name'], 
                test_case['keywords']
            )
            
            total_scores.append(analysis['total_score'])
            
            print(f"\n💡 TO GET 10/10, THIS RESPONSE NEEDS:")
            missing_points = 10 - analysis['total_score']
            if missing_points == 0:
                print("   🎉 Nothing! This is already perfect!")
            else:
                suggestions = []
                if analysis['length_score'] < 2:
                    suggestions.append("• More detailed and comprehensive content")
                if analysis['relevance_score'] < 2:
                    suggestions.append("• Include more relevant keywords and specific terms")
                if analysis['structure_score'] < 2:
                    suggestions.append("• Better formatting with headers, bullet points, or paragraphs")
                if analysis['technical_score'] < 2:
                    suggestions.append("• More technical accuracy indicators (disclaimers, equations, etc.)")
                if analysis['completeness_score'] < 2:
                    suggestions.append("• More comprehensive and complete explanations")
                
                for suggestion in suggestions:
                    print(f"   {suggestion}")
            
            time.sleep(2)  # Delay between requests
        
        # Summary analysis
        if total_scores:
            avg_score = sum(total_scores) / len(total_scores)
            print(f"\n{'='*100}")
            print("📈 SUMMARY ANALYSIS")
            print(f"{'='*100}")
            print(f"🔢 Sample Tests Analyzed: {len(total_scores)}")
            print(f"📊 Average Score: {avg_score:.1f}/10")
            print(f"🎯 Target Score: 10.0/10")
            print(f"📉 Gap: {10.0 - avg_score:.1f} points")
            
            print(f"\n🎯 MAIN REASONS FOR NOT ACHIEVING 10/10:")
            print("1. 📏 Length/Detail: Many responses could be more comprehensive")
            print("2. 🔍 Keyword Relevance: Missing specific technical terms or concepts")
            print("3. 🎨 Structure: Lack of formatting (headers, lists, paragraphs)")
            print("4. 🔧 Technical Elements: Missing disclaimers, equations, or technical indicators")
            print("5. ✅ Completeness: Some responses could be more thorough")
            
            print(f"\n💡 HOW TO ACHIEVE 10/10 SCORES:")
            print("• 📝 Provide more detailed responses (150+ words)")
            print("• 🎯 Include all relevant keywords and technical terms")
            print("• 🎨 Use proper formatting (headers, bullet points, paragraphs)")
            print("• 🔧 Add appropriate disclaimers and technical elements")
            print("• ✅ Ensure responses are comprehensive and complete")
            print("• 📚 Use varied vocabulary and sentence structures")
            
            print(f"\n📋 CURRENT SYSTEM STATUS:")
            if avg_score >= 8.0:
                print("🥇 EXCELLENT - System performing very well with minor optimization needed")
            elif avg_score >= 7.0:
                print("🥈 GOOD - System performing well with some areas for improvement")
            else:
                print("🥉 SATISFACTORY - System needs significant improvements")

def main():
    analyzer = QualityAnalyzer()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health/", timeout=5)
        if response.status_code != 200:
            print("❌ Server not running! Please start with: python3 manage.py runserver")
            return
    except:
        print("❌ Cannot connect to server! Please start with: python3 manage.py runserver")
        return
    
    print("✅ Server connected. Starting quality analysis...")
    analyzer.analyze_sample_responses()

if __name__ == "__main__":
    main()
