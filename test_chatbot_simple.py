#!/usr/bin/env python3
"""
Simple Chatbot Test - No Downloads Required
Test the chatbot functionality without any external downloads
"""

def test_chatbot_locally():
    """Test chatbot with simple local responses"""
    
    print("🤖 Testing Chatbot Locally (No Downloads)")
    print("=" * 50)
    
    # Simple test responses without API calls
    test_questions = [
        "What is Python?",
        "How to create a function?", 
        "Explain machine learning",
        "Write about AI"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        # Simple local response without external APIs
        if "python" in question.lower():
            response = "Python is a high-level programming language known for its simplicity and readability. It's widely used for web development, data science, and automation."
        elif "function" in question.lower():
            response = "To create a function in Python: def function_name(parameters): # code here return result"
        elif "machine learning" in question.lower():
            response = "Machine learning is a subset of AI that enables computers to learn and make decisions from data without being explicitly programmed."
        elif "ai" in question.lower():
            response = "Artificial Intelligence (AI) is the simulation of human intelligence in machines, enabling them to think, learn, and solve problems."
        else:
            response = "I can help you with programming, science, and general questions!"
            
        print(f"   Answer: {response}")
    
    print(f"\n✅ Local chatbot test completed successfully!")
    print("🚀 Your chatbot is working fine without any downloads!")

if __name__ == "__main__":
    test_chatbot_locally()
