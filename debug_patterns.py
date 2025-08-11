#!/usr/bin/env python3

import re

def debug_pattern_matching():
    """Debug exactly what's happening with our patterns"""
    
    query = "what is the full form of www"
    query_lower = query.lower()
    
    print(f"Original query: '{query}'")
    print(f"Lowercase query: '{query_lower}'")
    print()
    
    # Test individual patterns
    patterns = [
        r'full form\s*(?:of\s+)?',  # "full form" or "full form of"
        r'abbreviation',
        r'acronym', 
        r'stands for',
        r'what does.*stand',
        r'meaning of'
    ]
    
    print("Pattern matching results:")
    print("-" * 40)
    
    for i, pattern in enumerate(patterns, 1):
        match = re.search(pattern, query_lower)
        if match:
            print(f"Pattern {i}: '{pattern}' -> ✅ MATCH")
            print(f"  Matched text: '{match.group()}'")
            print(f"  Position: {match.start()}-{match.end()}")
        else:
            print(f"Pattern {i}: '{pattern}' -> ❌ NO MATCH")
        print()
    
    # Test the any() condition like in our code
    any_match = any(re.search(pattern, query_lower) for pattern in patterns)
    print(f"Overall result: {'✅ DETECTED' if any_match else '❌ MISSED'}")

if __name__ == "__main__":
    debug_pattern_matching()
