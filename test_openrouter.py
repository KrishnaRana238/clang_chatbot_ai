#!/usr/bin/env python3
"""
Quick test for OpenRouter API key with the free Gemini model
"""
import os
import sys
import asyncio

# Add the project directory to Python path
sys.path.append('/Users/krishnarana/Desktop/Web Development/chatbot')

# Set environment variable for the API key
os.environ['OPENROUTER_API_KEY'] = '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'

# Import Django setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from chatbot_app.chatbot_service import OpenSourceChatbotService

async def test_openrouter_key():
    """Test the OpenRouter API key with free Gemini model"""
    
    print("🧪 Testing OpenRouter API Key with Free Gemini Model")
    print("=" * 60)
    
    # Create chatbot service (it will automatically detect the API key)
    chatbot = OpenSourceChatbotService()
    
    print(f"📍 Method selected: {chatbot.method}")
    print("-" * 40)
    
    # Test cases
    test_cases = [
        "3+5",  # Math (should be handled by built-in math)
        "Hello! Can you help me?",  # Simple conversation  
        "Write a Python function to calculate factorial",  # Complex coding task
        "Explain how photosynthesis works",  # Knowledge question
        "What is the capital of France?",  # Simple question
    ]
    
    for i, test_msg in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_msg}")
        print("-" * 30)
        
        try:
            response = await chatbot.get_response(test_msg)
            print(f"🤖 Response: {response[:150]}{'...' if len(response) > 150 else ''}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing completed!")
    
    if chatbot.method == "openrouter_api":
        print("✅ OpenRouter API is working!")
    else:
        print("ℹ️  Using fallback method. Check API key or connection.")

if __name__ == "__main__":
    asyncio.run(test_openrouter_key())
