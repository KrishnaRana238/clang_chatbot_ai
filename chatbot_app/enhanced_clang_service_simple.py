"""
Simple Enhanced Clang AI Chatbot Service
Clean, direct responses without complex modules
"""

import os
import asyncio
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Import basic services
try:
    from .knowledge_base_service import (
        knowledge_base, grammar_checker, math_calculator, get_knowledge_response
    )
    from .nlp_processor import nlp_processor, process_user_query
    from .medical_knowledge_service import medical_service, get_medical_information
    from .chatbot_service import OpenSourceChatbotService
    from .conversation_memory import ConversationMemory
    from .human_interaction import interaction_optimizer
    
    HAS_ENHANCED_SERVICES = True
    HAS_MEDICAL_SERVICE = True
    HAS_MEMORY_SERVICE = True
    HAS_HUMAN_INTERACTION = True
except ImportError as e:
    print(f"⚠️  Enhanced services not available: {e}")
    HAS_ENHANCED_SERVICES = False
    HAS_MEDICAL_SERVICE = False
    HAS_MEMORY_SERVICE = False
    HAS_HUMAN_INTERACTION = False
    try:
        from .chatbot_service import OpenSourceChatbotService
        try:
            from .medical_knowledge_service import medical_service, get_medical_information
            HAS_MEDICAL_SERVICE = True
        except ImportError:
            HAS_MEDICAL_SERVICE = False
    except ImportError:
        pass

