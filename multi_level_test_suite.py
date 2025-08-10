#!/usr/bin/env python3
"""
Multi-Level Comprehensive Test Suite
Tests all services with Easy, Medium, and Hard complexity levels
Includes essay writing and grammar checking across all services
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class MultiLevelTestSuite:
    def __init__(self):
        self.results = {
            'easy': [],
            'medium': [],
            'hard': []
        }
        self.session_id = f"test_session_{int(time.time())}"
    
    def make_request(self, endpoint, data=None, method='GET'):
        """Make HTTP request with error handling"""
        try:
            if method == 'POST':
                response = requests.post(f"{BASE_URL}{endpoint}", 
                                       json=data, 
                                       timeout=30)
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
    
    def test_level(self, level, test_cases):
        """Run tests for a specific difficulty level"""
        print(f"\n{'='*60}")
        print(f"🎯 TESTING {level.upper()} LEVEL SERVICES")
        print(f"{'='*60}")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {level.upper()}-{i}: {test_case['name']}")
            print(f"🔍 Category: {test_case['category']}")
            print(f"📝 Prompt: {test_case['prompt'][:80]}...")
            
            # Make the API call
            response = self.make_request('/api/chat/', {
                'message': test_case['prompt'],
                'session_id': self.session_id
            }, 'POST')
            
            # Analyze response
            result = self.analyze_response(test_case, response, level)
            self.results[level].append(result)
            
            # Print results
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"🏆 Result: {status}")
            print(f"⏱️  Response Time: {result['response_time']:.2f}s")
            print(f"📊 Quality Score: {result['quality_score']}/10")
            
            if result['notes']:
                print(f"📝 Notes: {result['notes']}")
            
            # Brief delay between tests
            time.sleep(1)
    
    def analyze_response(self, test_case, response, level):
        """Analyze response quality and correctness"""
        result = {
            'test_name': test_case['name'],
            'category': test_case['category'],
            'level': level,
            'response_time': response['response_time'],
            'status_code': response['status_code'],
            'passed': False,
            'quality_score': 0,
            'notes': []
        }
        
        if not response['success']:
            result['notes'].append(f"Request failed: {response['content']}")
            return result
        
        try:
            content = response['content']
            if isinstance(content, dict):
                response_text = content.get('response', str(content))
            else:
                response_text = str(content)
            
            # Quality scoring based on response characteristics
            score = 0
            
            # Length check (appropriate for complexity level)
            expected_lengths = {'easy': 50, 'medium': 150, 'hard': 300}
            if len(response_text) >= expected_lengths[level]:
                score += 2
                result['notes'].append("✓ Appropriate response length")
            else:
                result['notes'].append(f"⚠ Short response ({len(response_text)} chars)")
            
            # Content relevance check
            keywords = test_case.get('keywords', [])
            found_keywords = sum(1 for keyword in keywords if keyword.lower() in response_text.lower())
            if found_keywords >= len(keywords) * 0.5:  # At least 50% of keywords
                score += 2
                result['notes'].append(f"✓ Relevant content ({found_keywords}/{len(keywords)} keywords)")
            else:
                result['notes'].append(f"⚠ Low relevance ({found_keywords}/{len(keywords)} keywords)")
            
            # Structure check (for essays and complex responses)
            if test_case['category'] in ['essay', 'creative', 'analysis']:
                if any(marker in response_text for marker in ['\n\n', '**', '#', '1.', '2.']):
                    score += 2
                    result['notes'].append("✓ Well-structured response")
                else:
                    result['notes'].append("⚠ Lacks clear structure")
            else:
                score += 1  # Give some points for non-essay formats
            
            # Technical accuracy (for specific domains)
            if test_case['category'] in ['medical', 'programming', 'math']:
                if any(term in response_text.lower() for term in ['disclaimer', 'note:', 'important:', 'def ', 'function', '=']):
                    score += 2
                    result['notes'].append("✓ Includes appropriate technical elements")
                else:
                    result['notes'].append("⚠ Missing technical accuracy indicators")
            else:
                score += 1
            
            # Response completeness
            if len(response_text) > 100 and not response_text.endswith('...'):
                score += 2
                result['notes'].append("✓ Complete response")
            else:
                result['notes'].append("⚠ Response may be incomplete")
            
            result['quality_score'] = min(score, 10)  # Cap at 10
            result['passed'] = score >= 6  # Pass threshold
            
        except Exception as e:
            result['notes'].append(f"Analysis error: {str(e)}")
        
        return result
    
    def run_comprehensive_tests(self):
        """Run all test levels"""
        print("🚀 STARTING MULTI-LEVEL COMPREHENSIVE TEST SUITE")
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Target: {BASE_URL}")
        
        # Easy Level Tests
        easy_tests = [
            {
                'name': 'Simple Greeting',
                'category': 'basic',
                'prompt': 'Hello, how are you?',
                'keywords': ['hello', 'help', 'assist']
            },
            {
                'name': 'Basic Math',
                'category': 'math',
                'prompt': '15 + 25 = ?',
                'keywords': ['40', 'answer', 'result']
            },
            {
                'name': 'Simple Essay',
                'category': 'essay',
                'prompt': 'Write a short paragraph about the importance of education.',
                'keywords': ['education', 'important', 'learning', 'knowledge']
            },
            {
                'name': 'Basic Medical Query',
                'category': 'medical',
                'prompt': 'What is fever?',
                'keywords': ['temperature', 'body', 'disclaimer', 'medical']
            },
            {
                'name': 'Simple Creative Writing',
                'category': 'creative',
                'prompt': 'Write a short story about a friendly cat.',
                'keywords': ['cat', 'story', 'friendly']
            }
        ]
        
        # Medium Level Tests
        medium_tests = [
            {
                'name': 'Complex Conversation',
                'category': 'conversational',
                'prompt': 'Explain the relationship between artificial intelligence and machine learning, and how they impact modern technology.',
                'keywords': ['artificial intelligence', 'machine learning', 'technology', 'data', 'algorithms']
            },
            {
                'name': 'Mathematical Problem',
                'category': 'math',
                'prompt': 'Solve the quadratic equation: x² - 5x + 6 = 0. Show your work.',
                'keywords': ['quadratic', 'equation', 'solution', 'x =']
            },
            {
                'name': 'Structured Essay',
                'category': 'essay',
                'prompt': 'Write a 200-word essay about climate change, including causes, effects, and solutions.',
                'keywords': ['climate change', 'causes', 'effects', 'solutions', 'environment']
            },
            {
                'name': 'Medical Analysis',
                'category': 'medical',
                'prompt': 'Describe the symptoms and treatment options for diabetes. Include lifestyle recommendations.',
                'keywords': ['diabetes', 'symptoms', 'treatment', 'lifestyle', 'disclaimer']
            },
            {
                'name': 'Programming Task',
                'category': 'programming',
                'prompt': 'Write a Python function to find the factorial of a number using recursion.',
                'keywords': ['python', 'function', 'factorial', 'recursion', 'def']
            }
        ]
        
        # Hard Level Tests
        hard_tests = [
            {
                'name': 'Complex Analysis',
                'category': 'analysis',
                'prompt': 'Analyze the socioeconomic implications of universal basic income implementation, considering economic theory, political feasibility, and social justice perspectives. Provide a balanced argument with at least 3 viewpoints.',
                'keywords': ['universal basic income', 'socioeconomic', 'economic theory', 'political', 'social justice']
            },
            {
                'name': 'Advanced Mathematics',
                'category': 'math',
                'prompt': 'Explain the concept of limits in calculus and solve: lim(x→0) (sin(x)/x). Include the mathematical reasoning.',
                'keywords': ['limits', 'calculus', 'sin(x)/x', 'mathematical', 'reasoning']
            },
            {
                'name': 'Academic Essay',
                'category': 'essay',
                'prompt': 'Write a comprehensive 400-word academic essay on "The Impact of Quantum Computing on Cryptography" with proper introduction, body paragraphs, and conclusion. Include technical details and future implications.',
                'keywords': ['quantum computing', 'cryptography', 'introduction', 'conclusion', 'technical']
            },
            {
                'name': 'Medical Case Study',
                'category': 'medical',
                'prompt': 'Analyze a hypothetical case: A 45-year-old patient presents with chest pain, shortness of breath, and elevated blood pressure. Discuss differential diagnosis, recommended tests, and potential treatment approaches.',
                'keywords': ['chest pain', 'shortness of breath', 'blood pressure', 'differential diagnosis', 'treatment']
            },
            {
                'name': 'Advanced Programming',
                'category': 'programming',
                'prompt': 'Design and implement a thread-safe singleton pattern in Python with lazy initialization and explain the thread safety mechanisms used.',
                'keywords': ['thread-safe', 'singleton', 'lazy initialization', 'python', 'thread safety']
            },
            {
                'name': 'Creative Narrative',
                'category': 'creative',
                'prompt': 'Write a complex short story about time travel that explores the philosophical implications of free will versus determinism, incorporating multiple timeline perspectives.',
                'keywords': ['time travel', 'philosophical', 'free will', 'determinism', 'timeline']
            }
        ]
        
        # Run tests for each level
        self.test_level('easy', easy_tests)
        self.test_level('medium', medium_tests)
        self.test_level('hard', hard_tests)
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE TEST REPORT")
        print(f"{'='*80}")
        
        total_tests = 0
        total_passed = 0
        avg_response_time = 0
        avg_quality_score = 0
        
        for level in ['easy', 'medium', 'hard']:
            level_results = self.results[level]
            level_passed = sum(1 for r in level_results if r['passed'])
            level_total = len(level_results)
            level_avg_time = sum(r['response_time'] for r in level_results) / level_total if level_total > 0 else 0
            level_avg_score = sum(r['quality_score'] for r in level_results) / level_total if level_total > 0 else 0
            
            print(f"\n🎯 {level.upper()} LEVEL RESULTS:")
            print(f"   ✅ Passed: {level_passed}/{level_total} ({level_passed/level_total*100:.1f}%)")
            print(f"   ⏱️  Avg Response Time: {level_avg_time:.2f}s")
            print(f"   📊 Avg Quality Score: {level_avg_score:.1f}/10")
            
            # Category breakdown
            categories = {}
            for result in level_results:
                cat = result['category']
                if cat not in categories:
                    categories[cat] = {'passed': 0, 'total': 0, 'scores': []}
                categories[cat]['total'] += 1
                if result['passed']:
                    categories[cat]['passed'] += 1
                categories[cat]['scores'].append(result['quality_score'])
            
            print(f"   📋 Category Breakdown:")
            for cat, stats in categories.items():
                avg_cat_score = sum(stats['scores']) / len(stats['scores'])
                print(f"      {cat.title()}: {stats['passed']}/{stats['total']} (Score: {avg_cat_score:.1f})")
            
            total_tests += level_total
            total_passed += level_passed
            avg_response_time += level_avg_time
            avg_quality_score += level_avg_score
        
        # Overall statistics
        overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        avg_response_time /= 3  # 3 levels
        avg_quality_score /= 3
        
        print(f"\n🏆 OVERALL PERFORMANCE:")
        print(f"   📈 Total Pass Rate: {total_passed}/{total_tests} ({overall_pass_rate:.1f}%)")
        print(f"   ⚡ Average Response Time: {avg_response_time:.2f}s")
        print(f"   🌟 Average Quality Score: {avg_quality_score:.1f}/10")
        
        # Performance grading
        if overall_pass_rate >= 90:
            grade = "🥇 EXCELLENT"
        elif overall_pass_rate >= 75:
            grade = "🥈 GOOD"
        elif overall_pass_rate >= 60:
            grade = "🥉 SATISFACTORY"
        else:
            grade = "❌ NEEDS IMPROVEMENT"
        
        print(f"   🎖️  Overall Grade: {grade}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_response_time > 10:
            print("   ⚠️ Consider optimizing response times")
        if avg_quality_score < 7:
            print("   ⚠️ Focus on improving response quality and relevance")
        
        failed_categories = set()
        for level_results in self.results.values():
            for result in level_results:
                if not result['passed']:
                    failed_categories.add(result['category'])
        
        if failed_categories:
            print(f"   🔧 Categories needing attention: {', '.join(failed_categories)}")
        
        print(f"\n✨ Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

def main():
    """Run the comprehensive test suite"""
    test_suite = MultiLevelTestSuite()
    
    try:
        # Check if server is running
        health_check = test_suite.make_request('/api/health/')
        if not health_check['success']:
            print("❌ Server not running! Please start the Django server first.")
            print("Run: python3 manage.py runserver")
            return
        
        print("✅ Server is running. Starting tests...")
        test_suite.run_comprehensive_tests()
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
