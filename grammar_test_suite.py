#!/usr/bin/env python3
"""
Grammar and Writing Quality Test Suite
Specifically tests grammar checking, writing quality, and linguistic accuracy
across all services with detailed language analysis
"""

import requests
import json
import time
import re
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class GrammarTestSuite:
    def __init__(self):
        self.results = []
        self.session_id = f"grammar_test_{int(time.time())}"
    
    def make_request(self, endpoint, data=None, method='GET'):
        """Make HTTP request with error handling"""
        try:
            if method == 'POST':
                response = requests.post(f"{BASE_URL}{endpoint}", 
                                       json=data, 
                                       timeout=45)
            else:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            return {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'content': response.text if response.status_code != 200 else response.json(),
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                'status_code': 0,
                'success': False,
                'content': str(e),
                'response_time': 0
            }
    
    def analyze_grammar_quality(self, text):
        """Analyze text for grammar and writing quality indicators"""
        analysis = {
            'word_count': len(text.split()),
            'sentence_count': len([s for s in re.split(r'[.!?]+', text) if s.strip()]),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
            'grammar_score': 0,
            'writing_quality': 0,
            'issues': [],
            'strengths': []
        }
        
        # Grammar indicators (positive)
        grammar_score = 0
        
        # Proper sentence structure
        if analysis['sentence_count'] > 0:
            avg_words_per_sentence = analysis['word_count'] / analysis['sentence_count']
            if 10 <= avg_words_per_sentence <= 25:  # Good sentence length
                grammar_score += 2
                analysis['strengths'].append("✓ Good average sentence length")
            else:
                analysis['issues'].append(f"⚠ Unusual sentence length (avg: {avg_words_per_sentence:.1f} words)")
        
        # Capitalization patterns
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        properly_capitalized = sum(1 for s in sentences if s and s[0].isupper())
        if properly_capitalized >= len(sentences) * 0.8:  # 80% properly capitalized
            grammar_score += 1
            analysis['strengths'].append("✓ Proper capitalization")
        else:
            analysis['issues'].append("⚠ Inconsistent capitalization")
        
        # Punctuation usage
        punctuation_marks = len(re.findall(r'[.!?,:;]', text))
        if punctuation_marks > 0:
            grammar_score += 1
            analysis['strengths'].append("✓ Uses punctuation")
        
        # Paragraph structure
        if analysis['paragraph_count'] > 1:
            grammar_score += 1
            analysis['strengths'].append("✓ Multi-paragraph structure")
        
        # Professional writing indicators
        writing_quality = 0
        
        # Transitional phrases
        transitions = ['however', 'furthermore', 'moreover', 'additionally', 'consequently', 
                      'therefore', 'meanwhile', 'subsequently', 'nevertheless', 'in conclusion']
        found_transitions = sum(1 for t in transitions if t in text.lower())
        if found_transitions > 0:
            writing_quality += 2
            analysis['strengths'].append(f"✓ Uses transitional phrases ({found_transitions})")
        
        # Technical terminology (context-appropriate)
        technical_indicators = ['analysis', 'evaluation', 'implementation', 'methodology', 
                               'approach', 'consideration', 'examination', 'assessment']
        found_technical = sum(1 for t in technical_indicators if t in text.lower())
        if found_technical > 0:
            writing_quality += 1
            analysis['strengths'].append(f"✓ Technical vocabulary ({found_technical})")
        
        # Varied sentence beginnings
        sentence_starters = [s.strip().split()[0].lower() for s in sentences if s.strip()]
        unique_starters = len(set(sentence_starters))
        if unique_starters >= len(sentence_starters) * 0.6:  # 60% unique starters
            writing_quality += 1
            analysis['strengths'].append("✓ Varied sentence beginnings")
        else:
            analysis['issues'].append("⚠ Repetitive sentence patterns")
        
        # Active voice indicators (approximate)
        active_indicators = len(re.findall(r'\b(is|are|was|were|being|been)\s+\w+ed\b', text.lower()))
        total_verbs = len(re.findall(r'\b(is|are|was|were|will|can|should|would|could)\b', text.lower()))
        if total_verbs > 0 and (active_indicators / total_verbs) < 0.3:  # Less than 30% passive
            writing_quality += 1
            analysis['strengths'].append("✓ Predominantly active voice")
        elif active_indicators > total_verbs * 0.5:
            analysis['issues'].append("⚠ Excessive passive voice")
        
        # Specific terminology usage
        if any(term in text.lower() for term in ['disclaimer', 'note:', 'important:', 'please consult']):
            writing_quality += 1
            analysis['strengths'].append("✓ Appropriate disclaimers/notes")
        
        analysis['grammar_score'] = min(grammar_score, 5)  # Max 5 points
        analysis['writing_quality'] = min(writing_quality, 5)  # Max 5 points
        
        return analysis
    
    def test_grammar_and_writing(self):
        """Run comprehensive grammar and writing quality tests"""
        print("📝 GRAMMAR & WRITING QUALITY TEST SUITE")
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Target: {BASE_URL}")
        print("="*70)
        
        test_cases = [
            {
                'name': 'Basic Grammar Check',
                'category': 'grammar',
                'prompt': 'Write a paragraph explaining the water cycle. Focus on proper grammar and sentence structure.',
                'expected_elements': ['evaporation', 'condensation', 'precipitation']
            },
            {
                'name': 'Formal Essay Writing',
                'category': 'essay',
                'prompt': 'Write a formal 250-word essay on "The Benefits of Reading Books" with proper introduction, body, and conclusion.',
                'expected_elements': ['introduction', 'benefits', 'conclusion']
            },
            {
                'name': 'Technical Writing',
                'category': 'technical',
                'prompt': 'Explain how machine learning algorithms work. Use proper technical terminology and clear explanations.',
                'expected_elements': ['algorithms', 'data', 'training', 'model']
            },
            {
                'name': 'Creative Writing Quality',
                'category': 'creative',
                'prompt': 'Write a creative short story about space exploration. Focus on vivid descriptions and proper narrative structure.',
                'expected_elements': ['space', 'exploration', 'story']
            },
            {
                'name': 'Medical Writing Accuracy',
                'category': 'medical',
                'prompt': 'Describe the process of photosynthesis in plants. Include proper scientific terminology and disclaimers.',
                'expected_elements': ['photosynthesis', 'chlorophyll', 'oxygen', 'disclaimer']
            },
            {
                'name': 'Business Communication',
                'category': 'business',
                'prompt': 'Write a professional email explaining project delays to a client. Use appropriate business language.',
                'expected_elements': ['project', 'delay', 'professional']
            },
            {
                'name': 'Academic Analysis',
                'category': 'academic',
                'prompt': 'Analyze the causes and effects of urbanization. Use academic writing style with proper citations format.',
                'expected_elements': ['urbanization', 'causes', 'effects', 'analysis']
            },
            {
                'name': 'Grammar Correction',
                'category': 'correction',
                'prompt': 'Please review and improve this text: "the students was working hard on there projects and they was excited about the results" - fix any grammar errors.',
                'expected_elements': ['were', 'their', 'correction']
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {i}: {test_case['name']}")
            print(f"🔍 Category: {test_case['category']}")
            print(f"📝 Prompt: {test_case['prompt'][:80]}...")
            
            # Make API request
            response = self.make_request('/api/chat/', {
                'message': test_case['prompt'],
                'session_id': self.session_id
            }, 'POST')
            
            if not response['success']:
                print(f"❌ Request failed: {response['content']}")
                continue
            
            # Extract response text
            try:
                content = response['content']
                if isinstance(content, dict):
                    response_text = content.get('response', str(content))
                else:
                    response_text = str(content)
            except:
                response_text = str(response['content'])
            
            # Analyze grammar and writing quality
            analysis = self.analyze_grammar_quality(response_text)
            
            # Calculate overall score
            total_score = analysis['grammar_score'] + analysis['writing_quality']
            max_score = 10
            percentage = (total_score / max_score) * 100
            
            # Determine pass/fail
            passed = percentage >= 60  # 60% threshold
            status = "✅ PASS" if passed else "❌ FAIL"
            
            # Store results
            result = {
                'test_name': test_case['name'],
                'category': test_case['category'],
                'passed': passed,
                'response_time': response['response_time'],
                'word_count': analysis['word_count'],
                'sentence_count': analysis['sentence_count'],
                'paragraph_count': analysis['paragraph_count'],
                'grammar_score': analysis['grammar_score'],
                'writing_quality': analysis['writing_quality'],
                'total_score': total_score,
                'percentage': percentage,
                'strengths': analysis['strengths'],
                'issues': analysis['issues']
            }
            self.results.append(result)
            
            # Print results
            print(f"🏆 Result: {status}")
            print(f"⏱️  Response Time: {response['response_time']:.2f}s")
            print(f"📊 Quality Score: {total_score}/{max_score} ({percentage:.1f}%)")
            print(f"📏 Text Stats: {analysis['word_count']} words, {analysis['sentence_count']} sentences, {analysis['paragraph_count']} paragraphs")
            
            if analysis['strengths']:
                print(f"💪 Strengths: {', '.join(analysis['strengths'][:3])}")  # Show top 3
            
            if analysis['issues']:
                print(f"⚠️  Issues: {', '.join(analysis['issues'][:2])}")  # Show top 2
            
            # Brief delay between tests
            time.sleep(1)
        
        # Generate comprehensive report
        self.generate_grammar_report()
    
    def generate_grammar_report(self):
        """Generate detailed grammar and writing quality report"""
        print(f"\n{'='*80}")
        print("📊 GRAMMAR & WRITING QUALITY REPORT")
        print(f"{'='*80}")
        
        if not self.results:
            print("❌ No test results to analyze")
            return
        
        # Overall statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['passed'])
        pass_rate = (passed_tests / total_tests) * 100
        
        avg_response_time = sum(r['response_time'] for r in self.results) / total_tests
        avg_word_count = sum(r['word_count'] for r in self.results) / total_tests
        avg_grammar_score = sum(r['grammar_score'] for r in self.results) / total_tests
        avg_writing_quality = sum(r['writing_quality'] for r in self.results) / total_tests
        avg_total_score = sum(r['total_score'] for r in self.results) / total_tests
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   ✅ Pass Rate: {passed_tests}/{total_tests} ({pass_rate:.1f}%)")
        print(f"   ⏱️  Average Response Time: {avg_response_time:.2f}s")
        print(f"   📝 Average Word Count: {avg_word_count:.0f} words")
        print(f"   📚 Average Grammar Score: {avg_grammar_score:.1f}/5")
        print(f"   ✨ Average Writing Quality: {avg_writing_quality:.1f}/5")
        print(f"   🏆 Average Total Score: {avg_total_score:.1f}/10 ({(avg_total_score/10)*100:.1f}%)")
        
        # Category breakdown
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category, results in categories.items():
            cat_pass_rate = (sum(1 for r in results if r['passed']) / len(results)) * 100
            cat_avg_score = sum(r['total_score'] for r in results) / len(results)
            cat_avg_words = sum(r['word_count'] for r in results) / len(results)
            
            print(f"   📚 {category.title()}:")
            print(f"      Pass Rate: {cat_pass_rate:.1f}%")
            print(f"      Avg Score: {cat_avg_score:.1f}/10")
            print(f"      Avg Words: {cat_avg_words:.0f}")
        
        # Top performing categories
        category_scores = {cat: sum(r['total_score'] for r in results) / len(results) 
                          for cat, results in categories.items()}
        best_category = max(category_scores, key=category_scores.get)
        worst_category = min(category_scores, key=category_scores.get)
        
        print(f"\n🏅 PERFORMANCE HIGHLIGHTS:")
        print(f"   🥇 Best Category: {best_category.title()} ({category_scores[best_category]:.1f}/10)")
        print(f"   🔧 Needs Work: {worst_category.title()} ({category_scores[worst_category]:.1f}/10)")
        
        # Common strengths and issues
        all_strengths = []
        all_issues = []
        for result in self.results:
            all_strengths.extend(result['strengths'])
            all_issues.extend(result['issues'])
        
        # Count frequency
        strength_counts = {}
        issue_counts = {}
        
        for strength in all_strengths:
            strength_counts[strength] = strength_counts.get(strength, 0) + 1
        
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Top 3 strengths and issues
        top_strengths = sorted(strength_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        if top_strengths:
            print(f"\n💪 COMMON STRENGTHS:")
            for strength, count in top_strengths:
                print(f"   {strength} (appeared {count} times)")
        
        if top_issues:
            print(f"\n⚠️  COMMON ISSUES:")
            for issue, count in top_issues:
                print(f"   {issue} (appeared {count} times)")
        
        # Overall grade
        if pass_rate >= 90:
            grade = "🥇 EXCELLENT"
            grade_desc = "Outstanding grammar and writing quality"
        elif pass_rate >= 75:
            grade = "🥈 GOOD"
            grade_desc = "Good writing with minor improvements needed"
        elif pass_rate >= 60:
            grade = "🥉 SATISFACTORY"
            grade_desc = "Acceptable quality with room for improvement"
        else:
            grade = "❌ NEEDS IMPROVEMENT"
            grade_desc = "Significant grammar and writing issues detected"
        
        print(f"\n🎖️  OVERALL GRADE: {grade}")
        print(f"📝 Assessment: {grade_desc}")
        
        # Specific recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if avg_grammar_score < 3:
            print("   📚 Focus on basic grammar rules and sentence structure")
        
        if avg_writing_quality < 3:
            print("   ✨ Improve vocabulary variety and writing style")
        
        if avg_word_count < 100:
            print("   📏 Provide more detailed and comprehensive responses")
        
        if 'Excessive passive voice' in [issue for issue, _ in top_issues]:
            print("   🎯 Work on using more active voice constructions")
        
        if 'Repetitive sentence patterns' in [issue for issue, _ in top_issues]:
            print("   🔄 Vary sentence beginnings and structures")
        
        print(f"\n✨ Grammar test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

def main():
    """Run the grammar and writing quality test suite"""
    test_suite = GrammarTestSuite()
    
    try:
        # Check if server is running
        health_check = test_suite.make_request('/api/health/')
        if not health_check['success']:
            print("❌ Server not running! Please start the Django server first.")
            print("Run: python3 manage.py runserver")
            return
        
        print("✅ Server is running. Starting grammar tests...")
        test_suite.test_grammar_and_writing()
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
