#!/usr/bin/env python3
"""
Clang Chatbot Focused Capability Testing
Targeted tests for specific high-value features
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple

class FocusedChatbotTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.session_id = f"focused_test_{int(time.time())}"
        
    def send_message(self, message: str) -> Tuple[str, float, bool]:
        """Send a message to the chatbot and measure response time"""
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat/",
                json={
                    "message": message,
                    "session_id": self.session_id
                },
                timeout=15
            )
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', ''), response_time, True
            else:
                return f"Error: {response.status_code}", response_time, False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return f"Exception: {str(e)}", response_time, False
    
    def focused_test(self, category: str, test_name: str, message: str, 
                    evaluation_func=None) -> Dict:
        """Run a focused test with custom evaluation"""
        print(f"🎯 {category} - {test_name}")
        print(f"   Query: {message}")
        
        response, response_time, success = self.send_message(message)
        
        # Custom evaluation if provided
        evaluation_result = True
        evaluation_notes = ""
        if evaluation_func and success:
            evaluation_result, evaluation_notes = evaluation_func(response)
        
        result = {
            'category': category,
            'test_name': test_name,
            'input': message,
            'output': response,
            'response_time_ms': round(response_time, 2),
            'api_success': success,
            'evaluation_passed': evaluation_result,
            'evaluation_notes': evaluation_notes,
            'overall_success': success and evaluation_result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        # Display results
        status = "✅ PASS" if result['overall_success'] else "❌ FAIL"
        print(f"   Response: {response[:150]}{'...' if len(response) > 150 else ''}")
        print(f"   Time: {response_time:.0f}ms | {status}")
        if evaluation_notes:
            print(f"   Notes: {evaluation_notes}")
        print()
        
        return result
    
    def run_medical_tests(self):
        """Test advanced medical capabilities"""
        print("🏥 MEDICAL KNOWLEDGE FOCUSED TESTS")
        print("=" * 50)
        
        # Test 1: Complex medical interaction
        def evaluate_drug_interaction(response):
            keywords = ['warfarin', 'vitamin k', 'interaction', 'bleeding', 'inr']
            found_keywords = [kw for kw in keywords if kw.lower() in response.lower()]
            has_disclaimer = any(word in response.lower() for word in ['doctor', 'medical', 'professional', 'consult'])
            
            if len(found_keywords) >= 3 and has_disclaimer:
                return True, f"Found {len(found_keywords)} relevant keywords with proper disclaimer"
            else:
                return False, f"Only found {len(found_keywords)} keywords, disclaimer: {has_disclaimer}"
        
        self.focused_test(
            "Medical", "Drug Interaction Analysis",
            "What are the interactions between warfarin and vitamin K? How does this affect INR levels?",
            evaluate_drug_interaction
        )
        
        # Test 2: Emergency medical response
        def evaluate_emergency_response(response):
            emergency_words = ['911', 'emergency', 'immediate', 'hospital', 'call']
            urgency_indicators = ['immediately', 'urgent', 'serious', 'critical']
            
            has_emergency = any(word in response.lower() for word in emergency_words)
            has_urgency = any(word in response.lower() for word in urgency_indicators)
            
            if has_emergency and has_urgency:
                return True, "Proper emergency response with urgency indicators"
            else:
                return False, f"Emergency response: {has_emergency}, Urgency: {has_urgency}"
        
        self.focused_test(
            "Medical", "Emergency Response Protocol",
            "I'm experiencing severe chest pain, shortness of breath, and my left arm is numb",
            evaluate_emergency_response
        )
        
        # Test 3: Comprehensive medical condition
        def evaluate_medical_condition(response):
            diabetes_keywords = ['diabetes', 'blood sugar', 'glucose', 'insulin', 'type 2']
            management_aspects = ['diet', 'exercise', 'medication', 'monitoring']
            
            condition_coverage = sum(1 for kw in diabetes_keywords if kw.lower() in response.lower())
            management_coverage = sum(1 for aspect in management_aspects if aspect.lower() in response.lower())
            
            if condition_coverage >= 3 and management_coverage >= 2:
                return True, f"Comprehensive coverage: {condition_coverage} condition terms, {management_coverage} management aspects"
            else:
                return False, f"Limited coverage: {condition_coverage} condition terms, {management_coverage} management aspects"
        
        self.focused_test(
            "Medical", "Comprehensive Condition Analysis",
            "Explain Type 2 diabetes, its causes, symptoms, and management strategies",
            evaluate_medical_condition
        )
    
    def run_math_tests(self):
        """Test advanced mathematical capabilities"""
        print("🔢 MATHEMATICAL CAPABILITIES FOCUSED TESTS")
        print("=" * 50)
        
        # Test 1: Complex calculus
        def evaluate_calculus(response):
            # Looking for integration by parts or correct approach
            integration_terms = ['integration', 'parts', 'derivative', 'antiderivative']
            # The answer should be 1/2
            correct_answer = any(term in response for term in ['1/2', '0.5', 'half'])
            
            has_method = any(term.lower() in response.lower() for term in integration_terms)
            
            if correct_answer and has_method:
                return True, "Correct answer with proper integration method"
            elif correct_answer:
                return True, "Correct answer (method may be abbreviated)"
            else:
                return False, f"Method shown: {has_method}, Correct answer: {correct_answer}"
        
        self.focused_test(
            "Mathematics", "Advanced Calculus Integration",
            "Calculate the integral of sin(x)cos(x) from 0 to π/2. Show your work step by step.",
            evaluate_calculus
        )
        
        # Test 2: Complex algebra
        def evaluate_algebra(response):
            # Looking for quadratic formula or factoring
            methods = ['quadratic formula', 'factoring', 'completing square']
            solutions = ['x = 2', 'x = 3', '2 and 3']
            
            has_method = any(method.lower() in response.lower() for method in methods)
            has_solutions = any(sol in response for sol in solutions)
            
            if has_method and has_solutions:
                return True, "Proper method with correct solutions"
            elif has_solutions:
                return True, "Correct solutions (method may be implicit)"
            else:
                return False, f"Method shown: {has_method}, Solutions found: {has_solutions}"
        
        self.focused_test(
            "Mathematics", "Quadratic Equation Solving",
            "Solve x² - 5x + 6 = 0 using two different methods and verify your answers",
            evaluate_algebra
        )
        
        # Test 3: Applied mathematics
        def evaluate_applied_math(response):
            physics_terms = ['acceleration', 'velocity', 'derivative', 'rate']
            calculation_terms = ['9.8', '4.9', 'seconds', 'meters']
            
            has_physics = any(term.lower() in response.lower() for term in physics_terms)
            has_calculation = any(term in response for term in calculation_terms)
            
            if has_physics and has_calculation:
                return True, "Applied physics concepts with numerical calculation"
            else:
                return False, f"Physics concepts: {has_physics}, Calculations: {has_calculation}"
        
        self.focused_test(
            "Mathematics", "Applied Physics Problem",
            "A ball is dropped from a 45-meter tall building. How long does it take to hit the ground? Use g = 9.8 m/s²",
            evaluate_applied_math
        )
    
    def run_programming_tests(self):
        """Test advanced programming capabilities"""
        print("💻 PROGRAMMING EXPERTISE FOCUSED TESTS")
        print("=" * 50)
        
        # Test 1: Algorithm design
        def evaluate_algorithm_design(response):
            algorithm_concepts = ['binary search', 'divide', 'conquer', 'log', 'complexity']
            implementation_aspects = ['left', 'right', 'middle', 'compare', 'while']
            
            concept_coverage = sum(1 for concept in algorithm_concepts if concept.lower() in response.lower())
            implementation_details = sum(1 for aspect in implementation_aspects if aspect.lower() in response.lower())
            
            if concept_coverage >= 3 and implementation_details >= 3:
                return True, f"Strong algorithm explanation: {concept_coverage} concepts, {implementation_details} details"
            else:
                return False, f"Limited explanation: {concept_coverage} concepts, {implementation_details} details"
        
        self.focused_test(
            "Programming", "Algorithm Design & Analysis",
            "Implement a binary search algorithm in Python and explain its time complexity. Include error handling.",
            evaluate_algorithm_design
        )
        
        # Test 2: Code review and optimization
        def evaluate_code_review(response):
            review_aspects = ['efficiency', 'readability', 'optimization', 'best practices']
            specific_suggestions = ['list comprehension', 'enumerate', 'performance', 'pythonic']
            
            review_quality = sum(1 for aspect in review_aspects if aspect.lower() in response.lower())
            specific_advice = sum(1 for suggestion in specific_suggestions if suggestion.lower() in response.lower())
            
            if review_quality >= 2 and specific_advice >= 1:
                return True, f"Quality code review: {review_quality} aspects, {specific_advice} specific suggestions"
            else:
                return False, f"Basic review: {review_quality} aspects, {specific_advice} suggestions"
        
        self.focused_test(
            "Programming", "Code Review & Optimization",
            """Review this Python code and suggest improvements:
            
