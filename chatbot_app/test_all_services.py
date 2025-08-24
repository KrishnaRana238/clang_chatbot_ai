#!/usr/bin/env python3
"""
Comprehensive test of all chatbot services
"""

import asyncio
import sys
import os

def test_ai_chatbot():
    """Test the main AI chatbot service"""
    print("=== TESTING AI CHATBOT SERVICE ===")
    try:
        from ai_chatbot import ChatbotAI
        chatbot = ChatbotAI()
        
        # Test identity
        identity_response = chatbot.generate_response("Who are you?")
        print(f"✅ AI Chatbot Identity: {identity_response[:100]}...")
        
        # Test programming question
        code_response = chatbot.generate_response("Write a Python function to sort a list")
        print(f"✅ AI Chatbot Code Response: {len(code_response)} characters generated")
        
    except Exception as e:
        print(f"❌ AI Chatbot Error: {e}")

def test_medical_service():
    """Test the medical service"""
    print("\n=== TESTING MEDICAL SERVICE ===")
    try:
        from advanced_medical_service import advanced_medical_service
        
        # Test with diabetes
        response = advanced_medical_service.get_medical_response("What are the symptoms of diabetes?")
        if response:
            print(f"✅ Medical Service: {len(response)} characters - {response[:100]}...")
        else:
            print("❌ Medical Service: No response generated")
            
    except Exception as e:
        print(f"❌ Medical Service Error: {e}")

def test_essay_service():
    """Test the essay writing service"""
    print("\n=== TESTING ESSAY SERVICE ===")
    try:
        from essay_writing_service import essay_writing_service
        
        response = essay_writing_service.get_essay_response("Write about AI")
        if response:
            print(f"✅ Essay Service: {len(response)} characters - {response[:100]}...")
        else:
            print("❌ Essay Service: No response generated")
            
    except Exception as e:
        print(f"❌ Essay Service Error: {e}")

def test_emotional_service():
    """Test the emotional intelligence service"""
    print("\n=== TESTING EMOTIONAL SERVICE ===")
    try:
        from emotional_intelligence_service import emotional_intelligence_service
        
        response = emotional_intelligence_service.get_emotional_response("I feel sad today")
        if response:
            print(f"✅ Emotional Service: {len(response)} characters - {response[:100]}...")
        else:
            print("❌ Emotional Service: No response generated")
            
    except Exception as e:
        print(f"❌ Emotional Service Error: {e}")

async def test_enhanced_clang():
    """Test the enhanced clang service"""
    print("\n=== TESTING ENHANCED CLANG SERVICE ===")
    try:
        from enhanced_clang_service import enhanced_clang
        
        response = await enhanced_clang.get_enhanced_response("How do I create a Python function?")
        if response and 'response' in response:
            content = response['response']
            print(f"✅ Enhanced Clang: {len(content)} characters - {content[:100]}...")
        else:
            print("❌ Enhanced Clang: No response generated")
            
    except Exception as e:
        print(f"❌ Enhanced Clang Error: {e}")

def test_views_integration():
    """Test the Django views integration"""
    print("\n=== TESTING VIEWS INTEGRATION ===")
    try:
        from views import ChatView
        
        # Check imports
        print("✅ Views imported successfully")
        print("✅ All service imports in views should be working")
        
    except Exception as e:
        print(f"❌ Views Error: {e}")

async def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE SERVICE TEST STARTED")
    print("=" * 50)
    
    # Test all services
    test_ai_chatbot()
    test_medical_service()
    test_essay_service()
    test_emotional_service()
    await test_enhanced_clang()
    test_views_integration()
    
    print("\n" + "=" * 50)
    print("🧪 COMPREHENSIVE SERVICE TEST COMPLETED")

if __name__ == "__main__":
    asyncio.run(main())
