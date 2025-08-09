#!/usr/bin/env python3
"""
Optimized Clang Chatbot Testing Suite
Fast, reliable tests for the optimized backend
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Tuple

class OptimizedChatbotTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.session_id = f"optimized_test_{int(time.time())}"
        
    def send_message(self, message: str, timeout: int = 8) -> Tuple[str, float, bool]:
        """Send a message with optimized timeout"""
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat/",
                json={
                    "message": message,
                    "session_id": self.session_id
                },
                timeout=timeout
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
    
    def quick_test(self, category: str, test_name: str, message: str, 
                   success_keywords: List[str] = None, max_time: float = 5000) -> Dict:
        """Run optimized test with quick evaluation"""
        print(f"🚀 {category} - {test_name}")
        print(f"   Query: {message}")
        
        response, response_time, api_success = self.send_message(message)
        
        # Quick keyword evaluation
        keyword_success = True
        if success_keywords and api_success:
            response_lower = response.lower()
            found_keywords = [kw for kw in success_keywords if kw.lower() in response_lower]
            keyword_success = len(found_keywords) >= len(success_keywords) // 2  # At least half
        
        # Performance check
        performance_good = response_time <= max_time
        
        # Overall success
        overall_success = api_success and keyword_success and performance_good and len(response) > 50
        
        result = {
            'category': category,
            'test_name': test_name,
            'input': message,
            'output': response[:300] + "..." if len(response) > 300 else response,
            'response_time_ms': round(response_time, 2),
            'api_success': api_success,
            'keyword_success': keyword_success,
            'performance_good': performance_good,
            'overall_success': overall_success,
            'found_keywords': found_keywords if success_keywords else [],
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        # Display results
        status = "✅ PASS" if overall_success else "❌ FAIL"
        print(f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        print(f"   Time: {response_time:.0f}ms | {status}")
        
        if not overall_success:
            issues = []
            if not api_success: issues.append("API Error")
            if not keyword_success: issues.append("Missing Keywords") 
            if not performance_good: issues.append("Slow Response")
            if len(response) <= 50: issues.append("Response Too Short")
            print(f"   Issues: {', '.join(issues)}")
        
        print()
        return result
    
    def run_core_tests(self):
        """Run essential tests that should pass"""
        print("🎯 CORE CAPABILITY TESTS (Optimized)")
        print("=" * 50)
        
        # Basic functionality
        self.quick_test(
            "Basic", "Greeting",
            "Hello, what's your name?",
            ["clang", "ai", "assistant", "krishna"],
            3000
        )
        
        self.quick_test(
            "Basic", "Capabilities",
            "What can you help me with?",
            ["medical", "math", "programming", "help"],
            3000
        )
        
        # Simple math (should be very fast)
        self.quick_test(
            "Math", "Basic Arithmetic",
            "Calculate 15 * 23 + 45",
            ["390", "345", "calculate"],
            2000
        )
        
        self.quick_test(
            "Math", "Simple Equation",
            "Solve 2x + 5 = 17",
            ["x = 6", "6", "solve"],
            3000
        )
        
        # Medical with safety
        self.quick_test(
            "Medical", "General Symptom",
            "I have a mild headache, what could help?",
            ["rest", "water", "medical", "professional"],
            4000
        )
        
        self.quick_test(
            "Medical", "Emergency Response",
            "I'm having chest pain",
            ["911", "emergency", "immediate", "medical"],
            3000
        )
        
        # Programming basics
        self.quick_test(
            "Programming", "Simple Debug",
            "Debug: for i in range(5) print(i)",
            ["colon", ":", "syntax"],
            3000
        )
        
        self.quick_test(
            "Programming", "Basic Algorithm",
            "Explain bubble sort briefly",
            ["sort", "compare", "swap", "algorithm"],
            4000
        )
        
        # Context and memory
        self.quick_test(
            "Context", "Memory Setting",
            "Remember my name is Krishna",
            ["remember", "krishna", "noted"],
            2000
        )
        
        self.quick_test(
            "Context", "Memory Recall",
            "What's my name?",
            ["krishna", "name"],
            2000
        )
    
    def run_advanced_tests(self):
        """Run more complex tests"""
        print("🔬 ADVANCED CAPABILITY TESTS")
        print("=" * 50)
        
        # Complex medical
        self.quick_test(
            "Medical", "Drug Interaction",
            "Warfarin and vitamin K interaction?",
            ["warfarin", "vitamin k", "bleeding", "inr"],
            5000
        )
        
        # Advanced math
        self.quick_test(
            "Math", "Calculus",
            "Derivative of x^3 + 2x^2",
            ["3x^2", "4x", "derivative"],
            4000
        )
        
        # Complex programming
        self.quick_test(
            "Programming", "Algorithm Design",
            "Binary search algorithm in Python",
            ["binary", "search", "log", "divide"],
            5000
        )
    
    def run_performance_test(self):
        """Test rapid message handling"""
        print("⚡ PERFORMANCE STRESS TEST")
        print("=" * 50)
        
        messages = [
            "2 + 2",
            "Hello",
            "Python help",
            "Medical advice",
            "Quick math"
        ]
        
        start_time = time.time()
        results = []
        
        for i, msg in enumerate(messages):
            print(f"   Rapid message {i+1}: {msg}")
            response, response_time, success = self.send_message(msg, timeout=5)
            results.append((success, response_time))
            print(f"   → {response_time:.0f}ms {'✅' if success else '❌'}")
        
        total_time = (time.time() - start_time) * 1000
        successful = sum(1 for success, _ in results if success)
        avg_time = sum(rt for _, rt in results) / len(results)
        
        overall_success = successful >= 4 and avg_time <= 3000  # Allow 1 failure
        
        result = {
            'category': 'Performance',
            'test_name': 'Rapid Message Handling',
            'input': f'{len(messages)} rapid messages',
            'output': f'{successful}/{len(messages)} successful',
            'response_time_ms': round(avg_time, 2),
            'total_time_ms': round(total_time, 2),
            'overall_success': overall_success,
            'successful_count': successful,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        status = "✅ PASS" if overall_success else "❌ FAIL"
        print(f"   Summary: {successful}/5 successful, Avg: {avg_time:.0f}ms | {status}")
        print()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("📊 OPTIMIZED TEST RESULTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['overall_success'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        response_times = [r['response_time_ms'] for r in self.test_results if 'response_time_ms' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        print(f"🎯 Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Avg Response Time: {avg_response_time:.0f}ms")
        print()
        
        # Category breakdown
        categories = {}
        for result in self.test_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'success': 0, 'times': []}
            categories[cat]['total'] += 1
            if 'response_time_ms' in result:
                categories[cat]['times'].append(result['response_time_ms'])
            if result['overall_success']:
                categories[cat]['success'] += 1
        
        print("📋 CATEGORY PERFORMANCE:")
        for category, stats in categories.items():
            rate = (stats['success'] / stats['total']) * 100
            avg_time = sum(stats['times']) / len(stats['times']) if stats['times'] else 0
            print(f"   {category}: {stats['success']}/{stats['total']} ({rate:.0f}%) - {avg_time:.0f}ms")
        
        print()
        
        # Success analysis
        if success_rate >= 80:
            print("🎉 EXCELLENT PERFORMANCE!")
            print("   The chatbot is working optimally with fast, accurate responses.")
        elif success_rate >= 60:
            print("✅ GOOD PERFORMANCE")
            print("   Most features working well, minor optimizations possible.")
        else:
            print("⚠️ NEEDS OPTIMIZATION")
            print("   Several areas need improvement for better performance.")
        
        # Failed tests
        failed_tests = [r for r in self.test_results if not r['overall_success']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests[:5]:  # Show first 5 failures
                print(f"   - {test['category']} - {test['test_name']}")
        
        print()
        
        # Save results
        filename = f"optimized_test_results_{self.session_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'test_type': 'optimized_performance',
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'successful_tests': successful_tests,
                    'success_rate': success_rate,
                    'avg_response_time': avg_response_time
                },
                'categories': categories,
                'results': self.test_results
            }, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
        print("=" * 60)

def main():
    """Run optimized tests"""
    print("🚀 CLANG CHATBOT OPTIMIZED TESTING")
    print("Testing core capabilities with performance focus")
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
        print("   Make sure Django server is running!")
        return
    
    print("✅ Connection successful!")
    print()
    
    # Run optimized tests
    tester = OptimizedChatbotTester(base_url)
    
    # Core tests (essential functionality)
    tester.run_core_tests()
    
    # Advanced tests (complex features)
    tester.run_advanced_tests()
    
    # Performance test
    tester.run_performance_test()
    
    # Generate report
    tester.generate_report()
    
    print("🎉 OPTIMIZED TESTING COMPLETE!")

if __name__ == "__main__":
    main()