def find_max_in_list(numbers):
    max_val = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] > max_val:
            max_val = numbers[i]
    return max_val""",
            evaluate_code_review
        )
        
        # Test 3: System design
        def evaluate_system_design(response):
            design_concepts = ['api', 'endpoint', 'rest', 'database', 'crud']
            specific_endpoints = ['get', 'post', 'put', 'delete', 'books', 'users']
            
            concept_coverage = sum(1 for concept in design_concepts if concept.lower() in response.lower())
            endpoint_details = sum(1 for endpoint in specific_endpoints if endpoint.lower() in response.lower())
            
            if concept_coverage >= 4 and endpoint_details >= 4:
                return True, f"Comprehensive system design: {concept_coverage} concepts, {endpoint_details} endpoints"
            else:
                return False, f"Basic design: {concept_coverage} concepts, {endpoint_details} endpoints"
        
        self.focused_test(
            "Programming", "System Architecture Design",
            "Design a RESTful API for a library management system. Include all necessary endpoints, data models, and explain the database schema.",
            evaluate_system_design
        )
    
    def run_performance_tests(self):
        """Test performance and responsiveness"""
        print("⚡ PERFORMANCE & RESPONSIVENESS TESTS")
        print("=" * 50)
        
        # Test 1: Response speed for complex query
        start_time = time.time()
        self.focused_test(
            "Performance", "Complex Query Response Time",
            "Explain quantum computing, its applications in cryptography, and compare it to classical computing methods",
            lambda r: (True, f"Complex query processed successfully") if len(r) > 200 else (False, "Response too brief")
        )
        
        # Test 2: Rapid successive queries
        print("🚀 Rapid Query Test (5 quick messages)")
        rapid_test_start = time.time()
        
        messages = [
            "What is 25 * 4?",
            "What is Python?",
            "Define AI",
            "Medical term: tachycardia",
            "Sort algorithm efficiency"
        ]
        
        rapid_results = []
        for i, msg in enumerate(messages):
            print(f"   Query {i+1}: {msg}")
            response, response_time, success = self.send_message(msg)
            rapid_results.append((success, response_time))
            print(f"   Response {i+1}: {response_time:.0f}ms - {'✅' if success else '❌'}")
        
        total_rapid_time = (time.time() - rapid_test_start) * 1000
        successful_rapid = sum(1 for success, _ in rapid_results if success)
        avg_rapid_time = sum(rt for _, rt in rapid_results) / len(rapid_results)
        
        print(f"   Rapid Test Summary: {successful_rapid}/5 successful, Avg: {avg_rapid_time:.0f}ms, Total: {total_rapid_time:.0f}ms")
        print()
    
    def run_contextual_tests(self):
        """Test conversation context and memory"""
        print("🧠 CONTEXTUAL AWARENESS & MEMORY TESTS")
        print("=" * 50)
        
        # Multi-turn conversation test
        context_messages = [
            "I'm a software developer working on a medical app",
            "What security considerations should I keep in mind?",
            "How does HIPAA compliance affect my database design?",
            "What about the encryption methods you mentioned earlier?"
        ]
        
        for i, msg in enumerate(context_messages):
            def evaluate_context(response):
                if i == 0:  # Introduction
                    return True, "Context established"
                elif i == 1:  # Security question
                    security_terms = ['hipaa', 'encryption', 'authentication', 'security']
                    found = sum(1 for term in security_terms if term.lower() in response.lower())
                    return found >= 2, f"Found {found} security-related terms"
                elif i == 2:  # HIPAA question
                    hipaa_terms = ['database', 'encryption', 'access control', 'audit']
                    found = sum(1 for term in hipaa_terms if term.lower() in response.lower())
                    return found >= 2, f"Found {found} HIPAA-related terms"
                elif i == 3:  # Reference to earlier
                    context_indicators = ['mentioned', 'earlier', 'previously', 'discussed']
                    has_context = any(indicator in response.lower() for indicator in context_indicators)
                    return has_context, f"Context reference: {has_context}"
                
                return True, "Standard evaluation"
            
            self.focused_test(
                "Context", f"Multi-turn Conversation Step {i+1}",
                msg,
                evaluate_context
            )
    
    def generate_focused_report(self):
        """Generate focused test report"""
        print("📊 FOCUSED TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['overall_success'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        response_times = [r['response_time_ms'] for r in self.test_results]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        print(f"🎯 Total Focused Tests: {total_tests}")
        print(f"✅ Successful Tests: {successful_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Average Response Time: {avg_response_time:.0f}ms")
        print()
        
        # Category performance
        categories = {}
        for result in self.test_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'times': []}
            categories[cat]['total'] += 1
            categories[cat]['times'].append(result['response_time_ms'])
            if result['overall_success']:
                categories[cat]['success'] += 1
        
        print("📋 CATEGORY PERFORMANCE:")
        for category, stats in categories.items():
            rate = (stats['success'] / stats['total']) * 100
            avg_time = sum(stats['times']) / len(stats['times'])
            print(f"   {category}: {stats['success']}/{stats['total']} ({rate:.0f}%) - Avg: {avg_time:.0f}ms")
        
        print()
        
        # Detailed insights
        print("🔍 DETAILED INSIGHTS:")
        
        # Best performing category
        best_category = max(categories.items(), key=lambda x: x[1]['success'] / x[1]['total'])
        print(f"   🏆 Best Performance: {best_category[0]} ({(best_category[1]['success']/best_category[1]['total']*100):.0f}%)")
        
        # Fastest responses
        fastest_test = min(self.test_results, key=lambda x: x['response_time_ms'])
        print(f"   ⚡ Fastest Response: {fastest_test['test_name']} ({fastest_test['response_time_ms']:.0f}ms)")
        
        # Most comprehensive response
        longest_response = max(self.test_results, key=lambda x: len(x['output']))
        print(f"   📝 Most Detailed: {longest_response['test_name']} ({len(longest_response['output'])} chars)")
        
        print()
        
        # Save results
        filename = f"focused_test_results_{self.session_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'test_type': 'focused_capabilities',
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'success_rate': success_rate,
                    'avg_response_time': avg_response_time
                },
                'category_performance': categories,
                'results': self.test_results
            }, f, indent=2)
        
        print(f"💾 Detailed results saved to: {filename}")
        print("=" * 60)

def main():
    """Run focused capability tests"""
    print("🎯 CLANG CHATBOT FOCUSED CAPABILITY TESTING")
    print("Testing the most advanced and impressive features")
    print("=" * 60)
    print()
    
    # Test connection
    base_url = "http://127.0.0.1:8000"
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            print(f"❌ Cannot connect to {base_url}")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    print("✅ Connection successful!")
    print()
    
    # Run focused tests
    tester = FocusedChatbotTester(base_url)
    
    # Run all focused test categories
    tester.run_medical_tests()
    tester.run_math_tests()
    tester.run_programming_tests()
    tester.run_performance_tests()
    tester.run_contextual_tests()
    
    # Generate comprehensive report
    tester.generate_focused_report()
    
    print("🎉 FOCUSED TESTING COMPLETE!")
    print("Check the generated JSON file for detailed results.")

if __name__ == "__main__":
    main()
