#!/usr/bin/env python3
"""
Human Interaction Training Script for Clang AI
This script helps optimize your chatbot for more human-like interactions
"""

import sys
import os
import asyncio
from typing import Dict, List, Any
import json
from datetime import datetime

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot_app.enhanced_clang_service import enhanced_clang, get_clang_response
    from chatbot_app.conversation_memory import ConversationMemory
    from chatbot_app.human_interaction import interaction_optimizer
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

class HumanInteractionTrainer:
    def __init__(self):
        self.memory = ConversationMemory()
        self.training_data = []
        self.optimization_suggestions = []
    
    def load_conversation_data(self, file_path: str = None) -> List[Dict]:
        """Load conversation data for training"""
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading file {file_path}: {e}")
        
        # Sample training data for demonstration
        return [
            {
                "user_message": "I'm feeling really frustrated with my code not working",
                "bot_response": "I understand this can be frustrating. Let me help you debug this step by step.",
                "feedback": {"rating": 5, "response_style": "empathetic", "helpful": True}
            },
            {
                "user_message": "Can you explain recursion?",
                "bot_response": "Great question! Recursion is like a function calling itself. Think of it like looking into two mirrors facing each other - you see infinite reflections.",
                "feedback": {"rating": 4, "response_style": "analogical", "clear": True}
            },
            {
                "user_message": "What's the weather like?",
                "bot_response": "I don't have access to current weather data, but I can help you understand weather patterns or suggest ways to check the weather!",
                "feedback": {"rating": 3, "response_style": "helpful_redirect", "honest": True}
            },
            {
                "user_message": "I'm confused about machine learning",
                "bot_response": "No worries, let me break this down for you! Machine learning is basically teaching computers to learn patterns from data, kind of like how you learn to recognize faces.",
                "feedback": {"rating": 5, "response_style": "simplified", "encouraging": True}
            }
        ]
    
    def analyze_interaction_patterns(self, conversations: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in successful interactions"""
        successful_patterns = []
        failed_patterns = []
        
        for conv in conversations:
            rating = conv.get('feedback', {}).get('rating', 0)
            if rating >= 4:
                successful_patterns.append({
                    'style': conv.get('feedback', {}).get('response_style'),
                    'user_emotion': interaction_optimizer.analyze_user_emotion(conv['user_message']),
                    'response_length': len(conv['bot_response']),
                    'has_empathy': any(word in conv['bot_response'].lower() 
                                     for word in ['understand', 'feel', 'frustrating', 'challenging']),
                    'has_encouragement': any(word in conv['bot_response'].lower() 
                                           for word in ['great', 'excellent', 'good job', 'keep going']),
                    'uses_analogies': any(word in conv['bot_response'].lower() 
                                        for word in ['like', 'similar to', 'think of it as', 'imagine'])
                })
            else:
                failed_patterns.append(conv)
        
        return {
            'successful_patterns': successful_patterns,
            'failed_patterns': failed_patterns,
            'success_rate': len(successful_patterns) / len(conversations) if conversations else 0
        }
    
    def generate_personality_recommendations(self, patterns: Dict) -> List[str]:
        """Generate recommendations for personality adjustments"""
        recommendations = []
        successful = patterns['successful_patterns']
        
        if not successful:
            return ["Need more training data to generate recommendations"]
        
        # Analyze empathy usage
        empathy_usage = sum(1 for p in successful if p['has_empathy']) / len(successful)
        if empathy_usage > 0.7:
            recommendations.append("✅ Increase empathy responses - users respond well to understanding")
        
        # Analyze encouragement
        encouragement_usage = sum(1 for p in successful if p['has_encouragement']) / len(successful)
        if encouragement_usage > 0.6:
            recommendations.append("✅ Use more encouraging language - boosts user confidence")
        
        # Analyze analogies
        analogy_usage = sum(1 for p in successful if p['uses_analogies']) / len(successful)
        if analogy_usage > 0.5:
            recommendations.append("✅ Include more analogies and metaphors - helps understanding")
        
        # Analyze response length
        avg_length = sum(p['response_length'] for p in successful) / len(successful)
        if avg_length > 100:
            recommendations.append(f"📏 Optimal response length: {int(avg_length)} characters")
        
        return recommendations
    
    def optimize_personality_settings(self, patterns: Dict) -> Dict[str, float]:
        """Suggest optimal personality settings based on successful patterns"""
        successful = patterns['successful_patterns']
        
        if not successful:
            return interaction_optimizer.personality.copy()
        
        # Calculate optimal settings
        empathy_score = sum(1 for p in successful if p['has_empathy']) / len(successful)
        encouragement_score = sum(1 for p in successful if p['has_encouragement']) / len(successful)
        analogy_score = sum(1 for p in successful if p['uses_analogies']) / len(successful)
        
        return {
            'friendliness': min(0.9, 0.7 + encouragement_score * 0.2),
            'formality': max(0.3, 0.6 - empathy_score * 0.2),  # Less formal when more empathetic
            'enthusiasm': min(0.9, 0.6 + encouragement_score * 0.3),
            'empathy': min(1.0, 0.8 + empathy_score * 0.2),
            'humor': min(0.8, 0.4 + analogy_score * 0.3)  # Analogies often involve humor
        }
    
    async def test_optimizations(self, test_queries: List[str], user_id: str = "test_user") -> Dict:
        """Test the optimized settings with sample queries"""
        results = {}
        
        for query in test_queries:
            print(f"\n🧪 Testing: {query}")
            
            try:
                response = await get_clang_response(query, user_id=user_id)
                
                # Analyze the response
                emotion_analysis = interaction_optimizer.analyze_user_emotion(query)
                
                results[query] = {
                    'response': response['response'][:200] + "..." if len(response['response']) > 200 else response['response'],
                    'user_emotion': emotion_analysis['primary_emotion'],
                    'response_time': response['metadata']['processing_time_seconds'],
                    'human_optimized': 'interaction_optimizer' in str(response)
                }
                
                print(f"   💬 Response: {results[query]['response']}")
                print(f"   😊 Detected emotion: {emotion_analysis['primary_emotion']}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results[query] = {'error': str(e)}
        
        return results
    
    def save_training_results(self, results: Dict, filename: str = None):
        """Save training results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"✅ Training results saved to {filename}")
        except Exception as e:
            print(f"⚠️ Error saving results: {e}")

