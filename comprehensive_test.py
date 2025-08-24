#!/usr/bin/env python3
"""
Comprehensive test script for the integrated modular response system
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/chat/"

def test_chatbot_response(query, expected_keywords=None):
    """Test a single query and analyze the response"""
    try:
        response = requests.post(BASE_URL, json={"message": query})
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get('response', '')
            response_length = len(bot_response)
            
            # Check for expected keywords if provided
            keyword_found = True
            if expected_keywords:
                keyword_found = any(keyword.lower() in bot_response.lower() for keyword in expected_keywords)
            
            status = "✅" if keyword_found else "⚠️"
            print(f"{status} {query[:40]:<40} | {response_length:>5} chars | Keywords: {keyword_found}")
            
            return bot_response, response_length
        else:
            print(f"❌ {query[:40]:<40} | HTTP {response.status_code}")
            return None, 0
            
    except Exception as e:
        print(f"❌ {query[:40]:<40} | Error: {e}")
        return None, 0

def main():
    print("🧪 COMPREHENSIVE MODULAR SYSTEM TEST")
    print("="*80)
    print(f"{'Query':<40} | {'Length':<6} | {'Status'}")
    print("-"*80)
    
    # Test cases organized by module
    test_cases = [
        # Acronym Module Tests
        ("What does WWW stand for?", ["World Wide Web", "internet"]),
        ("What is HTML?", ["HyperText", "markup", "language"]),
        ("Explain CSS", ["Cascading", "Style", "Sheets"]),
        ("What does NASA do?", ["space", "aeronautics", "administration"]),
        ("What is AI?", ["artificial", "intelligence"]),
        
        # Programming Module Tests
        ("Explain binary search algorithm", ["binary", "search", "algorithm"]),
        ("What is quicksort?", ["quicksort", "sorting", "algorithm"]),
        ("How do you code a loop in Python?", ["python", "loop", "for"]),
        ("What is recursion?", ["recursion", "function", "calls"]),
        
        # Astronomy Module Tests
        ("Tell me about Mars", ["Mars", "planet", "red"]),
        ("What is the solar system?", ["solar", "system", "planets"]),
        ("Explain black holes", ["black", "hole", "gravity"]),
        ("How big is the universe?", ["universe", "space", "galaxy"]),
        
        # Science Module Tests
        ("Explain photosynthesis", ["photosynthesis", "plants", "sunlight"]),
        ("What is an atom?", ["atom", "proton", "electron"]),
        ("How does gravity work?", ["gravity", "force", "mass"]),
        ("What is energy?", ["energy", "work", "force"]),
        
        # Biology Module Tests
        ("What is DNA?", ["DNA", "genetic", "nucleotide"]),
        ("Explain evolution", ["evolution", "species", "natural"]),
        ("How do cells work?", ["cell", "organism", "membrane"]),
        ("What is mitosis?", ["mitosis", "cell", "division"]),
        
        # History Module Tests
        ("Who was Napoleon?", ["Napoleon", "French", "emperor"]),
        ("Tell me about World War II", ["World War", "1939", "1945"]),
        ("What was the Renaissance?", ["Renaissance", "art", "period"]),
        ("Ancient Egyptian civilization", ["Egypt", "pharaoh", "pyramid"]),
        
        # Geography Module Tests
        ("What is the capital of France?", ["Paris", "France", "capital"]),
        ("Tell me about Asia", ["Asia", "continent", "largest"]),
        ("Where is Mount Everest?", ["Everest", "mountain", "Nepal"]),
        ("What are the seven continents?", ["continent", "Africa", "Asia"]),
        
        # Mathematics Module Tests
        ("Solve x + 5 = 10", ["x = 5", "equation", "algebra"]),
        ("What is calculus?", ["calculus", "derivative", "integral"]),
        ("Explain geometry", ["geometry", "shapes", "angles"]),
        ("What is a triangle?", ["triangle", "three", "sides"]),
        
        # Physics Module Tests
        ("Explain Newton's laws", ["Newton", "motion", "force"]),
        ("What is velocity?", ["velocity", "speed", "direction"]),
        ("How does acceleration work?", ["acceleration", "velocity", "time"]),
        ("What is thermodynamics?", ["thermodynamics", "heat", "energy"]),
        
        # Arts Module Tests
        ("Tell me about Renaissance art", ["Renaissance", "art", "painting"]),
        ("Who was Leonardo da Vinci?", ["Leonardo", "artist", "inventor"]),
        ("What is abstract art?", ["abstract", "art", "form"]),
        ("Explain music theory", ["music", "theory", "notes"]),
        
        # Literature Module Tests
        ("Who wrote Hamlet?", ["Shakespeare", "Hamlet", "playwright"]),
        ("What is poetry?", ["poetry", "poem", "verse"]),
        ("Tell me about Romeo and Juliet", ["Romeo", "Juliet", "tragedy"]),
        ("What is a sonnet?", ["sonnet", "poem", "lines"]),
        
        # Business Module Tests
        ("What is entrepreneurship?", ["entrepreneur", "business", "startup"]),
        ("Explain economics", ["economics", "market", "supply"]),
        ("What is marketing?", ["marketing", "product", "customer"]),
        ("How do businesses work?", ["business", "profit", "revenue"]),
    ]
    
    total_tests = len(test_cases)
    successful_tests = 0
    total_response_length = 0
    
    for query, expected_keywords in test_cases:
        response, length = test_chatbot_response(query, expected_keywords)
        if response:
            successful_tests += 1
            total_response_length += length
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    print("-"*80)
    print(f"📊 TEST SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {successful_tests}")
    print(f"   Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    print(f"   Average Response Length: {total_response_length//successful_tests if successful_tests > 0 else 0} chars")
    print(f"   Status: {'🎉 EXCELLENT' if successful_tests/total_tests > 0.9 else '⚠️ NEEDS REVIEW'}")

if __name__ == "__main__":
    main()
