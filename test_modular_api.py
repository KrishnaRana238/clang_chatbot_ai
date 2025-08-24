#!/usr/bin/env python3
"""
Comprehensive test script for the modular response system
Tests API endpoints with various topic queries
"""
import requests
import json
import time

# Test configuration
BASE_URL = "http://127.0.0.1:8001"
API_ENDPOINT = f"{BASE_URL}/api/chat/"

# Test cases for different modular response categories
test_cases = [
    # Acronym responses
    {"message": "WWW", "expected_module": "Acronym", "description": "WWW acronym test"},
    {"message": "What is HTML?", "expected_module": "Acronym", "description": "HTML acronym test"},
    {"message": "GPU", "expected_module": "Acronym", "description": "GPU acronym test"},
    
    # Programming responses
    {"message": "What is binary search?", "expected_module": "Programming", "description": "Binary search algorithm"},
    {"message": "Explain quicksort algorithm", "expected_module": "Programming", "description": "Quicksort algorithm"},
    {"message": "Python programming example", "expected_module": "Programming", "description": "Python programming"},
    
    # Astronomy responses
    {"message": "Tell me about Mars", "expected_module": "Astronomy", "description": "Mars planet information"},
    {"message": "What is the solar system?", "expected_module": "Astronomy", "description": "Solar system overview"},
    {"message": "Explain black holes", "expected_module": "Astronomy", "description": "Black hole explanation"},
    
    # Science responses
    {"message": "Explain photosynthesis", "expected_module": "Science", "description": "Photosynthesis process"},
    {"message": "What is chemistry?", "expected_module": "Science", "description": "Chemistry basics"},
    {"message": "Physics laws", "expected_module": "Science", "description": "Physics principles"},
    
    # Technology responses
    {"message": "What is AI?", "expected_module": "Technology", "description": "Artificial Intelligence"},
    {"message": "Machine learning explained", "expected_module": "Technology", "description": "Machine Learning"},
    {"message": "Computer networks", "expected_module": "Technology", "description": "Computer Networks"},
    
    # History responses
    {"message": "Who was Napoleon?", "expected_module": "History", "description": "Napoleon Bonaparte"},
    {"message": "World War 2", "expected_module": "History", "description": "World War 2 history"},
    {"message": "Ancient civilizations", "expected_module": "History", "description": "Ancient history"},
    
    # Geography responses
    {"message": "What is the capital of France?", "expected_module": "Geography", "description": "France capital"},
    {"message": "Tell me about continents", "expected_module": "Geography", "description": "World continents"},
    {"message": "Countries in Asia", "expected_module": "Geography", "description": "Asian countries"},
    
    # Biology responses
    {"message": "Explain DNA", "expected_module": "Biology", "description": "DNA structure and function"},
    {"message": "What is evolution?", "expected_module": "Biology", "description": "Evolution theory"},
    {"message": "Human body systems", "expected_module": "Biology", "description": "Human biology"},
    
    # Environmental responses
    {"message": "What is climate change?", "expected_module": "Environmental", "description": "Climate change"},
    {"message": "Global warming effects", "expected_module": "Environmental", "description": "Global warming"},
    {"message": "Renewable energy", "expected_module": "Environmental", "description": "Renewable energy"},
    
    # Mathematics responses (NEW)
    {"message": "Solve x + 5 = 10", "expected_module": "Mathematics", "description": "Algebra equation"},
    {"message": "What is calculus?", "expected_module": "Mathematics", "description": "Calculus basics"},
    {"message": "Geometry formulas", "expected_module": "Mathematics", "description": "Geometry principles"},
    
    # Physics responses (NEW)
    {"message": "Explain Newton's laws", "expected_module": "Physics", "description": "Newton's laws of motion"},
    {"message": "What is force?", "expected_module": "Physics", "description": "Force and motion"},
    {"message": "Classical mechanics", "expected_module": "Physics", "description": "Classical mechanics"},
    
    # Arts responses (NEW)
    {"message": "Tell me about Renaissance art", "expected_module": "Arts", "description": "Renaissance art movement"},
    {"message": "What is painting?", "expected_module": "Arts", "description": "Painting as art form"},
    {"message": "Music instruments", "expected_module": "Arts", "description": "Musical instruments"},
    
    # Literature responses (NEW)
    {"message": "Who wrote Hamlet?", "expected_module": "Literature", "description": "Shakespeare's Hamlet"},
    {"message": "What is poetry?", "expected_module": "Literature", "description": "Poetry basics"},
    {"message": "Drama and theater", "expected_module": "Literature", "description": "Dramatic arts"},
    
    # Business responses (NEW)
    {"message": "What is entrepreneurship?", "expected_module": "Business", "description": "Entrepreneurship basics"},
    {"message": "Economics principles", "expected_module": "Business", "description": "Economic theory"},
    {"message": "Business management", "expected_module": "Business", "description": "Management principles"},
]

