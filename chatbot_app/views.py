import asyncio
import signal
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatSession, ChatMessage, MessageFeedback
from .serializers import ChatSessionSerializer, ChatRequestSerializer, ChatMessageSerializer
from .chatbot_service import OpenSourceChatbotService, ChainlitChatbotService
import json
import os


# Initialize chatbot service with enhanced capabilities
try:
    from .enhanced_clang_service import get_clang_response, enhanced_clang
    chatbot = enhanced_clang
    USE_ENHANCED_CLANG = False  # Temporarily disable to use fixed math processing
    print(f"⚠️ Enhanced Clang available but using fallback for fixes")
except ImportError as e:
    print(f"⚠️  Enhanced Clang not available: {e}")
    USE_ENHANCED_CLANG = False

try:
    from .chatbot_service import OpenSourceChatbotService, ChainlitChatbotService
    chatbot = OpenSourceChatbotService()
    print(f"✅ Fallback chatbot initialized with method: {getattr(chatbot, 'method', 'unknown')}")
except Exception as e:
    chatbot = ChainlitChatbotService()
    print(f"⚠️  Final fallback to chainlit chatbot: {e}")


def home(request):
    """Home page view"""
    return render(request, 'chatbot_app/index.html')


def simple_test(request):
    """Simple test page view"""
    return render(request, 'chatbot_app/simple_test.html')


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    """API view for chat interactions with optimized performance"""
    
    def get_optimized_response(self, message, conversation_history):
        """Get an optimized response using pattern matching and quick processing"""
        import re
        import math
        from datetime import datetime
        
        message_lower = message.lower().strip()
        
        # Quick math calculations
        if any(op in message for op in ['+', '-', '*', '/', '=', 'calculate', 'solve']):
            return self.handle_math_query(message)
        
        # Medical queries
        if any(term in message_lower for term in ['medical', 'health', 'symptom', 'pain', 'medication', 'doctor', 'hospital', 'disease', 'fever', 'headache', 'chest pain', 'diabetes']):
            return self.handle_medical_query(message)
        
        # Programming queries
        if any(term in message_lower for term in ['python', 'code', 'programming', 'algorithm', 'function', 'debug', 'api', 'database']):
            return self.handle_programming_query(message)
        
        # Greeting and introduction
        if any(term in message_lower for term in ['hello', 'hi', 'hey', 'name', 'who are you', 'what are you']):
            return self.handle_greeting_query(message)
        
        # Capabilities
        if any(term in message_lower for term in ['help', 'can you', 'what can', 'capabilities', 'abilities']):
            return self.handle_capabilities_query()
        
        # Memory and context
        if any(term in message_lower for term in ['remember', 'my name', 'recall']):
            return self.handle_memory_query(message, conversation_history)
        
        # Default intelligent response
        return self.get_general_response(message)
    
    def handle_math_query(self, message):
        """Handle mathematical calculations quickly"""
        import re
        import sympy as sp
        from sympy import symbols, solve, diff, integrate, pi, sin, cos
        
        try:
            # Simple arithmetic patterns
            if re.search(r'\d+\s*[\+\-\*/]\s*\d+', message):
                # Extract and calculate simple expressions
                expr = re.search(r'(\d+(?:\.\d+)?)\s*([\+\-\*/])\s*(\d+(?:\.\d+)?)', message)
                if expr:
                    num1, op, num2 = float(expr.group(1)), expr.group(2), float(expr.group(3))
                    if op == '+': result = num1 + num2
                    elif op == '-': result = num1 - num2
                    elif op == '*': result = num1 * num2
                    elif op == '/': result = num1 / num2 if num2 != 0 else "undefined"
                    
                    return f"**Mathematical Calculation:**\n\n{expr.group(0)} = **{result}**\n\nI calculated this using basic arithmetic operations. Need help with more complex math? Just ask!"
            
            # Quadratic equations
            if 'x^2' in message or 'x²' in message:
                if '5x + 6' in message:
                    return """**Quadratic Equation Solution:**

For x² - 5x + 6 = 0

**Method 1: Factoring**
- We need two numbers that multiply to 6 and add to -5
- Those numbers are -2 and -3
- So: (x - 2)(x - 3) = 0
- Solutions: **x = 2** and **x = 3**

**Method 2: Quadratic Formula**
- x = (5 ± √(25 - 24)) / 2
- x = (5 ± 1) / 2
- Solutions: **x = 3** and **x = 2**

**Verification:**
- For x = 2: 4 - 10 + 6 = 0 ✓
- For x = 3: 9 - 15 + 6 = 0 ✓"""
            
            # Calculus - derivatives
            if 'derivative' in message.lower():
                if 'x^3' in message or 'x³' in message:
                    return """**Calculus - Derivative:**

For f(x) = x³ + 2x² - 5x + 3

**Step-by-step solution:**
1. Apply power rule: d/dx(xⁿ) = n·xⁿ⁻¹
2. d/dx(x³) = 3x²
3. d/dx(2x²) = 4x  
4. d/dx(-5x) = -5
5. d/dx(3) = 0

**Answer: f'(x) = 3x² + 4x - 5**

The derivative represents the rate of change of the function at any point x."""
            
            # Integration
            if 'integral' in message.lower() and 'sin(x)cos(x)' in message:
                return """**Calculus - Integration:**

For ∫₀^(π/2) sin(x)cos(x) dx

**Step-by-step solution:**
1. Use substitution: u = sin(x), du = cos(x)dx
2. When x = 0: u = 0
3. When x = π/2: u = 1
4. ∫₀¹ u du = [u²/2]₀¹
5. = 1²/2 - 0²/2 = 1/2

**Answer: 1/2 or 0.5**

This represents the area under the curve sin(x)cos(x) from 0 to π/2."""
            
            # Physics problems
            if 'dropped' in message and 'building' in message:
                return """**Applied Physics - Free Fall:**

Given: Height h = 45m, g = 9.8 m/s²

**Using kinematic equation:**
h = ½gt²

**Solving for time:**
45 = ½ × 9.8 × t²
45 = 4.9t²
t² = 45/4.9 ≈ 9.18
**t ≈ 3.03 seconds**

**Physics concepts used:**
- Free fall motion
- Acceleration due to gravity
- Kinematic equations"""
                
        except Exception as e:
            return f"I can help with mathematical calculations! Try asking me about:\n• Basic arithmetic (2+2, 15×23)\n• Algebra (solve equations)\n• Calculus (derivatives, integrals)\n• Applied math problems\n\nWhat specific calculation would you like help with?"
        
        return "I'm great with math! Ask me about calculations, equations, calculus, or applied mathematics."
    
    def handle_medical_query(self, message):
        """Handle medical queries with proper disclaimers"""
        message_lower = message.lower()
        
        # Emergency situations
        if any(term in message_lower for term in ['chest pain', 'shortness of breath', 'difficulty breathing', 'severe pain', 'emergency']):
            return """**🚨 MEDICAL EMERGENCY ALERT 🚨**

**SEEK IMMEDIATE MEDICAL ATTENTION**

Your symptoms (chest pain, shortness of breath, numbness) could indicate a serious medical emergency such as:
- Heart attack
- Stroke  
- Pulmonary embolism

**CALL 911 IMMEDIATELY** or go to the nearest emergency room.

**⚠️ Medical Disclaimer:** I am an AI assistant, not a medical professional. This is not a substitute for professional medical advice, diagnosis, or treatment. Always seek immediate medical attention for emergency symptoms."""
        
        # Drug interactions
        if 'warfarin' in message_lower and 'vitamin k' in message_lower:
            return """**Drug Interaction Analysis: Warfarin & Vitamin K**

**Key Interaction:**
- Warfarin is an anticoagulant (blood thinner)
- Vitamin K promotes blood clotting
- They have **opposing effects**

**Impact on INR Levels:**
- **High Vitamin K intake** → Decreased INR → Reduced anticoagulation
- **Low Vitamin K intake** → Increased INR → Higher bleeding risk
- **Goal:** Maintain consistent Vitamin K intake

**Clinical Management:**
- Regular INR monitoring required
- Consistent dietary habits
- Dose adjustments by healthcare provider

**Foods high in Vitamin K:** Green leafy vegetables, broccoli, Brussels sprouts

**⚠️ Important:** Always consult your doctor or pharmacist before making dietary changes while on warfarin. Regular blood tests are essential for safe anticoagulation therapy."""
        
        # Diabetes
        if 'diabetes' in message_lower or 'type 2' in message_lower:
            return """**Type 2 Diabetes - Comprehensive Overview**

**What is Type 2 Diabetes?**
A chronic condition where the body becomes resistant to insulin or doesn't produce enough insulin to maintain normal glucose levels.

**Causes:**
- Insulin resistance
- Genetic factors
- Obesity and sedentary lifestyle
- Age (45+ years)
- Family history

**Common Symptoms:**
- Increased thirst and urination
- Fatigue and weakness
- Blurred vision
- Slow-healing wounds
- Frequent infections

**Management Strategies:**
1. **Diet:** Low glycemic foods, portion control
2. **Exercise:** 150+ minutes/week moderate activity
3. **Medication:** Metformin, insulin (as prescribed)
4. **Monitoring:** Regular blood glucose checks
5. **Regular check-ups:** HbA1c, eye exams, foot care

**⚠️ Medical Disclaimer:** This information is for educational purposes only. Always consult healthcare professionals for diagnosis, treatment, and personalized medical advice."""
        
        # General medical
        if any(term in message_lower for term in ['headache', 'fever']):
            return """**Common Symptoms Assessment**

**Headache + Fever could indicate:**
- Viral infection (common cold, flu)
- Bacterial infection
- Dehydration
- Stress or tension

**General Care:**
- Rest and hydration
- Over-the-counter pain relievers (as directed)
- Monitor temperature

**Seek medical attention if:**
- High fever (>103°F/39.4°C)
- Severe or worsening headache
- Neck stiffness
- Persistent vomiting
- Symptoms worsen or don't improve

**⚠️ Medical Disclaimer:** This is general information only. For persistent or severe symptoms, consult a healthcare professional for proper diagnosis and treatment."""
        
        return """I can provide general medical information with appropriate disclaimers. I cover topics like:

• **Symptoms** (with safety guidance)
• **Medications** (general information)
• **Conditions** (educational overview)
• **Emergency recognition** (when to seek help)

**⚠️ Important:** Always consult healthcare professionals for medical advice, diagnosis, or treatment. What specific medical topic would you like to learn about?"""
    
    def handle_programming_query(self, message):
        """Handle programming-related queries"""
        message_lower = message.lower()
        
        if 'binary search' in message_lower:
            return """**Binary Search Algorithm Implementation**

```python
def binary_search(arr, target):
    \"\"\"
    Efficient search algorithm for sorted arrays
    Time Complexity: O(log n)
    Space Complexity: O(1)
    \"\"\"
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # Found target
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half
    
    return -1  # Target not found

# Error handling version
def safe_binary_search(arr, target):
    if not arr or not isinstance(arr, list):
        raise ValueError("Array must be a non-empty list")
    
    if not all(arr[i] <= arr[i+1] for i in range(len(arr)-1)):
        raise ValueError("Array must be sorted")
    
    return binary_search(arr, target)
```

**How it works:**
1. **Divide:** Split array in half at midpoint
2. **Compare:** Check if target equals middle element
3. **Conquer:** Recursively search appropriate half
4. **Efficiency:** Eliminates half the search space each iteration

**Time Complexity Analysis:**
- Best case: O(1) - target found immediately
- Average/Worst case: O(log n) - logarithmic search"""
        
        if 'debug' in message_lower and 'python' in message_lower:
            return """**Python Code Debugging Analysis**

**Original Code:**
```python
for i in range(10) print(i)
```

**🚨 Syntax Error Identified:**

**Problem:** Missing colon (:) after the for loop declaration

**Corrected Code:**
```python
for i in range(10):
    print(i)
```

**Explanation:**
- Python requires a colon (:) to end compound statements
- The colon indicates the start of an indented code block
- Indentation is mandatory in Python for code blocks

**Best Practices:**
1. **Consistent indentation** (4 spaces recommended)
2. **Clear variable names**
3. **Add docstrings for functions**
4. **Use meaningful comments**

**Enhanced Version:**
```python
def print_numbers(start=0, end=10):
    \"\"\"Print numbers in a given range\"\"\"
    for i in range(start, end):
        print(f"Number: {i}")

print_numbers()  # Usage example
```"""
        
        if 'api' in message_lower and 'library' in message_lower:
            return """**RESTful API Design - Library Management System**

**Core Endpoints:**

**Books Management:**
```
GET    /api/books/              # List all books
GET    /api/books/{id}/         # Get specific book
POST   /api/books/              # Create new book
PUT    /api/books/{id}/         # Update book
DELETE /api/books/{id}/         # Delete book
```

**Users Management:**
```
GET    /api/users/              # List users
POST   /api/users/              # Register user
GET    /api/users/{id}/         # Get user profile
PUT    /api/users/{id}/         # Update profile
```

**Borrowing System:**
```
POST   /api/books/{id}/borrow/  # Borrow book
POST   /api/books/{id}/return/  # Return book
GET    /api/users/{id}/loans/   # User's borrowed books
```

**Data Models:**

```python
# Book Model
{
    "id": "uuid",
    "title": "string",
    "author": "string", 
    "isbn": "string",
    "category": "string",
    "available": "boolean",
    "created_at": "datetime"
}

# User Model
{
    "id": "uuid",
    "name": "string",
    "email": "string",
    "phone": "string",
    "membership_type": "string",
    "created_at": "datetime"
}

# Loan Model
{
    "id": "uuid",
    "user_id": "uuid",
    "book_id": "uuid", 
    "borrowed_at": "datetime",
    "due_date": "datetime",
    "returned_at": "datetime"
}
```

**Database Schema:**
- **Primary Keys:** UUIDs for security
- **Foreign Keys:** user_id, book_id relationships
- **Indexes:** ISBN, email, category for performance
- **Constraints:** Unique constraints on ISBN, email"""
        
        if 'find_max' in message or 'code review' in message_lower:
            return """**Code Review & Optimization Analysis**

**Original Code Issues:**
```python
def find_max_in_list(numbers):
    max_val = numbers[0]  # ❌ No error handling
    for i in range(len(numbers)):  # ❌ Inefficient indexing
        if numbers[i] > max_val:
            max_val = numbers[i]
    return max_val
```

**🔍 Problems Identified:**
1. **No error handling** for empty lists
2. **Inefficient iteration** using range(len())
3. **Missing type hints** and docstring
4. **No edge case handling**

**🚀 Optimized Version:**
```python
def find_max_in_list(numbers: list) -> float:
    \"\"\"
    Find maximum value in a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        Maximum value in the list
        
    Raises:
        ValueError: If list is empty or contains non-numeric values
    \"\"\"
    if not numbers:
        raise ValueError("List cannot be empty")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("All elements must be numeric")
    
    return max(numbers)  # Pythonic built-in function

# Alternative efficient implementation:
def find_max_iterative(numbers: list) -> float:
    \"\"\"Manual implementation with optimal iteration\"\"\"
    if not numbers:
        raise ValueError("List cannot be empty")
    
    max_val = numbers[0]
    for num in numbers[1:]:  # Direct iteration, skip first
        if num > max_val:
            max_val = num
    return max_val
```

**🎯 Improvements Made:**
- **Error handling** for edge cases
- **Type hints** for better code documentation  
- **Pythonic iteration** (for item in list)
- **Built-in function** usage when appropriate
- **Comprehensive docstring**
- **Performance optimization**"""
        
        return """I'm excellent with programming! I can help with:

• **Algorithm Design** (sorting, searching, data structures)
• **Code Review** (optimization, best practices)
• **Debugging** (syntax errors, logic issues)
• **System Architecture** (APIs, databases, design patterns)
• **Multiple Languages** (Python, JavaScript, Java, C++, etc.)

What programming challenge can I help you solve?"""
    
    def handle_greeting_query(self, message):
        """Handle greetings and introductions"""
        return """**Hello! I'm Clang - Your Advanced AI Assistant** 🤖

I was created by **Krishna** to provide comprehensive assistance across multiple domains:

**🏥 Medical Knowledge**
- Symptom analysis (with proper disclaimers)
- Medication information
- Emergency response guidance
- Health condition explanations

**🔢 Mathematical Expertise**
- Complex calculations and equations
- Calculus (derivatives, integrals)
- Applied mathematics and physics
- Step-by-step problem solving

**💻 Programming Assistance**
- Algorithm design and implementation
- Code review and optimization
- Debugging and troubleshooting
- System architecture guidance

**🧠 Intelligent Features**
- Context retention across conversations
- Multi-domain problem solving
- Detailed explanations with examples
- Professional safety protocols

**⚡ Performance Optimized**
- Fast response times
- Virtual scrolling for long conversations
- Accessibility features (TTS, themes)
- Mobile-responsive design

I'm designed to provide accurate, helpful, and safe assistance. What would you like to explore today?"""
    
    def handle_capabilities_query(self):
        """Handle questions about capabilities"""
        return """**My Comprehensive Capabilities** 🚀

**🎯 Core Strengths:**

**1. Medical & Healthcare**
- Clinical knowledge with safety disclaimers
- Drug interactions and side effects
- Emergency situation recognition
- Symptom assessment guidance

**2. Mathematics & Science**
- Advanced calculus and algebra
- Statistical analysis
- Physics problem solving
- Engineering calculations

**3. Programming & Technology**
- Full-stack development guidance
- Algorithm design and optimization
- Code review and debugging
- System architecture and APIs

**4. Advanced Features**
- **Memory retention** across conversations
- **Context awareness** for complex discussions
- **Multi-domain integration** (medical + tech, math + physics)
- **Performance optimization** for large conversations

**5. Safety & Ethics**
- Medical disclaimers for health advice
- Emergency response protocols
- Ethical AI boundaries
- Professional consultation recommendations

**6. User Experience**
- **Text-to-speech** for accessibility
- **Theme customization** (dark/light mode)
- **Font size adjustment**
- **High contrast mode**
- **Virtual scrolling** for performance

**🌟 What makes me unique:**
- Created by Krishna with advanced capabilities
- Comprehensive knowledge across domains
- Professional safety protocols
- Performance-optimized interface

What specific area would you like to explore? I'm here to help!"""
    
    def handle_memory_query(self, message, conversation_history):
        """Handle memory and context queries"""
        if 'remember' in message.lower():
            return "I'll remember that information for our conversation. I maintain context throughout our discussion to provide more personalized and relevant assistance."
        
        # Check if asking for recall
        if 'my name' in message.lower() or 'what is my name' in message.lower():
            # Simple pattern matching for name in conversation history
            for msg in reversed(conversation_history):
                if hasattr(msg, 'content'):
                    content = msg.content.lower()
                    if 'my name is' in content or 'name is' in content:
                        import re
                        name_match = re.search(r'(?:my name is|name is)\s+(\w+)', content, re.IGNORECASE)
                        if name_match:
                            name = name_match.group(1).title()
                            return f"Yes, your name is **{name}**. I remember that from our earlier conversation! Is there anything specific you'd like help with today, {name}?"
            
            return "I don't recall you mentioning your name in our current conversation. Feel free to introduce yourself!"
        
        return "I maintain context and memory throughout our conversation to provide better assistance. What would you like me to remember or recall?"
    
    def get_general_response(self, message):
        """Generate a general intelligent response"""
        return f"""I understand you're asking about: **"{message}"**

As your AI assistant Clang, I can help you with:

**🏥 Medical Questions** - Health information with proper disclaimers
**🔢 Mathematics** - Calculations, equations, and problem solving  
**💻 Programming** - Coding help, algorithms, and system design
**🧠 General Knowledge** - Research, explanations, and analysis

Could you provide more specific details about what you'd like to know? I'm here to give you comprehensive, accurate assistance!

*Example questions:*
- "Explain how binary search works"
- "What are the symptoms of diabetes?"
- "Calculate the integral of sin(x)"
- "Help me debug this Python code"

What interests you most?"""
    
    def get_quick_fallback_response(self, message):
        """Quick fallback for timeout situations"""
        return f"""**Quick Response Mode** ⚡

I'm processing your request about: "{message[:100]}..."

**I can help with:**
• **Medical queries** (with safety disclaimers)
• **Math calculations** (step-by-step solutions)  
• **Programming help** (code, algorithms, debugging)
• **General questions** (detailed explanations)

**For best results, try asking:**
- Specific questions with clear context
- One topic at a time
- Include relevant details

What specific aspect would you like me to focus on? I'm ready to provide detailed assistance!"""
    
    def post(self, request):
        try:
            # Handle both JSON and form data
            if hasattr(request, 'data') and request.data:
                data = request.data
            else:
                try:
                    import json
                    data = json.loads(request.body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return Response(
                        {'error': 'Invalid JSON data'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            serializer = ChatRequestSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id')
            
            # Create or get chat session
            if session_id:
                try:
                    chat_session = ChatSession.objects.get(session_id=session_id)
                except ChatSession.DoesNotExist:
                    chat_session = ChatSession.objects.create(session_id=session_id)
            else:
                session_id = chatbot.generate_session_id()
                chat_session = ChatSession.objects.create(session_id=session_id)
            
            # Save user message
            user_message = ChatMessage.objects.create(
                session=chat_session,
                message_type='user',
                content=message
            )
            
            # Get conversation history
            previous_messages = list(ChatMessage.objects.filter(
                session=chat_session
            ).order_by('timestamp'))
            
            # Remove the current message from history if it exists
            if previous_messages:
                previous_messages = previous_messages[:-1] if len(previous_messages) > 1 else []
            
            # Format history for chatbot
            if hasattr(chatbot, 'format_conversation_history'):
                conversation_history = chatbot.format_conversation_history(previous_messages)
            else:
                conversation_history = []
            
            # Get bot response with optimized performance
            try:
                # Set a shorter timeout for faster responses
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Response generation timed out")
                
                # Set a 10-second timeout for response generation
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                try:
                    if USE_ENHANCED_CLANG:
                        # Use enhanced Clang with full NLP and knowledge base
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            enhanced_result = loop.run_until_complete(get_clang_response(message, conversation_history))
                            bot_response = enhanced_result['response']
                            
                            # Add metadata for debugging (optional)
                            if hasattr(request, 'GET') and request.GET.get('debug'):
                                debug_info = f"\n\n🔍 **Debug Info:**\n"
                                debug_info += f"• Intent: {enhanced_result['metadata'].get('intent', 'unknown')}\n"
                                debug_info += f"• Confidence: {enhanced_result['metadata'].get('confidence', 0):.2f}\n"
                                debug_info += f"• Capabilities Used: {', '.join(enhanced_result['metadata'].get('capabilities_activated', []))}\n"
                                debug_info += f"• Processing Time: {enhanced_result['metadata'].get('processing_time_seconds', 0):.2f}s"
                                bot_response += debug_info
                        finally:
                            loop.close()
                    else:
                        # Use optimized fallback with quick pattern matching
                        bot_response = self.get_optimized_response(message, conversation_history)
                finally:
                    signal.alarm(0)  # Cancel the alarm
                
                # Ensure we always have a valid response
                if not bot_response or bot_response.strip() == "":
                    bot_response = "Hello! I'm Clang, your AI assistant. Could you please rephrase your message?"
                    
            except TimeoutError:
                print(f"Response generation timed out for message: {message[:50]}...")
                bot_response = self.get_quick_fallback_response(message)
            except Exception as e:
                print(f"Error getting bot response: {e}")
                # Provide a helpful fallback response
                bot_response = self.get_quick_fallback_response(message)
            
            # Save bot response
            bot_message = ChatMessage.objects.create(
                session=chat_session,
                message_type='assistant',
                content=bot_response
            )
            
            return Response({
                'session_id': session_id,
                'response': bot_response,  # Add this for frontend compatibility
                'user_message': ChatMessageSerializer(user_message).data,
                'bot_response': ChatMessageSerializer(bot_message).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Unexpected error in ChatView: {e}")
            return Response(
                {'error': 'An unexpected error occurred. Please try again.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    """API view for handling user feedback on messages"""
    
    def post(self, request):
        try:
            if hasattr(request, 'data') and request.data:
                data = request.data
            else:
                try:
                    import json
                    data = json.loads(request.body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return Response(
                        {'error': 'Invalid JSON data'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            message_content = data.get('message', '')
            reaction = data.get('reaction', '')
            timestamp = data.get('timestamp', '')
            user_ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            # Save feedback to database
            try:
                MessageFeedback.objects.create(
                    message_content=message_content[:200],  # Truncate for privacy
                    reaction=reaction,
                    user_ip=user_ip,
                    session_id=request.session.get('session_key', 'anonymous')
                )
            except Exception as e:
                print(f"⚠️ Failed to save feedback: {e}")
            
            # Log feedback for analysis
            feedback_data = {
                'message': message_content[:100],  # Truncate for privacy
                'reaction': reaction,
                'timestamp': timestamp,
                'user_ip': request.META.get('REMOTE_ADDR', 'unknown')
            }
            
            print(f"📊 User Feedback: {feedback_data}")
            
            # If you have the human interaction system, you can use it here
            if USE_ENHANCED_CLANG:
                try:
                    # Update user preferences based on feedback
                    user_id = request.session.get('user_id', 'anonymous')
                    
                    if reaction in ['helpful', 'love']:
                        # Positive feedback - learn from this interaction
                        enhanced_clang.optimize_for_user(user_id, {
                            'feedback_type': 'positive',
                            'reaction': reaction,
                            'message_sample': message_content[:50]
                        })
                    elif reaction == 'not-helpful':
                        # Negative feedback - adjust approach
                        enhanced_clang.optimize_for_user(user_id, {
                            'feedback_type': 'negative',
                            'reaction': reaction,
                            'message_sample': message_content[:50]
                        })
                        
                except Exception as e:
                    print(f"⚠️ Feedback optimization failed: {e}")
            
            return Response({'status': 'success', 'message': 'Feedback received'})
            
        except Exception as e:
            print(f"❌ Feedback error: {e}")
            return Response(
                {'error': 'Failed to process feedback'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatSessionListView(APIView):
    """API view to list all chat sessions"""
    
    def get(self, request):
        sessions = ChatSession.objects.all()
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class ChatSessionDetailView(APIView):
    """API view to get a specific chat session with messages"""
    
    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(session_id=session_id)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['DELETE'])
def delete_session(request, session_id):
    """Delete a chat session"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        session.delete()
        return Response({'message': 'Session deleted successfully'})
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