async def main():
    """Main training workflow"""
    print("🚀 Starting Human Interaction Training for Clang AI")
    print("=" * 60)
    
    trainer = HumanInteractionTrainer()
    
    # Step 1: Load conversation data
    print("\n📊 Step 1: Loading conversation data...")
    conversations = trainer.load_conversation_data()
    print(f"   Loaded {len(conversations)} conversation examples")
    
    # Step 2: Analyze patterns
    print("\n🔍 Step 2: Analyzing interaction patterns...")
    patterns = trainer.analyze_interaction_patterns(conversations)
    success_rate = patterns['success_rate'] * 100
    print(f"   Success rate: {success_rate:.1f}%")
    print(f"   Successful patterns: {len(patterns['successful_patterns'])}")
    print(f"   Failed patterns: {len(patterns['failed_patterns'])}")
    
    # Step 3: Generate recommendations
    print("\n💡 Step 3: Generating personality recommendations...")
    recommendations = trainer.generate_personality_recommendations(patterns)
    for rec in recommendations:
        print(f"   {rec}")
    
    # Step 4: Optimize personality settings
    print("\n⚙️ Step 4: Optimizing personality settings...")
    optimal_settings = trainer.optimize_personality_settings(patterns)
    print("   Optimal personality settings:")
    for setting, value in optimal_settings.items():
        current_value = interaction_optimizer.personality.get(setting, 0.5)
        change = "📈" if value > current_value else "📉" if value < current_value else "➡️"
        print(f"     {setting}: {current_value:.2f} → {value:.2f} {change}")
    
    # Step 5: Apply optimizations
    print("\n🔧 Step 5: Applying optimizations...")
    for setting, value in optimal_settings.items():
        interaction_optimizer.personality[setting] = value
    print("   ✅ Personality settings updated")
    
    # Step 6: Test with sample queries
    print("\n🧪 Step 6: Testing optimized responses...")
    test_queries = [
        "I'm really confused about this programming concept",
        "This is frustrating, nothing works!",
        "Can you help me with machine learning?",
        "I'm excited to learn more about AI!",
        "What's the best way to study algorithms?"
    ]
    
    test_results = await trainer.test_optimizations(test_queries)
    
    # Step 7: Train from conversations
    print("\n🎓 Step 7: Training from conversation data...")
    enhanced_clang.train_from_conversation("training_user", conversations)
    
    # Step 8: Save results
    print("\n💾 Step 8: Saving training results...")
    training_results = {
        'patterns': patterns,
        'recommendations': recommendations,
        'optimal_settings': optimal_settings,
        'test_results': test_results,
        'timestamp': datetime.now().isoformat()
    }
    trainer.save_training_results(training_results)
    
    print("\n🎉 Training completed successfully!")
    print("\n📋 Summary:")
    print(f"   • Success rate: {success_rate:.1f}%")
    print(f"   • Recommendations generated: {len(recommendations)}")
    print(f"   • Personality settings optimized")
    print(f"   • Test queries processed: {len(test_queries)}")
    
    print("\n🔄 Next steps to improve human interaction:")
    print("   1. Collect more conversation data from real users")
    print("   2. Implement user feedback collection in your UI")
    print("   3. Run this training script regularly with new data")
    print("   4. Fine-tune personality settings based on user preferences")
    print("   5. Monitor conversation quality metrics")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
