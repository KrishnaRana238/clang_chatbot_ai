#!/usr/bin/env python3

import re

def test_acronym_detection():
    """Test if our regex patterns correctly detect acronym questions"""
    
    test_queries = [
        "what is the full form of www",
        "what is the full form www", 
        "full form of www",
        "www stands for",
        "what does www stand for",
        "abbreviation of www",
        "meaning of www acronym"
    ]
    
    # Same patterns as in our service
    acronym_patterns = [
        r'full form\s*(?:of\s+)?',  # "full form" or "full form of"
        r'abbreviation',
        r'acronym', 
        r'stands for',
        r'what does.*stand',
        r'meaning of'
    ]
    
    print("Testing acronym detection patterns:")
    print("=" * 50)
    
    for query in test_queries:
        query_lower = query.lower()
        matches = []
        
        for pattern in acronym_patterns:
            if re.search(pattern, query_lower):
                matches.append(pattern)
        
        result = "✅ DETECTED" if matches else "❌ MISSED"
        print(f"{result}: '{query}'")
        if matches:
            print(f"    Matched patterns: {matches}")
        print()

if __name__ == "__main__":
    test_acronym_detection()
