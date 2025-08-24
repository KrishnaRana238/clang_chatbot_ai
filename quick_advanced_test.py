#!/usr/bin/env python3
"""
Quick advanced test - 10 complex questions to verify modular system ability
"""
import requests
import json

API_URL = "http://127.0.0.1:8005/api/chat/"

quick_advanced_questions = [
    "Explain the difference between RAM and SSD in modern computers.",
    "Write a Python function to check if a string is a palindrome.",
    "Describe the process of star formation in a nebula.",
    "How does CRISPR gene editing work in biotechnology?",
    "Analyze the causes and consequences of the French Revolution.",
    "Describe the process of photosynthesis at the molecular level.",
    "Prove the Pythagorean theorem using geometry.",
    "Explain the concept of quantum entanglement and its implications.",
    "Analyze the theme of fate in Shakespeare's Macbeth.",
    "How do startups achieve product-market fit?"
]

def test_question(question, num):
    try:
        payload = {"message": question, "session_id": f"test_{num}"}
        response = requests.post(API_URL, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            text = data.get('response', '')
            length = len(text)
            preview = text[:100].replace('\n', ' ') + ('...' if len(text) > 100 else '')
            return length, preview, "✅" if length > 500 else "⚠️" if length > 0 else "❌"
        else:
            return 0, f"HTTP {response.status_code}", "❌"
    except Exception as e:
        return 0, str(e), "❌"

def main():
    print("🚀 QUICK ADVANCED MODULAR ABILITY TEST")
    print("="*50)
    
    results = []
    for i, question in enumerate(quick_advanced_questions, 1):
        print(f"\nQ{i}: {question[:60]}{'...' if len(question) > 60 else ''}")
        length, preview, status = test_question(question, i)
        print(f"{status} {length} chars: {preview}")
        results.append((status == "✅", length))
    
    # Summary
    successful = sum(1 for success, _ in results if success)
    total_chars = sum(length for _, length in results)
    avg_length = total_chars / len(results) if results else 0
    
    print(f"\n📊 RESULTS: {successful}/{len(results)} substantial responses")
    print(f"📏 Average response length: {avg_length:.0f} characters")
    
    if successful >= 8:
        print("🌟 EXCELLENT: Advanced modular system working perfectly!")
    elif successful >= 6:
        print("✅ GOOD: Strong modular system performance!")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Some modules need attention")

if __name__ == "__main__":
    main()
