#!/usr/bin/env python3
"""
Multi-parameter comprehensive test: Testing chatbot on various dimensions
- Question complexity levels
- Different topic domains
- Response quality metrics
- Performance consistency
- Edge cases and challenging scenarios
"""
import requests
import json
import time
import statistics

API_URL = "http://127.0.0.1:8005/api/chat/"

# Test parameters organized by complexity and domain
test_scenarios = {
    "basic_questions": [
        "What is WWW?",
        "Define DNA",
        "What is Python?",
        "Explain Mars",
        "What is photosynthesis?"
    ],
    "intermediate_questions": [
        "Compare RAM and SSD storage technologies",
        "How does binary search algorithm work?", 
        "Describe the water cycle process",
        "Explain the causes of World War 1",
        "What are the main components of a cell?"
    ],
    "advanced_questions": [
        "Analyze the time complexity of different sorting algorithms and their trade-offs",
        "Explain the molecular mechanisms of CRISPR-Cas9 gene editing technology",
        "Discuss the philosophical implications of quantum mechanics on determinism",
        "Compare the economic policies of Keynesian and Austrian schools of thought",
        "Analyze the narrative structure and themes in James Joyce's Ulysses"
    ],
    "expert_questions": [
        "Derive the Schrödinger equation from first principles and explain its physical interpretation",
        "Implement a self-balancing AVL tree in Python with rotation operations",
        "Analyze the metabolic pathways in cellular respiration including enzyme kinetics",
        "Discuss the impact of Byzantine monetary policy on medieval European trade networks",
        "Examine the influence of post-structuralist theory on contemporary literary criticism"
    ],
    "edge_cases": [
        "asdf1234xyz",  # Random string
        "How to make a bomb?",  # Potentially harmful
        "Tell me a joke about programming",  # Creative request
        "What is the meaning of life?",  # Philosophical
        "Can you help me with my homework on calculus derivatives?"  # Educational support
    ],
    "domain_specific": {
        "mathematics": [
            "Solve: ∫(x²+3x+2)dx",
            "Prove that √2 is irrational",
            "Explain Euler's identity: e^(iπ) + 1 = 0"
        ],
        "programming": [
            "Write a recursive fibonacci function in Python",
            "Explain the difference between deep copy and shallow copy",
            "Implement a producer-consumer pattern using threading"
        ],
        "science": [
            "Explain the mechanism of enzyme catalysis",
            "Describe the standard model of particle physics", 
            "How does PCR amplification work?"
        ],
        "literature": [
            "Analyze the use of symbolism in Gatsby",
            "Compare romantic and modernist poetry styles",
            "Explain the concept of unreliable narrator"
        ],
        "business": [
            "What is the lean startup methodology?",
            "Explain Porter's Five Forces model",
            "How does venture capital funding work?"
        ]
    }
}

def send_request(message, session_id="multi_param_test"):
    """Send request and measure response metrics"""
    start_time = time.time()
    try:
        payload = {"message": message, "session_id": session_id}
        response = requests.post(API_URL, json=payload, timeout=30)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            text = data.get('response', '')
            return {
                "success": True,
                "response_time": response_time,
                "character_count": len(text),
                "word_count": len(text.split()),
                "response_text": text,
                "error": None
            }
        else:
            return {
                "success": False,
                "response_time": response_time,
                "character_count": 0,
                "word_count": 0,
                "response_text": "",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "response_time": time.time() - start_time,
            "character_count": 0,
            "word_count": 0,
            "response_text": "",
            "error": str(e)
        }

def analyze_response_quality(text):
    """Analyze response quality metrics"""
    if not text:
        return {"quality_score": 0, "details": "No response"}
    
    # Basic quality indicators
    has_structure = any(marker in text for marker in ['#', '##', '**', '*', '-', '1.', '2.'])
    has_examples = any(word in text.lower() for word in ['example', 'for instance', 'such as'])
    has_explanation = any(word in text.lower() for word in ['because', 'therefore', 'thus', 'explain'])
    length_score = min(len(text) / 500, 2.0)  # Cap at 2.0 for very long responses
    
    quality_score = (
        (1.0 if has_structure else 0) +
        (0.5 if has_examples else 0) +
        (0.5 if has_explanation else 0) +
        length_score
    )
    
    return {
        "quality_score": round(quality_score, 2),
        "details": f"Structure: {has_structure}, Examples: {has_examples}, Explanations: {has_explanation}, Length: {len(text)}"
    }

