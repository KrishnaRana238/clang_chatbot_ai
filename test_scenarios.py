#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Clang Chatbot
Tests multiple scenarios: Greetings, Identity, Medical, Essays, and AI responses
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000/api/chat/"

class ChatbotTester:
    def __init__(self):
        self.test_count = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def test_request(self, message, test_name, expected_keywords=None):
        """Send a test request and validate response"""
        self.test_count += 1
        print(f"\n{'='*60}")
        print(f"🧪 TEST {self.test_count}: {test_name}")
        print(f"📤 INPUT: {message}")
        print(f"{'='*60}")
        
        try:
            response = requests.post(
                BASE_URL,
                headers={"Content-Type": "application/json"},
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('response', 'No response')
                
                print(f"✅ STATUS: Success (200)")
                print(f"📥 OUTPUT: {bot_response}")
                
                # Check for expected keywords if provided
                if expected_keywords:
                    found_keywords = []
                    missing_keywords = []
                    
                    for keyword in expected_keywords:
                        if keyword.lower() in bot_response.lower():
                            found_keywords.append(keyword)
                        else:
                            missing_keywords.append(keyword)
                    
                    print(f"🔍 KEYWORD CHECK:")
                    if found_keywords:
                        print(f"   ✅ Found: {', '.join(found_keywords)}")
                    if missing_keywords:
                        print(f"   ❌ Missing: {', '.join(missing_keywords)}")
                    
                    if missing_keywords:
                        print(f"⚠️  RESULT: PARTIAL - Some expected keywords missing")
                        self.failed_tests += 1
                    else:
                        print(f"🎉 RESULT: PASSED - All keywords found")
                        self.passed_tests += 1
                else:
                    print(f"🎉 RESULT: PASSED - Response received")
                    self.passed_tests += 1
                    
            else:
                print(f"❌ STATUS: Failed ({response.status_code})")
                print(f"📥 ERROR: {response.text}")
                print(f"💥 RESULT: FAILED")
                self.failed_tests += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR: Server not responding")
            print(f"💥 RESULT: FAILED")
            self.failed_tests += 1
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print(f"💥 RESULT: FAILED")
            self.failed_tests += 1
            
        time.sleep(2)  # Brief pause between tests

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 STARTING COMPREHENSIVE CHATBOT TEST SUITE")
        print("=" * 80)
        
        # 1. Greeting Tests
        print("\n🤝 GREETING TESTS")
        self.test_request("hey", "Basic Greeting", ["help", "how"])
        self.test_request("hi", "Alternative Greeting")
        self.test_request("hello", "Formal Greeting")
        
        # 2. Identity Tests
        print("\n🤖 IDENTITY TESTS")
        self.test_request("what's your name", "Name Query", ["Clang", "Krishna"])
        self.test_request("who are you", "Identity Query", ["Clang"])
        self.test_request("tell me about yourself", "Self Description")
        
        # 3. Medical Tests
        print("\n🏥 MEDICAL KNOWLEDGE TESTS")
        self.test_request("What are the symptoms of asthma?", "Asthma Symptoms", ["breathing", "wheezing"])
        self.test_request("Tell me about diabetes", "Diabetes Info", ["blood sugar", "glucose"])
        self.test_request("What medications help with anxiety?", "Anxiety Medication", ["sertraline", "medication"])
        self.test_request("Drug interactions with metformin", "Drug Interactions", ["metformin", "interaction"])
        self.test_request("chest pain emergency", "Emergency Detection", ["emergency", "medical"])
        
        # 4. Essay Writing Tests
        print("\n✍️ ESSAY WRITING TESTS")
        self.test_request("write an essay about artificial intelligence", "AI Essay", ["artificial intelligence", "technology"])
        self.test_request("write an essay on environmental conservation", "Environment Essay", ["environment", "conservation"])
        self.test_request("write an essay about education", "Education Essay", ["education", "learning"])
        
        # 5. General AI Tests
        print("\n🧠 GENERAL AI TESTS")
        self.test_request("What is photosynthesis?", "Science Query")
        self.test_request("Explain quantum computing", "Technology Query")
        self.test_request("How do I learn programming?", "Learning Query")
        
        # 6. Mathematical Tests
        print("\n🔢 MATHEMATICAL TESTS")
        self.test_request("What is 25 * 34?", "Basic Math")
        self.test_request("Solve x^2 + 5x + 6 = 0", "Equation Solving")
        
        # 7. Edge Case Tests
        print("\n⚠️ EDGE CASE TESTS")
        self.test_request("", "Empty Message")
        self.test_request("asdfghjkl", "Random Text")
        self.test_request("What is the meaning of life?", "Philosophical Query")
        
        # Print Summary
        self.print_summary()

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*80)
        print("📊 TEST RESULTS SUMMARY")
        print("="*80)
        print(f"🧪 Total Tests: {self.test_count}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.test_count * 100) if self.test_count > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🏆 EXCELLENT: Chatbot performing exceptionally well!")
        elif success_rate >= 75:
            print("👍 GOOD: Chatbot performing well with minor issues")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Chatbot has significant issues to address")
        else:
            print("🚨 POOR: Chatbot needs major improvements")
        
        print("="*80)

def main():
    """Main function to run tests"""
    print("⏳ Waiting for server to be ready...")
    time.sleep(10)  # Wait for server to fully start
    
    tester = ChatbotTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
