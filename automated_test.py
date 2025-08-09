#!/usr/bin/env python3
"""
Clang Chatbot Automated Testing Suite
Comprehensive testing of all chatbot capabilities
"""

import requests
import time
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class ClangChatbotTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.session_id = f"test_session_{int(time.time())}"
        
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
                timeout=30
            )
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', ''), response_time, True
            else:
                return f"Error: {response.status_code}", response_time, False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return f"Exception: {str(e)}", response_time, False
    
    def run_test(self, category: str, test_name: str, message: str, 
                 expected_keywords: List[str] = None, max_response_time: float = 5000) -> Dict:
        """Run a single test and return results"""
        print(f"🧪 Testing {category} - {test_name}")
        print(f"   Input: {message}")
        
        response, response_time, success = self.send_message(message)
        
        # Check if response contains expected keywords
        keyword_match = True
        if expected_keywords and success:
            response_lower = response.lower()
            keyword_match = any(keyword.lower() in response_lower for keyword in expected_keywords)
        
        # Evaluate performance
        performance_good = response_time <= max_response_time
        
        # Overall success
        overall_success = success and keyword_match and performance_good
        
        result = {
            'category': category,
            'test_name': test_name,
            'input': message,
            'output': response[:200] + "..." if len(response) > 200 else response,
            'response_time_ms': round(response_time, 2),
            'success': overall_success,
            'api_success': success,
            'keyword_match': keyword_match,
            'performance_good': performance_good,
            'expected_keywords': expected_keywords or [],
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        # Print results
        status = "✅ PASS" if overall_success else "❌ FAIL"
        print(f"   Response: {response[:100]}...")
        print(f"   Time: {response_time:.0f}ms | {status}")
        print()
        
        return result
    
    def run_performance_stress_test(self) -> Dict:
        """Test performance with rapid messages"""
        print("🚀 Running Performance Stress Test")
        
        messages = [
            f"Rapid test message {i+1}" for i in range(10)
        ]
        
        start_time = time.time()
        response_times = []
        successful_responses = 0
        
        for i, message in enumerate(messages):
            print(f"   Sending message {i+1}/10...")
            response, response_time, success = self.send_message(message)
            response_times.append(response_time)
            if success:
                successful_responses += 1
            time.sleep(0.1)  # Small delay between messages
        
        total_time = (time.time() - start_time) * 1000
        avg_response_time = sum(response_times) / len(response_times)
        
        result = {
            'category': 'Performance',
            'test_name': 'Stress Test - 10 Rapid Messages',
            'input': f"{len(messages)} rapid messages",
            'output': f"Processed {successful_responses}/{len(messages)} messages successfully",
            'response_time_ms': round(avg_response_time, 2),
            'total_time_ms': round(total_time, 2),
            'success': successful_responses >= 8,  # Allow 2 failures
            'successful_responses': successful_responses,
            'total_messages': len(messages),
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        print(f"   Completed: {successful_responses}/{len(messages)} successful")
        print(f"   Avg Response Time: {avg_response_time:.0f}ms")
        print(f"   Total Time: {total_time:.0f}ms")
        print()
        
        return result
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🎯 Starting Comprehensive Clang Chatbot Test Suite")
        print(f"   Session ID: {self.session_id}")
        print(f"   Base URL: {self.base_url}")
        print("=" * 60)
        print()
        
        # Basic Conversation Tests
        print("📝 BASIC CONVERSATION TESTS")
        print("-" * 30)
        
        self.run_test(
            "Basic", "Greeting", 
            "Hello, what's your name?",
            ["clang", "ai", "assistant", "krishna"],
            3000
        )
        
        self.run_test(
            "Basic", "Capabilities", 
            "What can you help me with?",
            ["medical", "math", "programming", "help"],
            3000
        )
        
        self.run_test(
            "Basic", "Memory Test", 
            "Remember that my name is Krishna",
            ["remember", "krishna", "noted"],
            3000
        )
        
        # Medical Knowledge Tests
        print("🏥 MEDICAL KNOWLEDGE TESTS")
        print("-" * 30)
        
        self.run_test(
            "Medical", "Symptom Analysis", 
            "I have a headache and fever, what could it be?",
            ["fever", "headache", "medical", "doctor", "professional"],
            4000
        )
        
        self.run_test(
            "Medical", "Medication Info", 
            "What is the dosage for ibuprofen?",
            ["ibuprofen", "dosage", "mg", "medical", "professional"],
            4000
        )
        
        self.run_test(
            "Medical", "Emergency Response", 
            "I'm having chest pain",
            ["emergency", "911", "immediate", "medical", "attention"],
            3000
        )
        
        # Mathematical Tests
        print("🔢 MATHEMATICAL TESTS")
        print("-" * 30)
        
        self.run_test(
            "Math", "Basic Arithmetic", 
            "Calculate 15 * 23 + 45",
            ["390", "345", "answer"],
            3000
        )
        
        self.run_test(
            "Math", "Quadratic Equation", 
            "Solve: x^2 + 5x + 6 = 0",
            ["x = -2", "x = -3", "quadratic"],
            4000
        )
        
        self.run_test(
            "Math", "Calculus", 
            "What's the derivative of x^3 + 2x^2?",
            ["3x^2", "4x", "derivative"],
            4000
        )
        
        # Programming Tests
        print("💻 PROGRAMMING TESTS")
        print("-" * 30)
        
        self.run_test(
            "Programming", "Algorithm Explanation", 
            "Explain bubble sort algorithm",
            ["bubble", "sort", "algorithm", "compare", "swap"],
            4000
        )
        
        self.run_test(
            "Programming", "Code Debugging", 
            "Debug this Python code: for i in range(10) print(i)",
            ["colon", ":", "syntax", "error"],
            3000
        )
        
        # Performance Tests
        print("⚡ PERFORMANCE TESTS")
        print("-" * 30)
        
        self.run_performance_stress_test()
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        response_times = [r['response_time_ms'] for r in self.test_results if 'response_time_ms' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Average Response Time: {avg_response_time:.0f}ms")
        print()
        
        # Category breakdown
        categories = {}
        for result in self.test_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0}
            categories[cat]['total'] += 1
            if result['success']:
                categories[cat]['success'] += 1
        
        print("📈 CATEGORY BREAKDOWN:")
        for category, stats in categories.items():
            rate = (stats['success'] / stats['total']) * 100
            print(f"   {category}: {stats['success']}/{stats['total']} ({rate:.0f}%)")
        
        print()
        
        # Failed tests
        failed_tests = [r for r in self.test_results if not r['success']]
        if failed_tests:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   - {test['category']} - {test['test_name']}")
                if not test.get('api_success', True):
                    print(f"     Issue: API Error")
                elif not test.get('keyword_match', True):
                    print(f"     Issue: Response doesn't contain expected keywords")
                elif not test.get('performance_good', True):
                    print(f"     Issue: Response time too slow ({test['response_time_ms']:.0f}ms)")
        else:
            print("🎉 ALL TESTS PASSED!")
        
        print()
        
        # Save detailed results
        self.save_results()
        
        print(f"💾 Detailed results saved to: test_results_{self.session_id}.json")
        print("=" * 60)
    
    def save_results(self):
        """Save test results to JSON file"""
        filename = f"test_results_{self.session_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'base_url': self.base_url,
                'summary': {
                    'total_tests': len(self.test_results),
                    'successful_tests': sum(1 for r in self.test_results if r['success']),
                    'success_rate': (sum(1 for r in self.test_results if r['success']) / len(self.test_results)) * 100,
                    'avg_response_time': sum(r['response_time_ms'] for r in self.test_results if 'response_time_ms' in r) / len(self.test_results)
                },
                'results': self.test_results
            }, f, indent=2)

def main():
    """Main function to run tests"""
    # Check if custom URL provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    print(f"🤖 Clang Chatbot Testing Suite")
    print(f"   Target: {base_url}")
    print()
    
    # Test connection first
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            print(f"❌ Cannot connect to {base_url}")
            print("   Make sure the Django server is running!")
            return
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("   Make sure the Django server is running!")
        return
    
    print("✅ Connection successful!")
    print()
    
    # Run tests
    tester = ClangChatbotTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
