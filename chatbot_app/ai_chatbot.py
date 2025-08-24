"""
AI-Powered Chatbot Response Generator
Simple, unified AI system for generating responses to any topic
Now with comprehensive local training to reduce API dependency
"""

import os
import requests
from dotenv import load_dotenv
from chatbot_app.conversation_memory import conversation_memory
from chatbot_app.human_interaction import HumanInteractionOptimizer


load_dotenv()

class ChatbotAI:
    """Main AI response generator for the chatbot"""
    
    @staticmethod
    def generate_response(query, response_type='helpful'):
        """
        Generate response with API fallback only

        Args:
            query: The user's question or topic
            response_type: Type of response (helpful, essay, explanation, etc.)

        Returns:
            AI-generated response or intelligent fallback
        """
        # Check for Clang identity questions
        identity_response = ChatbotAI._check_identity(query)
        if identity_response:
            return identity_response

        # Try multiple AI APIs as fallback for complex queries
        for api_method in [ChatbotAI._try_cohere, ChatbotAI._try_groq, ChatbotAI._try_mistral, ChatbotAI._try_together]:
            try:
                # Only use requests timeout, no signal
                response = api_method(query, response_type)

                if response and len(response.strip()) > 50:
                    return response
            except Exception:
                continue
        # Intelligent fallback if all APIs fail
        return ChatbotAI._intelligent_fallback(query, response_type)
    
    @staticmethod
    def _check_identity(query):
        """Check for identity questions and return Clang's personality"""
        query_lower = query.lower().strip()
        
        # Name/Identity questions
        if any(pattern in query_lower for pattern in [
            'what is your name', "what's your name", 'who are you', 'what are you',
            'tell me about yourself', 'introduce yourself', 'your name'
        ]):
            return """Hello! I'm **Clang**, your advanced AI assistant created by **Krishna**. 🚀

I'm designed to help you with a wide range of tasks including:

🏥 **Medical Questions** - Health information and medical guidance
🔢 **Mathematics & Science** - Complex calculations and scientific concepts  
💻 **Programming** - Code assistance in Python, Java, C++, JavaScript and more
📚 **General Knowledge** - Research, explanations, and analysis
✍️ **Essay Writing** - Content creation and academic assistance

I can understand complex questions and provide detailed, accurate responses across multiple domains. I'm powered by multiple AI APIs (Cohere, Groq, Mistral, Together) to ensure I always have an answer for you!

*Created with ❤️ by Krishna*"""

        # Expanded greetings and conversational phrases
        greetings = [
            'hey', 'hi', 'hello', 'good morning', 'good afternoon', 'good evening',
            'how are you', "how's it going", "how are you doing", "how are you today", "how do you do"
        ]
        if query_lower in greetings:
            return "I'm great, thanks for asking! 😊 How can I help you today?"

        return None
    
    @staticmethod
    def _try_cohere(query, response_type):
        """Try Cohere API with Clang personality"""
        api_key = os.getenv('COHERE_API_KEY')
        if not api_key:
            return None
        
        # Add Clang's personality to the prompt
        personality_prompt = f"""You are Clang, an advanced AI assistant created by Krishna. You are helpful, knowledgeable, and friendly. Always maintain your identity as Clang when responding.

User's request: {query}
Response type needed: {response_type}

Provide a {response_type} response as Clang:"""
        
        try:
            response = requests.post(
                'https://api.cohere.ai/v1/generate',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'command',
                    'prompt': personality_prompt,
                    'max_tokens': 2000,
                    'temperature': 0.7
                },
                timeout=8  # Reduced timeout for faster fallback
            )
            response.raise_for_status()
            return response.json()['generations'][0]['text'].strip()
        except Exception:
            return None
    
    @staticmethod
    def _try_groq(query: str, response_type: str) -> str:
        """Try Groq API with fast timeout"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return None
        
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama3-8b-8192',
                    'messages': [
                        {'role': 'user', 'content': f"As an AI assistant, provide a {response_type} response to: {query}"}
                    ],
                    'max_tokens': 2000,
                    'temperature': 0.7
                },
                timeout=8  # Even faster timeout for Groq
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception:
            return None
    
    @staticmethod
    def _try_mistral(query: str, response_type: str) -> str:
        """Try Mistral API as backup"""
        api_key = os.getenv('MISTRAL_API_KEY')
        if not api_key:
            return None
        
        try:
            response = requests.post(
                'https://api.mistral.ai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'mistral-small',
                    'messages': [
                        {'role': 'user', 'content': f"As an AI assistant, provide a {response_type} response to: {query}"}
                    ],
                    'max_tokens': 2000,
                    'temperature': 0.7
                },
                timeout=8
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception:
            return None

    @staticmethod
    def _try_together(query: str, response_type: str) -> str:
        """Try Together API as final backup"""
        api_key = os.getenv('TOGETHER_API_KEY')
        if not api_key:
            return None
        
        try:
            response = requests.post(
                'https://api.together.xyz/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Llama-2-7b-chat-hf',
                    'messages': [
                        {'role': 'user', 'content': f"As an AI assistant, provide a {response_type} response to: {query}"}
                    ],
                    'max_tokens': 2000,
                    'temperature': 0.7
                },
                timeout=8
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Together API error: {e}")
            return None
    
    @staticmethod
    def _build_prompt(query: str, response_type: str) -> str:
        """Build appropriate prompt based on response type"""
        prompts = {
            "helpful": f"Provide a helpful and informative response to: {query}",
            "essay": f"Write a comprehensive essay about: {query}",
            "explanation": f"Explain in detail: {query}",
            "analysis": f"Analyze the topic: {query}",
            "summary": f"Provide a clear summary of: {query}",
            "guide": f"Create a step-by-step guide for: {query}"
        }
        
        return prompts.get(response_type, f"Help the user with: {query}")
    
    @staticmethod
    def _intelligent_fallback(query: str, response_type: str) -> str:
        """Smart fallback when APIs are unavailable"""
        
        # Basic topic categorization for better fallbacks
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['programming', 'code', 'python', 'javascript', 'software']):
            return f"""**Programming Topic: {query}**

