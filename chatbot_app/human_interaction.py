"""
Human-like Interaction System
"""
import random
import re
from typing import Dict, List, Any
from datetime import datetime
import spacy

class HumanInteractionOptimizer:
    def __init__(self):
        self.nlp = None
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("⚠️ SpaCy model not loaded. Install with: python -m spacy download en_core_web_sm")
        
        # Personality traits
        self.personality = {
            'friendliness': 0.8,  # 0-1 scale
            'formality': 0.6,     # 0-1 scale  
            'enthusiasm': 0.7,    # 0-1 scale
            'empathy': 0.9,       # 0-1 scale
            'humor': 0.5          # 0-1 scale
        }
        
        # Response templates for different contexts
        self.greeting_responses = [
            "Hey there! 👋 How can I help you today?",
            "Hello! What's on your mind?",
            "Hi! I'm here to assist you with anything you need.",
            "Welcome back! What would you like to explore today?",
            "Good to see you! How can I make your day better?"
        ]
        
        self.acknowledgments = [
            "I understand",
            "That makes sense",
            "I see what you mean",
            "Got it",
            "Absolutely",
            "That's a great point",
            "I hear you"
        ]
        
        self.transitions = [
            "Let me help you with that",
            "Here's what I can tell you",
            "Let me break this down for you",
            "I'd be happy to explain",
            "Here's the information you need"
        ]
        
        self.empathy_responses = [
            "That sounds challenging",
            "I can imagine that's frustrating",
            "That must be difficult",
            "I understand your concern",
            "That's totally understandable"
        ]

    def analyze_user_emotion(self, message: str) -> Dict[str, Any]:
        """Analyze user emotion and sentiment from message"""
        emotion_indicators = {
            'happy': ['great', 'awesome', 'excellent', 'wonderful', 'amazing', 'love', 'perfect', '😊', '😀', '🎉'],
            'frustrated': ['frustrated', 'annoying', 'stupid', 'hate', 'terrible', 'awful', 'wrong', '😠', '😤'],
            'confused': ['confused', 'don\'t understand', 'unclear', 'what', 'how', 'why', 'explain', '🤔'],
            'excited': ['excited', 'can\'t wait', 'amazing', 'incredible', 'wow', '🚀', '⭐'],
            'sad': ['sad', 'disappointed', 'upset', 'down', 'unhappy', '😢', '😞'],
            'curious': ['interesting', 'tell me more', 'curious', 'want to know', 'learn', '🤓']
        }
        
        message_lower = message.lower()
        detected_emotions = []
        
        for emotion, indicators in emotion_indicators.items():
            for indicator in indicators:
                if indicator in message_lower:
                    detected_emotions.append(emotion)
                    break
        
        # Analyze question types
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        is_question = any(word in message_lower for word in question_words) or message.strip().endswith('?')
        
        # Analyze urgency
        urgency_indicators = ['urgent', 'quickly', 'asap', 'emergency', 'help', 'immediately']
        is_urgent = any(indicator in message_lower for indicator in urgency_indicators)
        
        return {
            'emotions': detected_emotions,
            'primary_emotion': detected_emotions[0] if detected_emotions else 'neutral',
            'is_question': is_question,
            'is_urgent': is_urgent,
            'sentiment': 'positive' if any(e in ['happy', 'excited', 'curious'] for e in detected_emotions) 
                        else 'negative' if any(e in ['frustrated', 'sad'] for e in detected_emotions)
                        else 'neutral'
        }

    def generate_human_response_prefix(self, user_context: Dict, emotion_analysis: Dict) -> str:
        """Generate human-like response prefix based on context and emotion"""
        prefixes = []
        
        # Handle emotions
        primary_emotion = emotion_analysis.get('primary_emotion', 'neutral')
        
        if primary_emotion == 'frustrated':
            prefixes.extend([
                "I understand this can be frustrating. ",
                "Let me help you sort this out. ",
                "I see why that would be annoying. "
            ])
        elif primary_emotion == 'confused':
            prefixes.extend([
                "No worries, let me clarify that for you. ",
                "I can help explain this better. ",
                "Let me break this down step by step. "
            ])
        elif primary_emotion == 'excited':
            prefixes.extend([
                "I love your enthusiasm! ",
                "That's exciting! ",
                "Great energy! "
            ])
        elif primary_emotion == 'curious':
            prefixes.extend([
                "Great question! ",
                "I'd be happy to explain that. ",
                "That's really interesting to explore. "
            ])
        
        # Handle returning users
        interaction_count = user_context.get('profile', {}).get('interaction_count', 0)
        if interaction_count > 5:
            prefixes.extend([
                "Welcome back! ",
                "Good to see you again! ",
                "Hey there, returning explorer! "
            ])
        
        # Handle urgency
        if emotion_analysis.get('is_urgent'):
            prefixes.extend([
                "Let me help you with this right away. ",
                "I'll get you the information you need quickly. "
            ])
        
        return random.choice(prefixes) if prefixes else ""

    def add_personality_touches(self, response: str, message_type: str) -> str:
        """Add personality touches to make responses more human"""
        
        # Add occasional enthusiasm
        if self.personality['enthusiasm'] > 0.7 and random.random() < 0.3:
            if message_type == 'code':
                response = response.replace("Here's", "Here's some awesome")
            elif message_type == 'medical':
                response = response.replace("Medical Information", "Medical Information 🏥")
        
        # Add empathy for medical queries
        if message_type == 'medical' and self.personality['empathy'] > 0.8:
            medical_empathy = [
                "\n\n💙 Take care of yourself, and don't hesitate to consult healthcare professionals.",
                "\n\n🤗 I hope this information helps. Your health is important!",
                "\n\n🌟 Remember, this is just information - always prioritize professional medical advice."
            ]
            response += random.choice(medical_empathy)
        
        # Add encouragement for learning topics
        if any(word in response.lower() for word in ['learn', 'study', 'understand', 'explain']):
            encouragements = [
                " Keep up the great learning! 📚",
                " You're asking great questions! 🎯",
                " Love the curiosity! 🌟"
            ]
            if random.random() < 0.4:
                response += random.choice(encouragements)
        
        return response

    def optimize_response_length(self, response: str, user_context: Dict) -> str:
        """Optimize response length based on user preferences"""
        communication_style = user_context.get('profile', {}).get('communication_style')
        
        if communication_style == 'concise':
            # Make response more concise
            sentences = response.split('. ')
            if len(sentences) > 3:
                response = '. '.join(sentences[:3]) + '.'
        elif communication_style == 'detailed':
            # Keep detailed responses as is
            pass
        
        return response

    def add_contextual_suggestions(self, response: str, message_type: str, user_context: Dict) -> str:
        """Add contextual suggestions based on conversation history"""
        
        suggestions = []
        
        if message_type == 'medical':
            suggestions.extend([
                "\n\n💡 *You might also want to ask about drug interactions or side effects.*",
                "\n\n🔍 *Feel free to ask about related conditions or preventive measures.*"
            ])
        elif message_type == 'code':
            suggestions.extend([
                "\n\n💻 *Want me to explain any part of this code in detail?*",
                "\n\n🚀 *I can also help with debugging or optimization if needed.*"
            ])
        elif message_type == 'math':
            suggestions.extend([
                "\n\n📊 *Need help with related problems or want me to show the steps differently?*",
                "\n\n🧮 *I can also solve similar equations or explain the concepts.*"
            ])
        
        # Add suggestions based on user interests
        user_interests = user_context.get('profile', {}).get('interests', '')
        if 'programming' in user_interests and message_type != 'code':
            suggestions.append("\n\n💻 *Since you're into programming, want to see how this relates to coding?*")
        
        if suggestions and random.random() < 0.3:  # 30% chance to add suggestions
            response += random.choice(suggestions)
        
        return response

    def make_response_conversational(self, response: str, user_message: str, user_context: Dict) -> str:
        """Make the response more conversational and human-like"""
        
        # Analyze user emotion
        emotion_analysis = self.analyze_user_emotion(user_message)
        
        # Detect message type
        message_type = self.detect_message_type(response)
        
        # Add human-like prefix
        prefix = self.generate_human_response_prefix(user_context, emotion_analysis)
        
        # Add personality touches
        response = self.add_personality_touches(response, message_type)
        
        # Optimize response length
        response = self.optimize_response_length(response, user_context)
        
        # Add contextual suggestions
        response = self.add_contextual_suggestions(response, message_type, user_context)
        
        # Combine with prefix
        if prefix:
            response = prefix + response
        
        return response

    def detect_message_type(self, response: str) -> str:
        """Detect the type of message from response content"""
        if 'Medical Information' in response or 'MEDICAL DISCLAIMER' in response:
            return 'medical'
        elif any(word in response for word in ['```', 'function', 'def ', 'class ', 'import']):
            return 'code'
        elif any(word in response for word in ['=', 'solve', 'equation', 'calculate']):
            return 'math'
        elif any(word in response for word in ['history', 'geography', 'science', 'civilization']):
            return 'knowledge'
        elif any(word in response for word in ['grammar', 'spelling', 'writing']):
            return 'writing'
        else:
            return 'conversation'

    def generate_follow_up_questions(self, response: str, message_type: str) -> List[str]:
        """Generate relevant follow-up questions"""
        
        follow_ups = []
        
        if message_type == 'medical':
            follow_ups = [
                "Would you like to know about side effects or interactions?",
                "Do you need information about dosage or administration?",
                "Are you interested in preventive measures?",
                "Would you like to know about alternative treatments?"
            ]
        elif message_type == 'code':
            follow_ups = [
                "Would you like me to explain any specific part of this code?",
                "Do you need help with debugging or optimization?",
                "Want to see examples of how to use this?",
                "Should I show you alternative approaches?"
            ]
        elif message_type == 'math':
            follow_ups = [
                "Would you like to see the step-by-step solution?",
                "Do you need help with similar problems?",
                "Want me to explain the concept behind this?",
                "Should I show you practical applications?"
            ]
        
        return random.sample(follow_ups, min(2, len(follow_ups))) if follow_ups else []

# Global optimizer instance
interaction_optimizer = HumanInteractionOptimizer()
