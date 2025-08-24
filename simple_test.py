#!/usr/bin/env python3
"""
Simple test script to verify modular response system with python3
"""
import requests
import json

def test_module(message, module_name):
    """Test a specific module with a message"""
    try:
        url = "http://127.0.0.1:8003/api/chat/"
        payload = {"message": message, "session_id": "test"}
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            length = len(response_text)
            return f"✅ {module_name}: {length} chars"
        else:
            return f"❌ {module_name}: HTTP {response.status_code}"
    except Exception as e:
        return f"❌ {module_name}: {str(e)}"

def main():
    print("🧪 MODULAR RESPONSE SYSTEM TEST WITH PYTHON3")
    print("=" * 50)
    
    tests = [
        ("WWW", "Acronym Module"),
        ("solve x + 5 = 10", "Mathematics Module"),  
        ("who wrote hamlet", "Literature Module"),
        ("what is entrepreneurship", "Business Module"),
        ("tell me about mars", "Astronomy Module"),
        ("explain photosynthesis", "Biology Module")
    ]
    
    for message, module in tests:
        result = test_module(message, module)
        print(result)

if __name__ == "__main__":
    main()