I'd be happy to help with programming! While my AI services are temporarily unavailable, here are some suggestions:

• Check official documentation for the specific language/framework
• Look at Stack Overflow for community solutions
• Try coding tutorials on platforms like freeCodeCamp or Codecademy
• Practice on coding challenge sites like LeetCode or HackerRank

I'll provide detailed programming assistance once my AI capabilities are restored."""

        elif any(word in query_lower for word in ['science', 'physics', 'chemistry', 'biology', 'math']):
            return f"""**Science/Math Topic: {query}**

This is an interesting scientific topic! While I'm experiencing connectivity issues:

• Consult peer-reviewed scientific journals
• Check educational resources like Khan Academy or MIT OpenCourseWare
• Look up the topic on NASA, NIH, or other official science websites
• Consider academic textbooks for in-depth understanding

I'll provide detailed scientific explanations once my systems are back online."""

        elif any(word in query_lower for word in ['history', 'historical', 'ancient', 'war', 'culture']):
            return f"""**Historical Topic: {query}**

History is fascinating! While my AI is temporarily offline:

• Check reputable sources like Encyclopedia Britannica
• Look at academic history websites and museums
• Read primary historical documents when available
• Consider books by respected historians

I'll give you detailed historical analysis once my capabilities return."""

        else:
            return f"""**Topic: {query}**

I'm currently experiencing technical difficulties with my AI services, but I'm here to help!

**Immediate suggestions:**
• Search for reliable sources on this topic
• Check academic or official websites
• Look for expert opinions and research
• Consider multiple perspectives on the subject

I'll provide comprehensive, AI-powered responses once my systems are restored. Thank you for your patience!"""

    @staticmethod
    def generate_human_like_response(session_id, user_message, response_type='helpful'):
        """
        Generate a human-like, context-aware response using memory and interaction optimizer

        Args:
            session_id: Unique identifier for the user session
            user_message: The user's message or question
            response_type: Type of response (helpful, essay, explanation, etc.)

        Returns:
            Human-like, contextually relevant response
        """
        history = conversation_memory.get_conversation_history(session_id)
        context = conversation_memory.get_user_context(session_id)
        patterns = conversation_memory.analyze_conversation_patterns(session_id)
        interaction_optimizer = HumanInteractionOptimizer()

        # Generate base response (from LLM or rules)
        base_response = ChatbotAI.generate_response(user_message, response_type)

        # Enhance with human interaction optimizer
        final_response = interaction_optimizer.make_response_conversational(
            base_response, user_message, context
        )
        # Save conversation
        conversation_memory.save_conversation(
            session_id=session_id,
            user_message=user_message,
            bot_response=final_response,
            message_type=response_type
        )
        return final_response
