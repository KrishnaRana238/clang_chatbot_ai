#!/usr/bin/env python3
"""
Interactive Question-Based Test: Focus on chatbot responses to various questions
"""
import requests
import json

API_URL = "http://127.0.0.1:8005/api/chat/"

# Diverse questions to test different modules
test_questions = [
    # Acronyms
    "What does WWW stand for?",
    "Explain GPU",
    
    # Programming
    "Write a Python function for binary search",
    "What is object-oriented programming?",
    
    # Science & Biology
    "How does photosynthesis work?",
    "Explain DNA structure",
    
    # Astronomy
    "Tell me about the planet Mars",
    "What is a black hole?",
    
    # Mathematics
    "Solve: 2x + 5 = 15",
    "What is calculus?",
    
    # Literature
    "Who wrote Romeo and Juliet?",
    "Explain what is poetry",
    
    # History
    "When did World War 2 end?",
    "Who was Napoleon Bonaparte?",
    
    # Business
    "What is entrepreneurship?",
    "Explain market economics",
    
    # Arts
    "What is Renaissance art?",
    "Explain different music genres",
    
    # Technology
    "What is artificial intelligence?",
    "How does the internet work?"
]

def ask_chatbot(question):
    """Send question to chatbot and get response"""
    try:
        payload = {"message": question, "session_id": "question_test"}
        response = requests.post(API_URL, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', 'No response received')
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def display_response(question, response):
    """Display question and response in a nice format"""
    print(f"\n{'='*60}")
    print(f"❓ QUESTION: {question}")
    print(f"{'='*60}")
    
    if len(response) > 500:
        # Show first part and summary for long responses
        print(f"✅ RESPONSE ({len(response)} characters):")
        print(response[:300])
        print(f"\n[... continues for {len(response)-300} more characters ...]")
        print(f"\nLAST PART:")
        print(response[-200:])
    else:
        print(f"✅ RESPONSE ({len(response)} characters):")
        print(response)

def main():
    print("🧪 CHATBOT QUESTION-BASED TEST")
    print("Testing different modules with various questions")
    print("="*60)
    
    successful_responses = 0
    total_questions = len(test_questions)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[Test {i}/{total_questions}]")
        response = ask_chatbot(question)
        
        if not response.startswith("Error:"):
            successful_responses += 1
            display_response(question, response)
        else:
            print(f"\n❌ QUESTION: {question}")
            print(f"❌ {response}")
        
        # Pause between questions for readability
        input("\nPress Enter for next question...")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Questions Asked: {total_questions}")
    print(f"Successful Responses: {successful_responses}")
    print(f"Success Rate: {(successful_responses/total_questions)*100:.1f}%")
    
    if successful_responses == total_questions:
        print("🌟 PERFECT! All questions answered successfully!")
    elif successful_responses >= total_questions * 0.9:
        print("✅ EXCELLENT! Most questions answered well!")
    elif successful_responses >= total_questions * 0.7:
        print("👍 GOOD! Majority of questions answered!")
    else:
        print("⚠️ NEEDS IMPROVEMENT! Some questions not handled well!")

if __name__ == "__main__":
    main()
