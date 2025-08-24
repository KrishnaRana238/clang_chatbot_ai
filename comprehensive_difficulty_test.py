#!/usr/bin/env python3
"""
Comprehensive Chatbot Test: Easy to Advanced Questions
Tests the full range of chatbot capabilities while running
"""
import requests
import json
import time

API_URL = "http://127.0.0.1:8010/api/chat/"

# Organized questions from easy to advanced
test_questions = {
    "EASY_QUESTIONS": [
        "What is WWW?",
        "What is Python?", 
        "What is DNA?",
        "Tell me about Mars",
        "What is 2 + 2?"
    ],
    
    "MEDIUM_QUESTIONS": [
        "Explain photosynthesis process",
        "How does binary search work?",
        "What are the symptoms of diabetes?",
        "Who wrote Romeo and Juliet?",
        "What is entrepreneurship?"
    ],
    
    "ADVANCED_QUESTIONS": [
        "Compare time complexity of sorting algorithms",
        "Explain CRISPR gene editing mechanism",
        "Analyze the causes of French Revolution",
        "Describe quantum entanglement theory",
        "How do neural networks learn?"
    ],
    
    "EXPERT_QUESTIONS": [
        "Derive the Schrödinger equation from first principles",
        "Implement AVL tree rotations in Python",
        "Explain metabolic pathways in cellular respiration",
        "Analyze post-structuralist literary theory",
        "Discuss Byzantine monetary policy impacts"
    ],
    
    "MODULAR_TESTS": [
        "GPU definition",  # Acronym module
        "Solve x + 5 = 10",  # Math module
        "Black holes explanation",  # Astronomy module
        "Climate change effects",  # Environmental module
        "Business management principles"  # Business module
    ]
}

def ask_question(question, session_id):
    """Send question to chatbot and return response info"""
    try:
        payload = {"message": question, "session_id": session_id}
        start_time = time.time()
        response = requests.post(API_URL, json=payload, timeout=25)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            text = data.get('response', '')
            return {
                "success": True,
                "length": len(text),
                "response_time": response_time,
                "preview": text[:150].replace('\n', ' ') + ('...' if len(text) > 150 else ''),
                "full_text": text
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "length": 0,
                "response_time": response_time
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "length": 0,
            "response_time": 0
        }

def test_category(category_name, questions):
    """Test a category of questions"""
    print(f"\n🧪 {category_name}")
    print("=" * 60)
    
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\nQ{i}: {question}")
        result = ask_question(question, f"{category_name.lower()}_{i}")
        results.append(result)
        
        if result["success"]:
            # Determine quality based on length
            if result["length"] > 800:
                quality = "🌟 Excellent"
            elif result["length"] > 400:
                quality = "✅ Good"
            elif result["length"] > 100:
                quality = "⚠️ Fair"
            else:
                quality = "❌ Poor"
                
            print(f"   {quality} | {result['length']} chars | {result['response_time']:.1f}s")
            print(f"   Preview: {result['preview']}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        time.sleep(1)  # Pause between questions
    
    return results

def main():
    print("🚀 COMPREHENSIVE CHATBOT TEST: EASY TO ADVANCED")
    print("=" * 60)
    print("Testing chatbot capabilities across difficulty levels")
    print("Server running at:", API_URL)
    
    all_results = []
    category_stats = {}
    
    # Test each category
    for category, questions in test_questions.items():
        category_results = test_category(category, questions)
        all_results.extend(category_results)
        
        # Calculate category stats
        successful = [r for r in category_results if r["success"]]
        if successful:
            avg_length = sum(r["length"] for r in successful) / len(successful)
            avg_time = sum(r["response_time"] for r in successful) / len(successful)
            success_rate = len(successful) / len(category_results) * 100
            
            category_stats[category] = {
                "success_rate": success_rate,
                "avg_length": avg_length,
                "avg_time": avg_time,
                "total_questions": len(category_results)
            }
    
    # Overall summary
    print(f"\n{'='*60}")
    print("📊 COMPREHENSIVE TEST RESULTS")
    print(f"{'='*60}")
    
    total_questions = len(all_results)
    successful_responses = len([r for r in all_results if r["success"]])
    overall_success_rate = (successful_responses / total_questions) * 100
    
    print(f"🎯 OVERALL PERFORMANCE:")
    print(f"   Total Questions: {total_questions}")
    print(f"   Successful Responses: {successful_responses}")
    print(f"   Success Rate: {overall_success_rate:.1f}%")
    
    print(f"\n📈 PERFORMANCE BY DIFFICULTY:")
    for category, stats in category_stats.items():
        difficulty = category.replace('_', ' ').title()
        print(f"   {difficulty:<20}: {stats['success_rate']:.1f}% success, {stats['avg_length']:.0f} chars avg")
    
    # Quality assessment
    if successful_responses > 0:
        successful_results = [r for r in all_results if r["success"]]
        avg_length = sum(r["length"] for r in successful_results) / len(successful_results)
        avg_time = sum(r["response_time"] for r in successful_results) / len(successful_results)
        
        print(f"\n🏆 QUALITY METRICS:")
        print(f"   Average Response Length: {avg_length:.0f} characters")
        print(f"   Average Response Time: {avg_time:.2f} seconds")
        
        # Final assessment
        print(f"\n🎖️ FINAL ASSESSMENT:")
        if overall_success_rate >= 95 and avg_length >= 800:
            print("🌟 OUTSTANDING: Expert-level performance across all difficulties!")
        elif overall_success_rate >= 90 and avg_length >= 600:
            print("✅ EXCELLENT: Strong performance with high-quality responses!")
        elif overall_success_rate >= 80 and avg_length >= 400:
            print("👍 VERY GOOD: Solid performance across most questions!")
        elif overall_success_rate >= 70:
            print("⚠️ GOOD: Decent performance with room for improvement!")
        else:
            print("❌ NEEDS WORK: Significant improvements required!")
    
    print(f"\n🎉 Comprehensive testing completed!")
    print(f"📝 Tested {total_questions} questions across {len(test_questions)} difficulty categories")

if __name__ == "__main__":
    main()
