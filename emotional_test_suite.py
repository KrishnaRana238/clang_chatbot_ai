#!/usr/bin/env python3
"""
Emotional Intelligence Test Suite for Enhanced Clang Chatbot
Testing human chit-chat, emotional detection, and conversational abilities
"""

import requests
import json
import time

def test_emotional_scenario(message, test_name, expected_keywords=None):
    """Test emotional and conversational scenarios"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/chat/",
            headers={"Content-Type": "application/json"},
            json={"message": message},
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data['response']
            
            result = {
                "status": "✅ PASS", 
                "response_length": len(bot_response),
                "emotional_indicators": 0
            }
            
            # Check for emotional indicators
            emotional_indicators = ['😊', '😄', '💙', '🫂', '💝', '😔', '💢', '🤗', '😴', '💤', '🤔', '💭', '🌟', '✨', '🌅', '☀️', '🌻', '🌙']
            result["emotional_indicators"] = sum(1 for emoji in emotional_indicators if emoji in bot_response)
            
            # Check for expected keywords if provided
            if expected_keywords:
                missing_keywords = []
                for keyword in expected_keywords:
                    if keyword.lower() not in bot_response.lower():
                        missing_keywords.append(keyword)
                
                if missing_keywords:
                    result["missing_keywords"] = missing_keywords
            
            return result
        else:
            return {"status": "❌ FAIL", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌ ERROR", "error": str(e)}

def main():
    print("🧠 EMOTIONAL INTELLIGENCE & CONVERSATIONAL TEST SUITE")
    print("=" * 65)
    
    test_cases = [
        # Basic conversational
        ("how are you?", "How Are You Check-in", ["feeling", "doing"]),
        ("how are you doing?", "How Are You Variant", ["doing", "day"]),
        ("what's up?", "Casual What's Up", ["up", "help"]),
        ("whats the matter?", "What's The Matter", ["matter", "wrong"]),
        ("everything okay?", "Everything OK Check", ["okay", "alright"]),
        
        # Time-based greetings
        ("good morning!", "Good Morning Greeting", ["morning", "day"]),
        ("good afternoon", "Good Afternoon", ["afternoon"]),
        ("good evening", "Good Evening", ["evening"]),
        ("good night", "Good Night", ["night", "sleep"]),
        ("going to bed", "Bedtime", ["sleep", "rest"]),
        
        # Emotional states - Positive
        ("I am so happy today!", "Happy Emotion", ["happy", "wonderful"]),
        ("I'm feeling excited!", "Excited Emotion", ["excited", "energy"]),
        ("I'm thrilled about something!", "Thrilled Emotion", ["thrilled", "amazing"]),
        ("Today was fantastic!", "Fantastic Day", ["fantastic", "great"]),
        
        # Emotional states - Negative  
        ("I'm feeling really sad", "Sad Emotion", ["sad", "sorry"]),
        ("I feel so down today", "Down Emotion", ["down", "tough"]),
        ("I'm quite upset about something", "Upset Emotion", ["upset", "bothering"]),
        ("I feel lonely", "Lonely Emotion", ["lonely", "here"]),
        ("I'm crying", "Crying Emotion", ["tears", "difficult"]),
        
        # Stress and anxiety
        ("I'm so stressed out", "Stressed Emotion", ["stressed", "overwhelmed"]),
        ("I feel really anxious", "Anxious Emotion", ["anxious", "worried"]),
        ("I'm worried about something", "Worried Emotion", ["worried", "mind"]),
        ("I'm having a panic attack", "Panic Emotion", ["panic", "breathe"]),
        ("I feel overwhelmed", "Overwhelmed Emotion", ["overwhelmed", "uncomfortable"]),
        
        # Anger and frustration
        ("I'm so angry right now", "Angry Emotion", ["angry", "frustrated"]),
        ("I'm really frustrated", "Frustrated Emotion", ["frustrated", "bothering"]),
        ("I'm furious about this", "Furious Emotion", ["furious", "angry"]),
        ("This is so annoying", "Annoyed Emotion", ["annoying", "irritated"]),
        
        # Tiredness
        ("I'm so tired", "Tired Emotion", ["tired", "rest"]),
        ("I feel exhausted", "Exhausted Emotion", ["exhausted", "sleep"]),
        ("I'm feeling drained", "Drained Emotion", ["drained", "tired"]),
        ("I'm burnt out", "Burnt Out Emotion", ["burnt", "exhausted"]),
        
        # Confusion
        ("I'm so confused", "Confused Emotion", ["confused", "puzzled"]),
        ("I don't understand", "Don't Understand", ["understand", "clarify"]),
        ("I'm puzzled by this", "Puzzled Emotion", ["puzzled", "confused"]),
        
        # Boredom
        ("I'm so bored", "Bored Emotion", ["bored", "conversation"]),
        ("I have nothing to do", "Nothing To Do", ["nothing", "fun"]),
        ("This is boring", "Boring Situation", ["boring", "interesting"]),
        
        # Life situations
        ("I'm going through a hard time", "Hard Time", ["hard", "challenging"]),
        ("I'm having relationship problems", "Relationship Issues", ["relationship", "complex"]),
        ("Work is really stressful", "Work Stress", ["work", "pressure"]),
        ("I broke up with my boyfriend", "Breakup", ["relationship", "complex"]),
        ("My family is driving me crazy", "Family Issues", ["family", "complicated"]),
    ]
    
    results = []
    passed_tests = 0
    total_tests = len(test_cases)
    
    print(f"🧪 Running {total_tests} emotional intelligence tests...\n")
    
    for i, test_data in enumerate(test_cases, 1):
        message, test_name, expected_keywords = test_data
            
        print(f"[{i:2d}/{total_tests}] 🧪 {test_name}")
        print(f"       📤 Input: '{message}'")
        
        result = test_emotional_scenario(message, test_name, expected_keywords)
        results.append((test_name, result))
        
        if result['status'] == "✅ PASS":
            passed_tests += 1
            emoji_count = result.get('emotional_indicators', 0)
            print(f"       {result['status']} ({result['response_length']} chars, {emoji_count} emojis)")
            if 'missing_keywords' in result:
                print(f"       ⚠️  Missing keywords: {result.get('missing_keywords', [])}")
        else:
            print(f"       {result['status']}")
            if 'error' in result:
                print(f"       💥 Error: {result['error']}")
        
        print()
        time.sleep(0.5)  # Brief pause between tests
    
    # Final Results
    print("=" * 65)
    print("📊 EMOTIONAL INTELLIGENCE RESULTS SUMMARY")
    print("=" * 65)
    
    success_rate = (passed_tests / total_tests * 100)
    
    print(f"🎯 **TOTAL TESTS**: {total_tests}")
    print(f"✅ **PASSED**: {passed_tests}")
    print(f"❌ **FAILED**: {total_tests - passed_tests}")
    print(f"📈 **SUCCESS RATE**: {success_rate:.1f}%")
    
    # Count emotional responses
    emotional_responses = sum(1 for _, result in results if result.get('emotional_indicators', 0) > 0)
    print(f"😊 **EMOTIONAL RESPONSES**: {emotional_responses}/{total_tests} ({emotional_responses/total_tests*100:.1f}%)")
    
    if success_rate == 100:
        print("\n🏆 **PERFECT EMOTIONAL INTELLIGENCE!**")
        print("🎉 CHATBOT IS FULLY EMOTIONALLY AWARE AND CONVERSATIONAL!")
    elif success_rate >= 90:
        print("\n🥇 **EXCELLENT EMOTIONAL INTELLIGENCE!**")
        print("👍 Chatbot shows strong emotional awareness!")
    elif success_rate >= 75:
        print("\n🥈 **GOOD EMOTIONAL INTELLIGENCE**")
        print("👌 Most emotional scenarios handled well!")
    else:
        print("\n⚠️  **EMOTIONAL INTELLIGENCE NEEDS IMPROVEMENT**")
        print("🔧 Several emotional scenarios need attention.")
    
    print("\n" + "=" * 65)

if __name__ == "__main__":
    main()
