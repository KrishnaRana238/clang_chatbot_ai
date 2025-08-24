#!/usr/bin/env python3
"""
Test script for the modular response system
"""
import sys
import os

# Add the chatbot directory to the path
sys.path.append('/Users/krishnarana/Desktop/Web Development/chatbot')

# Test imports from the response modules
try:
    from chatbot_app.response_modules import (
        AcronymResponses,
        ProgrammingResponses,
        AstronomyResponses,
        ScienceResponses,
        TechnologyResponses,
        HistoryResponses,
        GeographyResponses,
        BiologyResponses,
        EnvironmentalResponses,
        MathematicsResponses,
        PhysicsResponses,
        ArtsResponses,
        LiteratureResponses,
        BusinessResponses
    )
    print("✅ All modular response classes imported successfully!")
    
    # Test each module with a sample query
    test_queries = [
        ("WWW", AcronymResponses.handle_acronym_questions),
        ("What is binary search?", ProgrammingResponses.generate_programming_response),
        ("Tell me about Mars", AstronomyResponses.generate_astronomy_response),
        ("Explain photosynthesis", ScienceResponses.generate_science_response),
        ("What is AI?", TechnologyResponses.generate_technology_response),
        ("Who was Napoleon?", HistoryResponses.generate_history_response),
        ("What is the capital of France?", GeographyResponses.generate_geography_response),
        ("Explain DNA", BiologyResponses.generate_biology_response),
        ("What is climate change?", EnvironmentalResponses.generate_environmental_response),
        ("Solve x + 5 = 10", MathematicsResponses.generate_mathematics_response),
        ("Explain Newton's laws", PhysicsResponses.generate_physics_response),
        ("Tell me about Renaissance art", ArtsResponses.generate_arts_response),
        ("Who wrote Hamlet?", LiteratureResponses.generate_literature_response),
        ("What is entrepreneurship?", BusinessResponses.generate_business_response)
    ]
    
    print("\n🧪 Testing modular response system:")
    print("="*50)
    
    for query, response_func in test_queries:
        try:
            response = response_func(query)
            print(f"✅ {query[:30]:<30} -> {len(response)} chars")
        except Exception as e:
            print(f"❌ {query[:30]:<30} -> Error: {e}")
    
    print("\n🎉 Modular system test completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all response modules are properly created and imported.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