class EnhancedClangService:
    """Simple, clean chatbot service with direct responses"""
    
    def __init__(self):
        self.name = "Enhanced Clang"
        self.version = "3.0 Simple"
        
        # Initialize base chatbot service
        try:
            self.base_chatbot = OpenSourceChatbotService()
            print(f"✅ {self.name} {self.version} initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize base chatbot: {e}")
            self.base_chatbot = None
        
        # Initialize conversation memory system
        if HAS_MEMORY_SERVICE:
            try:
                self.memory = ConversationMemory()
                print("✅ Conversation memory system initialized")
            except Exception as e:
                print(f"⚠️ Memory system failed to initialize: {e}")
                self.memory = None
        else:
            self.memory = None
        
        # Track conversation context
        self.conversation_memory = []
        self.user_preferences = {}
        self.session_stats = {
            'queries_processed': 0,
            'session_start': datetime.now()
        }
    
    async def get_enhanced_response(self, user_message: str, conversation_history: List = None, user_id: str = None) -> Dict[str, Any]:
        """Main method to process user queries with simple, direct responses"""
        
        start_time = datetime.now()
        self.session_stats['queries_processed'] += 1
        
        try:
            # Get simple, direct response
            response_text = self._get_direct_response(user_message)
            
            return {
                'response': response_text,
                'metadata': {
                    'processing_time_seconds': (datetime.now() - start_time).total_seconds(),
                    'query_type': 'direct_response',
                    'service_used': 'simple_enhanced_clang',
                    'sources': ['built_in_knowledge']
                }
            }
            
        except Exception as e:
            return {
                'response': f"I encountered an issue: {str(e)}. Let me try to help you in a simpler way.",
                'metadata': {
                    'error': str(e),
                    'processing_time_seconds': (datetime.now() - start_time).total_seconds(),
                    'fallback_used': True
                }
            }
    
    def _get_direct_response(self, query: str) -> str:
        """Generate simple, direct, accurate responses"""
        query_lower = query.lower()
        
        # Greetings
        if any(greeting in query_lower for greeting in ['hello', 'hi', 'hey']):
            return """Hey there! 👋 

How can I help you today? I'm here to assist with:
• Medical questions and health information
• Mathematical calculations and problem solving  
• Programming help and code assistance
• General knowledge and research
• Writing and creative tasks

What would you like to explore?"""
        
        # Simple arithmetic calculations
        arithmetic_match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', query)
        if arithmetic_match:
            num1, operator, num2 = arithmetic_match.groups()
            try:
                result = eval(f"{num1} {operator} {num2}")
                return f"**{num1} {operator} {num2} = {result}**"
            except:
                pass
        
        # Common acronyms - direct answers
        if 'www' in query_lower:
            return """**WWW** stands for **World Wide Web**

The World Wide Web (WWW) is an information system that enables documents and other web resources to be accessed over the Internet using web browsers.

**Key facts:**
- Invented by Tim Berners-Lee in 1989-1990
- Uses HTTP/HTTPS protocols  
- Consists of web pages connected by hyperlinks
- Revolutionized global information sharing"""

        if 'html' in query_lower:
            return """**HTML** stands for **HyperText Markup Language**

HTML is the standard markup language for creating web pages and web applications.

**Key features:**
- Uses tags to structure content
- Defines headings, paragraphs, links, images
- Works with CSS for styling and JavaScript for interactivity
- Forms the backbone of all websites"""

        if 'api' in query_lower:
            return """**API** stands for **Application Programming Interface**

An API is a set of protocols and tools that allows different software applications to communicate with each other.

**Key concepts:**
- Enables data exchange between applications
- Uses HTTP requests (GET, POST, PUT, DELETE)
- Returns data in formats like JSON or XML
- Powers modern web services and mobile apps"""
            
        # Programming questions - direct answers
        if any(keyword in query_lower for keyword in ['python code', 'write code', 'programming']) and 'sort' in query_lower:
            return """**Python Code for Sorting a List:**

```python
# Method 1: Using built-in sorted() function
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # [11, 12, 22, 25, 34, 64, 90]

# Method 2: Using list.sort() method
numbers = [64, 34, 25, 12, 22, 11, 90]
numbers.sort()
print(numbers)  # [11, 12, 22, 25, 34, 64, 90]

# Method 3: Bubble Sort implementation
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```"""

        # Astronomy questions - direct answers
        if 'mars' in query_lower:
            return """**Mars** is the fourth planet from the Sun in our solar system.

**Key facts about Mars:**
- **Distance from Sun:** 228 million km (142 million miles)
- **Size:** About half the size of Earth
- **Day length:** 24 hours 37 minutes
- **Year length:** 687 Earth days
- **Moons:** 2 small moons (Phobos and Deimos)
- **Atmosphere:** Thin, mostly carbon dioxide
- **Color:** Red/orange due to iron oxide (rust)
- **Temperature:** Very cold, average -80°F (-62°C)

Mars is a major target for space exploration and potential human colonization."""

        if 'earth' in query_lower:
            return """**Earth** is the third planet from the Sun and our home planet.

**Key facts about Earth:**
- **Distance from Sun:** 150 million km (93 million miles)
- **Size:** Diameter of 12,742 km
- **Day length:** 24 hours
- **Year length:** 365.25 days
- **Moon:** 1 large moon
- **Atmosphere:** 78% nitrogen, 21% oxygen
- **Surface:** 71% water, 29% land
- **Temperature:** Average 15°C (59°F)

Earth is the only known planet with life in the universe."""

        # Medical questions - use existing medical service
        if any(keyword in query_lower for keyword in ['diabetes', 'symptoms', 'medical', 'health']):
            if HAS_MEDICAL_SERVICE:
                try:
                    if hasattr(medical_service, 'get_medical_response'):
                        return medical_service.get_medical_response(query)
                    elif hasattr(medical_service, 'get_condition_info'):
                        return medical_service.get_condition_info(query)
                    else:
                        return get_medical_information(query)
                except Exception as e:
                    print(f"Medical service error: {e}")
                    return "I can help with medical information. Please ask specific questions about symptoms, conditions, or treatments."
            else:
                return "I can help with medical information. Please ask specific questions about symptoms, conditions, or treatments."
        
        # Science questions
        if any(keyword in query_lower for keyword in ['photosynthesis', 'cell', 'dna']):
            return """**Photosynthesis** is the process by which plants make their own food using sunlight.

**How it works:**
1. **Light absorption:** Chlorophyll captures sunlight
2. **Water uptake:** Roots absorb water from soil
3. **CO2 intake:** Leaves take in carbon dioxide from air
4. **Chemical reaction:** Creates glucose and oxygen
5. **Energy storage:** Glucose provides energy for plant growth

**Formula:** 6CO₂ + 6H₂O + sunlight → C₆H₁₂O₆ + 6O₂

This process is essential for life on Earth as it produces the oxygen we breathe."""

        # Technology questions
        if any(keyword in query_lower for keyword in ['artificial intelligence', 'ai', 'machine learning']):
            return """**Artificial Intelligence (AI)** is technology that enables machines to perform tasks that typically require human intelligence.

**Key concepts:**
- **Machine Learning:** Systems that learn from data
- **Neural Networks:** AI models inspired by the brain
- **Natural Language Processing:** Understanding human language
- **Computer Vision:** Analyzing images and videos

**Applications:**
- Virtual assistants (Siri, Alexa)
- Recommendation systems (Netflix, Spotify)
- Self-driving cars
- Medical diagnosis
- Language translation

AI is rapidly advancing and transforming many industries."""
        
        # Fallback using base chatbot if available
        if self.base_chatbot:
            try:
                base_response = self.base_chatbot.get_response(query)
                if base_response and len(base_response.strip()) > 10:
                    return base_response
            except:
                pass
        
        # Simple general knowledge fallback
        return f"""I can help explain **{query}**. 

For specific questions, try asking about:
- **Technology:** WWW, HTML, APIs, AI, programming
- **Science:** planets, biology, chemistry, physics  
- **Math:** calculations, equations, formulas
- **Medical:** symptoms, conditions, treatments
- **General knowledge:** history, geography, culture

What would you like to know more about?"""

# Global instance
enhanced_clang = EnhancedClangService()
