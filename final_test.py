#!/usr/bin/env python3
"""
Quick Test Results Summary for Enhanced Clang Chatbot
"""

import requests
import json
import time

def test_scenario(message, test_name):
    """Quick test function"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/",
            headers={"Content-Type": "application/json"},
            json={"message": message},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"status": "✅ PASS", "response_length": len(data['response'])}
        else:
            return {"status": "❌ FAIL", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)}

def main():
    print("🚀 FINAL TESTING SUMMARY")
    print("=" * 60)
    
    test_cases = [
        ("hey", "Greeting Response"),
        ("what's your name", "Identity Response"),
        ("What are the symptoms of asthma?", "Medical Knowledge"),
        ("write an essay about technology", "Essay Writing"),
        ("What is 15 + 25?", "Mathematical Query"),
        ("Explain artificial intelligence", "General AI Knowledge"),
        ("I have a headache", "Medical Symptoms"),
        ("write an essay on education", "Essay - Education"),
    ]
    
    results = []
    
    for message, test_name in test_cases:
        print(f"\n🧪 Testing: {test_name}")
        result = test_scenario(message, test_name)
        results.append((test_name, result))
        print(f"   {result['status']}")
        if 'response_length' in result:
            print(f"   📏 Response Length: {result['response_length']} chars")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result['status'] == "✅ PASS")
    total = len(results)
    
    for test_name, result in results:
        print(f"{result['status']} {test_name}")
    
    print(f"\n🎯 Success Rate: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🏆 ALL TESTS PASSED! Chatbot is working perfectly!")
    elif passed >= total * 0.8:
        print("👍 EXCELLENT! Most features working well!")
    else:
        print("⚠️  Some issues detected. Check failed tests.")

if __name__ == "__main__":
    main()
