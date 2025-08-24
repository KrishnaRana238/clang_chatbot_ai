#!/usr/bin/env python3
"""
Advanced modular system test: asks multiple complex questions to check chatbot ability
"""
import requests
import json
import time

API_URL = "http://127.0.0.1:8005/api/chat/"

advanced_questions = [
    # Acronym/Tech
    "Explain the difference between RAM and SSD in modern computers.",
    "What does API stand for and how does it work in web development?",
    # Programming
    "Write a Python function to check if a string is a palindrome.",
    "Explain the time complexity of quicksort and compare it to merge sort.",
    # Astronomy
    "Describe the process of star formation in a nebula.",
    "What evidence supports the Big Bang theory?",
    # Science
    "How does CRISPR gene editing work in biotechnology?",
    "Explain the laws of thermodynamics with real-world examples.",
    # Technology
    "How does blockchain ensure security and decentralization?",
    "What are the main differences between supervised and unsupervised machine learning?",
    # History
    "Analyze the causes and consequences of the French Revolution.",
    "How did the Industrial Revolution change global economies?",
    # Geography
    "Why is the Amazon rainforest important for the Earth's climate?",
    "Compare the political systems of the USA and China.",
    # Biology
    "Describe the process of photosynthesis at the molecular level.",
    "How do vaccines stimulate the immune system?",
    # Environmental
    "What are the most effective strategies to combat climate change?",
    "Explain the greenhouse effect and its impact on global warming.",
    # Mathematics
    "Prove the Pythagorean theorem using geometry.",
    "What is the significance of eigenvalues and eigenvectors in linear algebra?",
    # Physics
    "Explain the concept of quantum entanglement and its implications.",
    "How does general relativity explain the bending of light by gravity?",
    # Arts
    "Discuss the influence of Impressionism on modern art.",
    "How did the Renaissance change the role of artists in society?",
    # Literature
    "Analyze the theme of fate in Shakespeare's Macbeth.",
    "What are the characteristics of Romantic poetry?",
    # Business
    "How do startups achieve product-market fit?",
    "Explain the concept of supply and demand with a real-world example."
]

def ask_question(question):
    try:
        payload = {"message": question, "session_id": "advanced_test"}
        response = requests.post(API_URL, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            text = data.get('response', '')
            return len(text), text[:120].replace('\n', ' ') + ('...' if len(text) > 120 else '')
        else:
            return 0, f"HTTP {response.status_code}"
    except Exception as e:
        return 0, str(e)

def main():
    print("🧪 ADVANCED MODULAR SYSTEM ABILITY TEST")
    print("="*60)
    
    successful_responses = 0
    substantial_responses = 0
    total_questions = len(advanced_questions)
    
    for i, q in enumerate(advanced_questions, 1):
        print(f"Q{i:2d}: {q}")
        length, preview = ask_question(q)
        
        if length > 0:
            successful_responses += 1
            
        if length > 500:
            substantial_responses += 1
            print(f"   ✅ {length} chars | Preview: {preview}")
        elif length > 0:
            print(f"   ⚠️  {length} chars (short) | Preview: {preview}")
        else:
            print(f"   ❌ Error: {preview}")
        
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*60)
    print("📊 ADVANCED ABILITY TEST RESULTS")
    print("="*60)
    print(f"Total Questions:       {total_questions}")
    print(f"Successful Responses:  {successful_responses} ({successful_responses/total_questions*100:.1f}%)")
    print(f"Substantial Responses: {substantial_responses} ({substantial_responses/total_questions*100:.1f}%)")
    
    if substantial_responses >= total_questions * 0.9:
        print("🌟 EXCELLENT: Advanced modular system performing at expert level!")
    elif substantial_responses >= total_questions * 0.75:
        print("✅ VERY GOOD: Strong performance across multiple domains!")
    elif substantial_responses >= total_questions * 0.5:
        print("⚠️  GOOD: Decent performance, some areas for improvement")
    else:
        print("❌ NEEDS WORK: Significant improvements needed")
    
    print("\n🎉 Advanced ability test completed!")

if __name__ == "__main__":
    main()
