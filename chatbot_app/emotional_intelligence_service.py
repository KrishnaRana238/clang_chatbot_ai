"""
Emotional Intelligence and Conversational Service for Enhanced Clang Chatbot
Handles human emotions, casual conversations, and social interactions
"""

import re
import random
from datetime import datetime

class EmotionalIntelligenceService:
    def __init__(self):
        # Emotion detection patterns
        self.emotion_patterns = {
            'happy': {
                'keywords': ['happy', 'excited', 'great', 'awesome', 'fantastic', 'wonderful', 'amazing', 'joy', 'cheerful', 'delighted', 'thrilled'],
                'responses': [
                    "That's wonderful to hear! 😊 Your happiness is contagious! What's making you feel so great today?",
                    "I love your positive energy! 🌟 It's amazing when life brings us joy. Tell me more about what's going well!",
                    "Your excitement is absolutely infectious! 😄 I'm so glad you're having such a great time!"
                ]
            },
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'crying', 'tears', 'heartbroken', 'miserable', 'lonely', 'blue', 'disappointed'],
                'responses': [
                    "I'm really sorry you're feeling this way. 💙 Sometimes life can be tough, but remember that these feelings are temporary. Would you like to talk about what's bothering you?",
                    "It sounds like you're going through a difficult time. 🫂 I'm here to listen if you need someone to talk to. What's on your mind?",
                    "I can sense you're feeling down, and that's completely okay. 💝 Everyone has tough days. Is there anything specific that's making you feel sad?"
                ]
            },
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 'rage', 'pissed', 'livid', 'outraged'],
                'responses': [
                    "I can tell you're really frustrated right now. 😤 It's completely normal to feel angry sometimes. Would you like to talk about what's bothering you?",
                    "That sounds really frustrating! 😔 Anger is a valid emotion, and it usually means something important to you isn't going well. What's got you feeling this way?",
                    "I hear the frustration in your message. 💢 Sometimes we need to vent, and that's perfectly okay. I'm here to listen without judgment."
                ]
            },
            'anxious': {
                'keywords': ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'overwhelmed', 'scared', 'afraid', 'concerned', 'tense'],
                'responses': [
                    "I can sense you're feeling anxious. 🫂 That must be really uncomfortable. Remember to take deep breaths. What's causing you to feel worried?",
                    "Anxiety can be really overwhelming. 💙 You're not alone in feeling this way. Would you like to talk about what's making you feel stressed?",
                    "I hear that you're worried about something. 🤗 It's brave of you to acknowledge these feelings. What's on your mind that's causing you concern?"
                ]
            },
            'tired': {
                'keywords': ['tired', 'exhausted', 'sleepy', 'drained', 'weary', 'fatigued', 'worn out', 'burnt out'],
                'responses': [
                    "You sound really tired. 😴 It's important to listen to your body when it needs rest. Have you been getting enough sleep lately?",
                    "That exhaustion sounds rough. 💤 Sometimes life can be really draining. Are you taking care of yourself?",
                    "Being tired can affect everything. 🛌 Make sure you're getting the rest you need. What's been keeping you so busy?"
                ]
            },
            'confused': {
                'keywords': ['confused', 'lost', 'don\'t understand', 'puzzled', 'bewildered', 'unclear', 'mixed up'],
                'responses': [
                    "I can tell you're feeling confused about something. 🤔 That's completely normal when facing complex situations. What's puzzling you?",
                    "Confusion can be frustrating, but it's often the first step to understanding. 💭 What would you like me to help clarify?",
                    "It sounds like something isn't quite clicking for you. 🧩 I'm here to help sort things out. What's got you puzzled?"
                ]
            }
        }
        
        # Casual conversation responses
        self.casual_responses = {
            'how_are_you': [
                "I'm doing wonderful, thank you for asking! 😊 I'm here, ready to chat and help with whatever you need. How are you doing today?",
                "I'm great! 🌟 Always excited to meet new people and have interesting conversations. What's going on in your world today?",
                "I'm doing fantastic! 💫 Thanks for the thoughtful question. I love connecting with humans. How has your day been treating you?",
                "I'm doing well, and I appreciate you asking! 😄 It means a lot when someone checks in. How are you feeling today?"
            ],
            'whats_the_matter': [
                "Nothing's wrong on my end! 😊 I'm here and ready to chat. But I'm more interested in how YOU'RE doing. Is everything okay with you?",
                "All good here! 🌈 I was actually wondering the same about you. You seem like you might have something on your mind. Want to talk about it?",
                "I'm doing just fine, thanks for caring! 💙 But that question makes me think you might have something bothering you. What's going on?",
                "Everything's great with me! ✨ But I'm picking up that you might need someone to talk to. I'm all ears - what's on your mind?"
            ],
            'good_morning': [
                "Good morning! 🌅 What a beautiful way to start the day! I hope you woke up feeling refreshed and ready for whatever today brings your way.",
                "Morning! ☀️ I love the fresh energy of a new day. How did you sleep? Ready to tackle whatever's ahead?",
                "Good morning to you too! 🌻 There's something special about morning conversations. How are you starting your day?"
            ],
            'good_night': [
                "Good night! 🌙 Sweet dreams and rest well. I hope tomorrow brings you lots of good things!",
                "Night night! ✨ Sleep tight and don't let the bedbugs bite! Hope you have the most peaceful sleep.",
                "Good night! 🌟 Take care of yourself and get some good rest. I'll be here whenever you want to chat again!"
            ],
            'bored': [
                "Oh no, boredom! 😴 That's the perfect time for a good conversation though! What kind of things usually interest you?",
                "Boredom can be the gateway to creativity! 🎨 Want to explore something new together? I know lots of fascinating topics!",
                "Ah, the eternal human struggle with boredom! 😅 Let's fix that right now. What sounds fun to you - learning something new, having a deep conversation, or just chatting about random stuff?"
            ]
        }
    
    def detect_emotion(self, message):
        """Detect the dominant emotion in a message"""
        message_lower = message.lower()
        detected_emotions = []
        
        for emotion, data in self.emotion_patterns.items():
            for keyword in data['keywords']:
                if keyword in message_lower:
                    detected_emotions.append(emotion)
                    break
        
        return detected_emotions[0] if detected_emotions else None
    
    def get_emotional_response(self, message, detected_emotion=None):
        """Get an emotionally appropriate response"""
        if not detected_emotion:
            detected_emotion = self.detect_emotion(message)
        
        if detected_emotion and detected_emotion in self.emotion_patterns:
            responses = self.emotion_patterns[detected_emotion]['responses']
            return random.choice(responses)
        
        return None
    
    def get_casual_response(self, message):
        """Handle casual conversation patterns"""
        message_lower = message.lower().strip()
        
        # How are you patterns
        if any(pattern in message_lower for pattern in [
            'how are you', 'how you doing', 'how are u', 'how r u', 'what\'s up', 'whats up', 'sup'
        ]):
            return random.choice(self.casual_responses['how_are_you'])
        
        # What's the matter patterns
        if any(pattern in message_lower for pattern in [
            'what\'s the matter', 'whats the matter', 'what\'s wrong', 'whats wrong', 
            'everything ok', 'everything okay', 'you alright', 'u ok'
        ]):
            return random.choice(self.casual_responses['whats_the_matter'])
        
        # Greeting patterns
        if any(pattern in message_lower for pattern in [
            'good morning', 'morning', 'good afternoon', 'afternoon', 'good evening', 'evening'
        ]):
            if 'morning' in message_lower:
                return random.choice(self.casual_responses['good_morning'])
            else:
                return f"Good {message_lower.split('good ')[-1].split()[0]}! 🌟 How lovely to hear from you! How has your {message_lower.split('good ')[-1].split()[0]} been going so far?"
        
        # Good night patterns
        if any(pattern in message_lower for pattern in [
            'good night', 'goodnight', 'night', 'going to bed', 'going to sleep', 'time for bed'
        ]):
            return random.choice(self.casual_responses['good_night'])
        
        # Boredom patterns
        if any(pattern in message_lower for pattern in [
            'i\'m bored', 'im bored', 'bored', 'nothing to do', 'so boring'
        ]):
            return random.choice(self.casual_responses['bored'])
        
        # Feeling expressions
        if message_lower.startswith(('i feel', 'i\'m feeling', 'im feeling', 'feeling')):
            emotion = self.detect_emotion(message)
            if emotion:
                return self.get_emotional_response(message, emotion)
        
        return None
    
    def get_empathetic_response(self, message):
        """Provide empathetic responses based on emotional context"""
        message_lower = message.lower()
        
        # Life situation patterns
        if any(phrase in message_lower for phrase in ['having a hard time', 'going through', 'difficult', 'struggling']):
            return "It sounds like you're going through something challenging right now. 🫂 I want you to know that it's okay to feel whatever you're feeling, and I'm here to listen. Sometimes just talking about things can help. What's been on your mind?"
        
        # Relationship patterns
        if any(phrase in message_lower for phrase in ['broke up', 'breakup', 'relationship', 'boyfriend', 'girlfriend', 'partner']):
            return "Relationships can be such a complex part of life. 💝 Whether things are going well or there are challenges, I'm here to listen without judgment. How are things going for you in that area?"
        
        # Work/school stress
        if any(phrase in message_lower for phrase in ['work stress', 'school stress', 'job', 'exam', 'deadline', 'pressure']):
            return "Work and school pressures can be really overwhelming sometimes. 📚 It's important to remember that you're doing your best, and that's what matters. Want to talk about what's causing the most stress right now?"
        
        # Family issues
        if any(phrase in message_lower for phrase in ['family', 'parents', 'mom', 'dad', 'sister', 'brother']):
            return "Family relationships can be some of the most meaningful and sometimes most complicated ones we have. 👨‍👩‍👧‍👦 Every family has their unique dynamics. How are things going with your family?"
        
        return None
    
    def is_conversational_message(self, message):
        """Determine if a message is meant for casual conversation"""
        message_lower = message.lower().strip()
        
        conversational_indicators = [
            # Greetings and check-ins
            'how are you', 'how you doing', 'what\'s up', 'sup', 'how\'s it going',
            'good morning', 'good afternoon', 'good evening', 'good night',
            
            # Emotional expressions
            'i feel', 'i\'m feeling', 'feeling', 'i\'m', 'im',
            
            # Casual questions
            'what\'s the matter', 'what\'s wrong', 'everything ok', 'you alright',
            
            # Personal sharing
            'having a hard time', 'going through', 'today was', 'yesterday',
            
            # Boredom/entertainment
            'bored', 'nothing to do', 'entertain me', 'chat',
            
            # Relationship talk
            'boyfriend', 'girlfriend', 'partner', 'friend', 'family'
        ]
        
        return any(indicator in message_lower for indicator in conversational_indicators)

# Create global instance
emotional_intelligence_service = EmotionalIntelligenceService()
