#!/usr/bin/env python3

def test_phrase_matching():
    """Test if our phrase matching works for the problematic query"""
    
    query = "what is the full form of www"
    query_lower = query.lower()
    
    print(f"Testing query: '{query}'")
    print(f"Lowercase: '{query_lower}'")
    print()
    
    acronym_phrases = [
        'full form', 'full form of', 'full form of the', 'what is the full form',
        'abbreviation', 'abbreviation of', 'abbreviation for',
        'acronym', 'acronym for', 'acronym of',
        'stands for', 'stand for', 'what does', 'what do',
        'meaning of', 'means', 'definition of'
    ]
    
    print("Checking each phrase:")
    matches = []
    for phrase in acronym_phrases:
        if phrase in query_lower:
            print(f"✅ '{phrase}' -> FOUND")
            matches.append(phrase)
        else:
            print(f"❌ '{phrase}' -> not found")
    
    print(f"\nTotal matches: {len(matches)}")
    print(f"Matching phrases: {matches}")
    print(f"any() result: {any(phrase in query_lower for phrase in acronym_phrases)}")

if __name__ == "__main__":
    test_phrase_matching()
