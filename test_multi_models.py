#!/usr/bin/env python3
"""
Multi-Model Testing and Comparison Script
Tests both Gemini and DeepSeek models to find the best integration
"""
import os
import sys
import asyncio
import time

# Set up environment
sys.path.append('/Users/krishnarana/Desktop/Web Development/chatbot')
os.environ['OPENROUTER_API_KEY'] = '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'

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from chatbot_app.chatbot_service import OpenSourceChatbotService

async def compare_models():
    """Compare responses from different models"""
    
    print("🚀 Multi-Model Integration Testing")
    print("=" * 60)
    
    chatbot = OpenSourceChatbotService()
    
    # Test cases for different scenarios
    test_cases = [
        {
            "category": "🧮 Mathematical Reasoning",
            "query": "What is the meaning of life from a philosophical perspective?"
        },
        {
            "category": "💻 Code Generation", 
            "query": "Write a Python function to find the largest prime number less than 100"
        },
        {
            "category": "🧠 Complex Analysis",
            "query": "Analyze the pros and cons of artificial intelligence in healthcare"
        },
        {
            "category": "💬 General Conversation",
            "query": "Tell me about the history of space exploration"
        },
        {
            "category": "🔬 Problem Solving",
            "query": "How would you solve climate change if you were a world leader?"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['category']}")
        print(f"Query: {test_case['query']}")
        print("-" * 50)
        
        # Test with intelligent model selection
        print("🤖 Intelligent Model Selection:")
        response = await chatbot.get_response(test_case['query'])
        print(f"Response: {response[:150]}{'...' if len(response) > 150 else ''}")
        
        print("\n📊 Comparing All Models:")
        # Test all models for comparison
        model_results = await chatbot._test_all_models(test_case['query'])
        
        for model_name, result in model_results.items():
            model_short = model_name.split('/')[-1].replace(':free', '')
            status_emoji = "✅" if result['status'] == 'success' else "❌"
            print(f"  {status_emoji} {model_short}: {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}")
        
        print("\n" + "="*60)
        await asyncio.sleep(1)  # Rate limiting
    
    print("\n🎯 Integration Testing Complete!")
    print("\n💡 Model Selection Summary:")
    print("• DeepSeek: Best for reasoning, analysis, coding")
    print("• Gemini: Best for general conversation, knowledge")
    print("• Your chatbot automatically picks the best model!")

async def test_specific_integrations():
    """Test specific integration scenarios"""
    print("\n🔧 Testing Integration Scenarios")
    print("=" * 40)
    
    chatbot = OpenSourceChatbotService()
    
    integration_tests = [
        "3+5",  # Should use built-in math
        "Write API integration code",  # Should use DeepSeek
        "What's the weather like?",  # General (could benefit from weather API)
        "Help me debug this error",  # Should use DeepSeek
        "Tell me a joke",  # Should use Gemini
    ]
    
    for test in integration_tests:
        print(f"\n🧪 Testing: {test}")
        response = await chatbot.get_response(test)
        print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")

if __name__ == "__main__":
    async def main():
        await compare_models()
        await test_specific_integrations()
    
    asyncio.run(main())