def test_api_endpoint(message, description):
    """Test a single API endpoint"""
    try:
        payload = {"message": message, "session_id": "test_session"}
        response = requests.post(API_ENDPOINT, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            response_length = len(response_text)
            
            # Check if response is substantial (indicating modular system worked)
            is_substantial = response_length > 500
            
            return {
                "success": True,
                "response_length": response_length,
                "is_substantial": is_substantial,
                "preview": response_text[:100] + "..." if len(response_text) > 100 else response_text
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "response_length": 0,
                "is_substantial": False
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_length": 0,
            "is_substantial": False
        }

def main():
    print("🧪 COMPREHENSIVE MODULAR RESPONSE SYSTEM TEST")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Server is running at {BASE_URL}")
    except:
        print(f"❌ Server not accessible at {BASE_URL}")
        print("Please start the server with: python manage.py runserver 8001")
        return
    
    print(f"\n🎯 Testing {len(test_cases)} different modular response scenarios...")
    print("-" * 60)
    
    results = {
        "total_tests": len(test_cases),
        "successful_requests": 0,
        "substantial_responses": 0,
        "failed_requests": 0,
        "module_coverage": {}
    }
    
    for i, test_case in enumerate(test_cases, 1):
        message = test_case["message"]
        expected_module = test_case["expected_module"]
        description = test_case["description"]
        
        print(f"Test {i:2d}: {description:<30} ", end="")
        
        result = test_api_endpoint(message, description)
        
        if result["success"]:
            results["successful_requests"] += 1
            
            if result["is_substantial"]:
                results["substantial_responses"] += 1
                status = f"✅ {result['response_length']:4d} chars"
            else:
                status = f"⚠️  {result['response_length']:4d} chars (short)"
                
            # Track module coverage
            if expected_module not in results["module_coverage"]:
                results["module_coverage"][expected_module] = {"tested": 0, "successful": 0}
            results["module_coverage"][expected_module]["tested"] += 1
            if result["is_substantial"]:
                results["module_coverage"][expected_module]["successful"] += 1
                
        else:
            results["failed_requests"] += 1
            status = f"❌ {result['error']}"
        
        print(status)
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    success_rate = (results["successful_requests"] / results["total_tests"]) * 100
    substantial_rate = (results["substantial_responses"] / results["total_tests"]) * 100
    
    print(f"Total Tests:           {results['total_tests']}")
    print(f"Successful Requests:   {results['successful_requests']} ({success_rate:.1f}%)")
    print(f"Substantial Responses: {results['substantial_responses']} ({substantial_rate:.1f}%)")
    print(f"Failed Requests:       {results['failed_requests']}")
    
    print(f"\n🎯 MODULE COVERAGE:")
    print("-" * 40)
    for module, stats in results["module_coverage"].items():
        coverage = (stats["successful"] / stats["tested"]) * 100 if stats["tested"] > 0 else 0
        print(f"{module:<15}: {stats['successful']}/{stats['tested']} ({coverage:.0f}%)")
    
    # Overall assessment
    print(f"\n🏆 OVERALL ASSESSMENT:")
    if substantial_rate >= 90:
        print("🌟 EXCELLENT: Modular system working perfectly!")
    elif substantial_rate >= 75:
        print("✅ GOOD: Modular system working well!")
    elif substantial_rate >= 50:
        print("⚠️  FAIR: Some modules need attention")
    else:
        print("❌ POOR: Modular system needs significant fixes")
    
    print(f"\n🎉 Test completed! Modular response system assessment finished.")

if __name__ == "__main__":
    main()
