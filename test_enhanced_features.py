"""
Quick Medical and Essay Test for Clang Chatbot
Test the new medical and essay writing capabilities
"""

import requests
import json

def test_medical_query():
    """Test a medical query"""
    url = "http://127.0.0.1:8000/api/chat/"
    data = {"message": "What are the symptoms of diabetes?"}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("🏥 **Medical Query Test:**")
            print(f"Query: {data['message']}")
            print(f"Response: {result.get('response', 'No response')}")
            print("\n" + "="*50 + "\n")
            return True
        else:
            print(f"❌ Medical test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Medical test error: {e}")
        return False

def test_essay_query():
    """Test an essay writing query"""
    url = "http://127.0.0.1:8000/api/chat/"
    data = {"message": "write an essay about artificial intelligence"}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("📝 **Essay Writing Test:**")
            print(f"Query: {data['message']}")
            print(f"Response: {result.get('response', 'No response')}")
            print("\n" + "="*50 + "\n")
            return True
        else:
            print(f"❌ Essay test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Essay test error: {e}")
        return False

def test_name_query():
    """Test the name response"""
    url = "http://127.0.0.1:8000/api/chat/"
    data = {"message": "what's your name?"}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("🤖 **Name Query Test:**")
            print(f"Query: {data['message']}")
            print(f"Response: {result.get('response', 'No response')}")
            print("\n" + "="*50 + "\n")
            return True
        else:
            print(f"❌ Name test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Name test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 **Testing Enhanced Clang Chatbot Features**\n")
    
    # Test name response
    print("Testing trained responses...")
    name_success = test_name_query()
    
    # Test medical functionality
    print("Testing medical capabilities...")
    medical_success = test_medical_query()
    
    # Test essay writing
    print("Testing essay writing...")
    essay_success = test_essay_query()
    
    # Summary
    print("📊 **Test Summary:**")
    print(f"✅ Name Response: {'PASSED' if name_success else 'FAILED'}")
    print(f"🏥 Medical Query: {'PASSED' if medical_success else 'FAILED'}")
    print(f"📝 Essay Writing: {'PASSED' if essay_success else 'FAILED'}")
    
    if all([name_success, medical_success, essay_success]):
        print("\n🎉 **All tests PASSED! Clang is fully enhanced!** 🎉")
    else:
        print("\n⚠️ **Some tests failed. Check server status.** ⚠️")
