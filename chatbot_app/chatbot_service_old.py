import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

# Try to import transformers for local models
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("Transformers not installed. Install with: pip install transformers torch")


class OpenSourceChatbotService:
    def __init__(self):
        self.use_local = os.getenv('USE_LOCAL_MODEL', 'True').lower() == 'true'
        self.hf_token = os.getenv('HUGGINGFACE_API_TOKEN')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        # For testing purposes, allow passing API key directly
        if not self.openrouter_key and hasattr(self, '_test_openrouter_key'):
            self.openrouter_key = self._test_openrouter_key

        print(f"✅ Chatbot initialized successfully with method: {self.method}")

        # Initialize the appropriate model/service
        if HAS_TRANSFORMERS and self.use_local:
import requests
from dotenv import load_dotenv

load_dotenv()

# Try to import transformers for local models
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("Transformers not installed. Install with: pip install transformers torch")


class OpenSourceChatbotService:
    def __init__(self):
        self.use_local = os.getenv('USE_LOCAL_MODEL', 'True').lower() == 'true'
        self.hf_token = os.getenv('HUGGINGFACE_API_KEY', None)
        
        if self.use_local and HAS_TRANSFORMERS:
            try:
                # Use a smaller, fast model for better performance
                model_name = "microsoft/DialoGPT-medium"  # Good conversational model
                # Alternative options:
                # model_name = "facebook/blenderbot-400M-distill"  # Another good option
                # model_name = "microsoft/DialoGPT-small"  # Faster, smaller model
                
                print(f"Loading local model: {model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
                
                # Add pad token if not present
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.generator = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
                
                self.method = "local_transformers"
                print("✅ Local model loaded successfully!")
                
            except Exception as e:
                print(f"❌ Failed to load local model: {e}")
                self.method = "simple"
        else:
            if self.openrouter_key:
                self.method = "openrouter_api"
                print("🚀 Using OpenRouter AI API")
            elif self.hf_token:
                self.method = "huggingface_api"
                print("🔗 Using Hugging Face Inference API")
            else:
                self.method = "simple"
                print("💡 Using simple responses (no API key provided)")

    async def get_response(self, message: str, conversation_history: list = None) -> str:
        """Get response using the best available method"""
        
        if self.method == "local_transformers":
            return await self._get_local_response(message, conversation_history)
        elif self.method == "openrouter_api":
            return await self._get_openrouter_response(message, conversation_history)
        elif self.method == "huggingface_api":
            return await self._get_huggingface_api_response(message)
        else:
            return await self._get_simple_response(message)

    async def _get_local_response(self, message: str, conversation_history: list = None) -> str:
        """Generate response using local transformers model"""
        try:
            # Prepare the input
            if conversation_history:
                # Take last few messages for context
                recent_history = conversation_history[-3:]  # Last 3 exchanges
                context = ""
                for msg in recent_history:
                    if msg["role"] == "user":
                        context += f"User: {msg['content']}\n"
                    else:
                        context += f"Bot: {msg['content']}\n"
                context += f"User: {message}\nBot:"
            else:
                context = f"User: {message}\nBot:"
            
            # Generate response
            response = self.generator(
                context,
                max_length=len(context.split()) + 50,  # Add 50 tokens for response
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                truncation=True
            )
            
            # Extract the bot's response
            full_response = response[0]['generated_text']
            bot_response = full_response[len(context):].strip()
            
            # Clean up the response
            if bot_response:
                # Remove any unwanted prefixes or suffixes
                bot_response = bot_response.split('\n')[0]  # Take first line
                bot_response = bot_response.replace('Bot:', '').strip()
                return bot_response
            else:
                return "I'm thinking about that... Could you rephrase your question?"
                
        except Exception as e:
            print(f"Error in local response generation: {e}")
            return await self._get_simple_response(message)

    async def _get_huggingface_api_response(self, message: str) -> str:
        """Generate response using Hugging Face Inference API with better free models"""
        try:
            # Use different models based on the task
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["code", "program", "python", "javascript"]):
                # Use a code-focused model
                API_URL = "https://api-inference.huggingface.co/models/microsoft/CodeGPT-small-py"
                payload = {
                    "inputs": f"# Task: {message}\n# Code:",
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.3,
                        "return_full_text": False
                    }
                }
            else:
                # Use a general conversational model
                API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
                payload = {
                    "inputs": message,
                    "parameters": {
                        "max_length": 150,
                        "temperature": 0.7,
                        "return_full_text": False
                    }
                }
            
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '').strip()
                    if generated_text and len(generated_text) > 5:
                        return generated_text
            elif response.status_code == 503:
                return "The AI model is loading. Please try again in a moment, or I can help with my built-in knowledge!"
            
            # If API fails, return a helpful message
            return "I'm having trouble with the AI service right now, but I can still help with my built-in knowledge on coding, writing, math, and many other topics!"
            
        except Exception as e:
            print(f"Error with Hugging Face API: {e}")
            return "The AI service is temporarily unavailable, but I'm still here to help with coding, writing, math, and general questions!"

    async def _get_openrouter_response(self, message: str, conversation_history: list = None) -> str:
        """Generate response using OpenRouter API"""
        try:
            import json
            
            # Prepare conversation history
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses. For coding questions, provide working code examples. For math problems, show the solution. For writing tasks, give structured guidance."}
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    role = "assistant" if msg.get("message_type") == "assistant" else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # OpenRouter API request
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "meta-llama/llama-3.2-3b-instruct:free",  # Free model
                "messages": messages,
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    return content.strip()
            elif response.status_code == 401:
                return "❌ Invalid API key. Please check your OpenRouter API key."
            elif response.status_code == 402:
                return "💳 OpenRouter credits exhausted. The chatbot will use built-in responses."
            elif response.status_code == 429:
                return "⏱️ Rate limit reached. Please wait a moment and try again."
            else:
                return f"🔄 OpenRouter API error (status {response.status_code}). Using built-in responses."
            
        except Exception as e:
            print(f"Error with OpenRouter API: {e}")
            return await self._get_simple_response(message)

    async def _get_simple_response(self, message: str) -> str:
        """Enhanced rule-based responses - ALWAYS WORKS"""
        message_lower = message.lower().strip()
        
        # Mathematical calculations
        if self._is_math_expression(message):
            try:
                result = self._calculate_math(message)
                return f"The answer is: {result}"
            except:
                return "I can help with basic math! Try simple expressions like '2+3', '10-4', '6*7', or '15/3'."
        
        # Complex task detection (coding, writing, etc.)
        complex_tasks = [
            "write", "essay", "paragraph", "code", "program", "function", 
            "explain how", "create", "develop", "build", "design",
            "help me with", "can you", "generate", "make", "tutorial"
        ]
        
        if any(task in message_lower for task in complex_tasks):
            return await self._handle_complex_task(message)
        
        # Knowledge base responses
        knowledge_responses = {
            # Technology
            "python": "Python is a powerful programming language! It's great for web development, AI, data science, and automation. What specifically about Python interests you?",
            "javascript": "JavaScript is the language of the web! It runs in browsers and servers (Node.js). Are you working on any JavaScript projects?",
            "django": "Django is a high-level Python web framework that's perfect for building robust web applications quickly and securely!",
            "react": "React is a popular JavaScript library for building user interfaces, especially single-page applications. It's component-based and very efficient!",
            
            # Programming concepts
            "api": "An API (Application Programming Interface) is a way for different software applications to communicate with each other. Think of it as a waiter in a restaurant - it takes your request and brings back the response!",
            "database": "A database is like a digital filing cabinet that stores and organizes data. Popular types include SQL (like PostgreSQL, MySQL) and NoSQL (like MongoDB).",
            "machine learning": "Machine Learning is a type of AI where computers learn patterns from data to make predictions or decisions. It's used everywhere from recommendation systems to self-driving cars!",
            
            # Science & Math
            "math": "Mathematics is the language of the universe! From basic arithmetic to advanced calculus, it helps us understand patterns and solve problems. What area of math interests you?",
            "physics": "Physics explores how the universe works - from tiny atoms to massive galaxies! It covers mechanics, thermodynamics, quantum physics, and more.",
            "chemistry": "Chemistry is the study of matter and how it changes. It's like cooking but with molecules! What chemistry topic are you curious about?",
            
            # General knowledge
            "history": "History helps us understand how we got to where we are today. From ancient civilizations to modern events, there's always something fascinating to learn!",
            "geography": "Geography is about places, people, and the environment. It includes physical features like mountains and rivers, as well as human settlements and cultures.",
            "space": "Space is incredibly vast and mysterious! We've learned so much about planets, stars, galaxies, and black holes, but there's still so much to discover.",
            
            # Health & Lifestyle
            "exercise": "Regular exercise is great for both physical and mental health! It can include cardio, strength training, yoga, or even just walking. What type of activity do you enjoy?",
            "nutrition": "Good nutrition fuels your body and mind! A balanced diet with fruits, vegetables, proteins, and whole grains provides the energy and nutrients you need.",
            "sleep": "Quality sleep is crucial for health, memory, and performance. Most adults need 7-9 hours per night. Good sleep hygiene can really make a difference!",
            
            # Business & Career
            "career": "Career development is important for personal growth and satisfaction. It involves building skills, networking, and finding work that aligns with your values and goals.",
            "business": "Business is about creating value for customers while generating profit. It involves strategy, marketing, operations, finance, and leadership.",
            "entrepreneurship": "Entrepreneurship is about identifying opportunities and creating innovative solutions. It requires creativity, risk-taking, and persistence!",
        }
        
        # Check for knowledge base topics first
        for topic, response in knowledge_responses.items():
            if topic in message_lower:
                return response
        
        # Enhanced question detection and responses
        if "?" in message:
            if any(word in message_lower for word in ["what is", "what are", "define", "explain"]):
                topic = message_lower.replace("what is", "").replace("what are", "").replace("define", "").replace("explain", "").replace("?", "").strip()
                if len(topic) > 2:
                    return f"That's a great question about {topic}! While I have basic knowledge on many topics, I'd recommend checking authoritative sources for detailed information. What specific aspect of {topic} interests you most?"
            
            if any(word in message_lower for word in ["how to", "how do", "how can"]):
                return "That's a practical question! For step-by-step guidance, I'd suggest looking up tutorials or guides from reliable sources. I can try to give you general direction - what specifically are you trying to accomplish?"
            
            if any(word in message_lower for word in ["why", "reason", "because"]):
                return "That's a thoughtful 'why' question! Understanding the reasons behind things is important. While I can share general knowledge, complex topics often have multiple perspectives worth exploring."
            
            if any(word in message_lower for word in ["when", "time", "date"]):
                return "That's a timing-related question! For current or historical dates and times, I'd recommend checking reliable sources as I don't have access to real-time information."
            
            if any(word in message_lower for word in ["where", "location", "place"]):
                return "That's a location-based question! For specific places, directions, or geographic information, I'd suggest using maps or travel resources for the most accurate details."
        
        # Enhanced conversational responses with more intelligence
        greetings = {
            "hello": "Hello! I can help with math, answer questions, and chat. Try asking me '3+5' or 'What is Python?'",
            "hi": "Hi there! I'm ready to help with calculations, questions, or just conversation. What's on your mind?",
            "hey": "Hey! I can do math, answer questions about technology, science, and more. What would you like to know?",
            "good morning": "Good morning! Hope you're having a great day! I can help with math problems or answer questions.",
            "good afternoon": "Good afternoon! How's your day going? I'm here to help with calculations or any questions.",
            "good evening": "Good evening! How can I assist you? I can solve math problems or discuss various topics.",
        }
        
        for greeting, response in greetings.items():
            if greeting in message_lower:
                return response
        
        # Status and capability questions
        status_responses = {
            "how are you": "I'm doing well, thank you! I'm here to help answer questions and have conversations. How are you doing?",
            "what can you do": "I can chat with you, answer questions on various topics, and help with general information! I'm particularly good with technology, science, and everyday topics. What would you like to know about?",
            "who are you": "I'm an AI assistant built with Django and Chainlit! I use a combination of programmed knowledge and conversational AI to help answer questions and chat. What can I help you with?",
            "help": "I'm here to help! You can ask me about technology, science, general knowledge, or just have a conversation. Try asking questions like 'What is Python?' or 'Tell me about space' - what interests you?",
        }
        
        for key, response in status_responses.items():
            if key in message_lower:
                return response
        
        # Fun and entertainment
        if any(word in message_lower for word in ["joke", "funny", "humor"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "I told my computer a joke about UDP... but I'm not sure if it got it! 💻",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "What's a computer's favorite snack? Microchips! 🖥️",
            ]
            import random
            return random.choice(jokes)
        
        # Learning and education
        if any(word in message_lower for word in ["learn", "study", "education", "school", "university"]):
            return "Learning is fantastic! Whether it's formal education or self-directed learning, there are so many resources available online. What subject are you interested in learning about?"
        
        # Technology-specific responses
        if any(word in message_lower for word in ["coding", "programming", "software", "development"]):
            return "Programming is an exciting field! There are many languages and frameworks to choose from depending on your goals. Are you just starting out or working on something specific?"
        
        # Problem-solving
        if any(word in message_lower for word in ["problem", "issue", "error", "bug", "fix"]):
            return "Problem-solving is a key skill! Breaking down complex issues into smaller parts often helps. What kind of problem are you working on? I might be able to offer some general guidance."
        
        # Generic intelligent response based on message content
        words = message_lower.split()
        if len(words) > 3:
            return f"I can see you're asking about something related to '{' '.join(words[:3])}...'. While I have general knowledge on many topics, I'd be happy to discuss what I know or point you toward better resources. What specifically would you like to know?"
        elif len(words) == 1:
            return f"'{message}' - that's an interesting topic! Could you tell me more about what you'd like to know? I'm here to help with information and conversation."
        else:
            return f"That's an interesting point about '{message}'. I'd love to hear more about what you're thinking or what specific information you're looking for!"

    async def _handle_complex_task(self, message: str) -> str:
        """Handle complex tasks like coding, writing, etc."""
        message_lower = message.lower()
        
        # Try Hugging Face API first if available
        if hasattr(self, 'huggingface_api_token') and self.huggingface_api_token:
            try:
                return await self._get_huggingface_api_response(message)
            except Exception as e:
                print(f"Hugging Face API failed: {e}")
        
        # Fallback to enhanced rule-based responses for complex tasks
        if any(word in message_lower for word in ["write", "essay", "paragraph"]):
            return self._writing_assistance(message)
        elif any(word in message_lower for word in ["code", "program", "function", "python", "javascript"]):
            return self._coding_assistance(message)
        elif any(word in message_lower for word in ["explain how", "tutorial", "step by step"]):
            return self._tutorial_assistance(message)
        else:
            return self._general_complex_assistance(message)
    
    def _writing_assistance(self, message: str) -> str:
        """Provide writing assistance"""
        if "essay" in message.lower():
            return """I can help you structure an essay! Here's a basic framework:

📝 **Essay Structure:**
1. **Introduction** - Hook, background, thesis statement
2. **Body Paragraphs** - Each with topic sentence, evidence, analysis
3. **Conclusion** - Restate thesis, summarize key points

**Tips:**
- Start with an outline
- Use transitions between paragraphs
- Support claims with evidence
- Revise and proofread

What topic are you writing about? I can provide more specific guidance!"""
        
        elif "paragraph" in message.lower():
            return """Here's how to write a strong paragraph:

📄 **Paragraph Structure:**
1. **Topic Sentence** - Main idea
2. **Supporting Details** - Evidence and examples
3. **Analysis** - Explain the significance
4. **Concluding Sentence** - Wrap up the idea

**Length:** Usually 4-6 sentences for academic writing.

What's your paragraph topic? I can help you develop it further!"""
        
        return """I can help with various writing tasks:
- Essays (structure, thesis development)
- Paragraphs (organization, flow)
- Creative writing (stories, descriptions)
- Business writing (emails, reports)

What specific writing help do you need?"""
    
    def _coding_assistance(self, message: str) -> str:
        """Provide coding assistance"""
        message_lower = message.lower()
        
        if "python" in message_lower:
            if "function" in message_lower:
                return """Here's a Python function template:

```python
def function_name(parameters):
    \"\"\"
    Brief description of what the function does
    
    Args:
        param1: Description of parameter
        
    Returns:
        Description of return value
    \"\"\"
    # Your code here
    return result

# Example usage
result = function_name(arguments)
```

What kind of function are you trying to create?"""
            
            return """I can help with Python! Here are some basics:

🐍 **Python Fundamentals:**
- Variables: `name = "value"`
- Lists: `[1, 2, 3]`
- Dictionaries: `{"key": "value"}`
- Loops: `for item in list:`
- Conditions: `if condition:`

**Common patterns:**
- File reading: `with open("file.txt") as f:`
- Try/except: `try: code except Exception:`

What specific Python concept do you need help with?"""
        
        elif "javascript" in message_lower:
            return """I can help with JavaScript! Here are key concepts:

💻 **JavaScript Basics:**
- Variables: `let name = "value";`
- Arrays: `[1, 2, 3]`
- Objects: `{key: "value"}`
- Functions: `function name() {}`
- DOM: `document.getElementById("id")`

**Modern JS:**
- Arrow functions: `() => {}`
- Async/await: `async function()`
- Destructuring: `const {name} = object`

What JavaScript topic interests you?"""
        
        return """I can help with coding in various languages:

💻 **Languages I can assist with:**
- Python (web development, data science)
- JavaScript (frontend, backend)
- HTML/CSS (web design)
- SQL (database queries)

**Programming concepts:**
- Functions and classes
- Loops and conditions
- Data structures
- Error handling

What programming challenge are you working on?"""
    
    def _tutorial_assistance(self, message: str) -> str:
        """Provide tutorial/how-to assistance"""
        return """I can help explain concepts step-by-step! 

📚 **I can provide tutorials on:**
- Programming concepts
- Problem-solving approaches
- Study techniques
- Project planning

To give you the best help, could you be more specific about what you'd like to learn? For example:
- "Explain how to create a Python function"
- "How to structure an essay"
- "Steps to learn web development"

What topic would you like a tutorial on?"""
    
    def _general_complex_assistance(self, message: str) -> str:
        """Handle other complex requests"""
        return """I'm here to help with complex tasks! 🚀

**I can assist with:**
- ✅ Writing (essays, paragraphs, creative writing)
- ✅ Coding (Python, JavaScript, web development)
- ✅ Math and calculations
- ✅ Explanations and tutorials
- ✅ Problem-solving approaches
- ✅ Learning strategies

For the best help, try to be specific about what you need. For example:
- "Write a Python function to calculate area"
- "Help me structure a 5-paragraph essay"
- "Explain how APIs work"

What specific task can I help you with?"""

    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())

    def format_conversation_history(self, messages) -> list:
        """Convert database messages to format for AI models"""
        formatted = []
        for msg in messages:
            role = "assistant" if msg.message_type == "assistant" else "user"
            formatted.append({"role": role, "content": msg.content})
        return formatted

    def _is_math_expression(self, text: str) -> bool:
        """Check if the text is a mathematical expression"""
        # Clean the text - remove common question words but keep the math
        import re
        original_text = text
        text = re.sub(r'\b(what is|what\'s|calculate|solve|compute)\b', '', text.lower()).strip()
        
        # Remove spaces
        text = text.replace(" ", "")
        
        # Enhanced patterns for math expressions including power operations
        simple_patterns = [
            r'^\d+[\+\-\*/]\d+$',  # Simple: 3+5, 10-2, etc.
            r'^\d+[\+\-\*/]\d+[\+\-\*/]\d+$',  # Chain: 3+5-2
            r'^\d+\*\d+[\+\-\*/]\d+$',  # Order of operations: 3*5+2
            r'^\d+[\+\-]\d+\*\d+$',  # Order of operations: 3+5*2
            r'^\(\d+[\+\-\*/]\d+\)\*\d+$',  # Parentheses: (3+5)*2
            r'^\d+\*\(\d+[\+\-\*/]\d+\)$',  # Parentheses: 2*(3+5)
            r'^\(\d+[\+\-\*/]\d+\)$',  # Simple parentheses: (3+5)
            r'^\d+(\.\d+)?[\+\-\*/]\d+(\.\d+)?$',  # Decimals: 3.5+2.1
            r'^\d+\*\*\d+$',  # Power: 5**2, 2**3
            r'^\d+\^\d+$',   # Alternative power: 5^2
        ]
        
        # Check if it contains only valid math characters
        pattern = r'^[0-9+\-*/().^*]+$'
        
        # Check if it matches any math pattern
        return bool(re.match(pattern, text)) and any(re.match(p, text) for p in simple_patterns)

    def _calculate_math(self, expression: str) -> str:
        """Safely calculate mathematical expressions"""
        try:
            # Clean the expression - remove question words
            import re
            original_expr = expression
            expression = re.sub(r'\b(what is|what\'s|calculate|solve|compute)\b', '', expression.lower()).strip()
            
            # Remove spaces and validate
            expression = expression.replace(" ", "")
            
            # Convert ^ to ** for power operations
            expression = expression.replace("^", "**")
            
            # Only allow safe characters (now including * for power)
            if not re.match(r'^[0-9+\-*/().^*]+$', expression):
                raise ValueError("Invalid characters")
            
            # Evaluate safely (only basic math)
            allowed_names = {
                "__builtins__": {},
                "__name__": "__main__",
                "__doc__": None,
            }
            
            result = eval(expression, allowed_names, {})
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.6g}"  # Remove trailing zeros
            else:
                return str(result)
                
        except ZeroDivisionError:
            return "Error: Cannot divide by zero!"
        except:
            raise ValueError("Invalid math expression")


# Backwards compatibility
ChatbotService = OpenSourceChatbotService

# Simple fallback chatbot (same as before)
class SimpleChatbot:
    def __init__(self):
        self.responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing well, thank you! How are you?",
            "bye": "Goodbye! Have a great day!",
            "help": "I'm here to help! You can ask me questions and I'll do my best to assist you.",
        }

    async def get_response(self, message: str, conversation_history: list = None) -> str:
        """Simple pattern-based responses"""
        message_lower = message.lower().strip()
        
        for key, response in self.responses.items():
            if key in message_lower:
                return response
        
        return "I'm a simple chatbot. I can respond to basic greetings like hello, hi, how are you, bye, and help."

    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())