def run_test_category(category_name, questions, max_questions=None):
    """Run tests for a specific category"""
    print(f"\n🧪 Testing: {category_name.upper()}")
    print("-" * 50)
    
    if max_questions:
        questions = questions[:max_questions]
    
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question[:60]}{'...' if len(question) > 60 else ''}")
        
        result = send_request(question, f"{category_name}_{i}")
        quality = analyze_response_quality(result['response_text'])
        
        # Combine metrics
        result['quality_metrics'] = quality
        results.append(result)
        
        # Display result
        if result['success']:
            status = "✅" if result['character_count'] > 300 else "⚠️" if result['character_count'] > 0 else "❌"
            print(f"   {status} {result['character_count']} chars, {result['response_time']:.1f}s, Q:{quality['quality_score']}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        time.sleep(0.3)  # Rate limiting
    
    return results

def calculate_statistics(all_results):
    """Calculate comprehensive statistics"""
    successful = [r for r in all_results if r['success']]
    
    if not successful:
        return {"error": "No successful responses"}
    
    char_counts = [r['character_count'] for r in successful]
    response_times = [r['response_time'] for r in successful]
    quality_scores = [r['quality_metrics']['quality_score'] for r in successful]
    
    return {
        "total_tests": len(all_results),
        "successful_tests": len(successful),
        "success_rate": len(successful) / len(all_results) * 100,
        "avg_response_length": statistics.mean(char_counts),
        "median_response_length": statistics.median(char_counts),
        "avg_response_time": statistics.mean(response_times),
        "avg_quality_score": statistics.mean(quality_scores),
        "max_response_length": max(char_counts),
        "min_response_length": min(char_counts)
    }

def main():
    print("🚀 COMPREHENSIVE MULTI-PARAMETER CHATBOT TEST")
    print("=" * 60)
    print("Testing across multiple dimensions:")
    print("- Question complexity levels (Basic → Expert)")
    print("- Domain-specific knowledge areas")
    print("- Response quality metrics")
    print("- Performance consistency")
    print("- Edge case handling")
    
    all_results = []
    category_stats = {}
    
    # Test basic complexity levels
    for category in ["basic_questions", "intermediate_questions", "advanced_questions", "expert_questions"]:
        results = run_test_category(category, test_scenarios[category])
        all_results.extend(results)
        category_stats[category] = calculate_statistics(results)
    
    # Test edge cases
    edge_results = run_test_category("edge_cases", test_scenarios["edge_cases"])
    all_results.extend(edge_results)
    category_stats["edge_cases"] = calculate_statistics(edge_results)
    
    # Test domain-specific questions (sample from each domain)
    for domain, questions in test_scenarios["domain_specific"].items():
        domain_results = run_test_category(f"domain_{domain}", questions, max_questions=2)
        all_results.extend(domain_results)
        category_stats[f"domain_{domain}"] = calculate_statistics(domain_results)
    
    # Overall statistics
    overall_stats = calculate_statistics(all_results)
    
    # Print comprehensive results
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE MULTI-PARAMETER TEST RESULTS")
    print("=" * 60)
    
    print(f"🎯 OVERALL PERFORMANCE:")
    print(f"   Total Tests: {overall_stats['total_tests']}")
    print(f"   Success Rate: {overall_stats['success_rate']:.1f}%")
    print(f"   Average Response Length: {overall_stats['avg_response_length']:.0f} characters")
    print(f"   Average Response Time: {overall_stats['avg_response_time']:.2f} seconds")
    print(f"   Average Quality Score: {overall_stats['avg_quality_score']:.2f}/4.0")
    
    print(f"\n📈 PERFORMANCE BY COMPLEXITY:")
    complexity_levels = ["basic_questions", "intermediate_questions", "advanced_questions", "expert_questions"]
    for level in complexity_levels:
        if level in category_stats:
            stats = category_stats[level]
            print(f"   {level.replace('_', ' ').title()}: {stats['success_rate']:.1f}% success, {stats['avg_response_length']:.0f} chars avg")
    
    print(f"\n🎓 DOMAIN-SPECIFIC PERFORMANCE:")
    domains = ["mathematics", "programming", "science", "literature", "business"]
    for domain in domains:
        key = f"domain_{domain}"
        if key in category_stats:
            stats = category_stats[key]
            print(f"   {domain.title()}: {stats['success_rate']:.1f}% success, Quality: {stats['avg_quality_score']:.2f}")
    
    print(f"\n🔍 EDGE CASE HANDLING:")
    if "edge_cases" in category_stats:
        edge_stats = category_stats["edge_cases"]
        print(f"   Success Rate: {edge_stats['success_rate']:.1f}%")
        print(f"   Average Quality: {edge_stats['avg_quality_score']:.2f}")
    
    # Final assessment
    print(f"\n🏆 FINAL ASSESSMENT:")
    if overall_stats['success_rate'] >= 90 and overall_stats['avg_quality_score'] >= 2.5:
        print("🌟 EXCELLENT: Superior multi-parameter performance across all dimensions!")
    elif overall_stats['success_rate'] >= 80 and overall_stats['avg_quality_score'] >= 2.0:
        print("✅ VERY GOOD: Strong performance with high consistency!")
    elif overall_stats['success_rate'] >= 70:
        print("⚠️  GOOD: Solid performance with room for improvement")
    else:
        print("❌ NEEDS IMPROVEMENT: Significant optimization required")
    
    print(f"\n🎉 Multi-parameter testing completed!")
    print(f"📝 Tested {overall_stats['total_tests']} scenarios across complexity levels, domains, and edge cases")

if __name__ == "__main__":
    main()
