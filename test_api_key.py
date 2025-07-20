#!/usr/bin/env python3
"""
Test script for OpenRouter API key
"""
import os
import sys
import django
import asyncio

# Add the project directory to the Python path
sys.path.append('/Users/krishnarana/Desktop/Web Development/chatbot')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from chatbot_app.chatbot_service import OpenSourceChatbotService

async def test_openrouter_api():
    """Test the OpenRouter API with the provided key"""
    
    # Your API key
    api_key = "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"
    
    print("🧪 Testing OpenRouter API Key...")
    print(f"Key: {api_key[:20]}...{api_key[-10:]}")
    print("-" * 50)
    
    # Create service instance and set the API key for testing
    service = OpenSourceChatbotService()
    service.openrouter_key = api_key
    service.method = "openrouter_api"
    
    # Test cases
    test_cases = [
        "3+5",  # Math test
        "Hello, can you help me?",  # Simple conversation
        "Write a Python function to calculate the area of a circle",  # Complex coding task
        "Explain how machine learning works",  # Knowledge question
    ]
    
    for i, test_message in enumerate(test_cases, 1):
        print(f"Test {i}: {test_message}")
        try:
            response = await service._get_openrouter_response(test_message)
            print(f"✅ Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 30)
    
    print("🎯 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_openrouter_api())
