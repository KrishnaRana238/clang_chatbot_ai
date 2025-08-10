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

# Import OpenAI client for OpenRouter
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("OpenAI library not installed. Install with: pip install openai")

# Import Cohere client
try:
    import cohere
    HAS_COHERE = True
except ImportError:
    HAS_COHERE = False
    print("Cohere library not installed. Install with: pip install cohere")

# Import Groq client
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False
    print("Groq library not installed. Install with: pip install groq")

# Import Mistral client
try:
    from mistralai.client import MistralClient
    HAS_MISTRAL = True
except ImportError:
    HAS_MISTRAL = False
    print("Mistral library not installed. Install with: pip install mistralai")

# Import Together AI client
try:
    from together import Together
    HAS_TOGETHER = True
except ImportError:
    HAS_TOGETHER = False
    print("Together AI library not installed. Install with: pip install together")

# Import Advanced LLM Service
try:
    from .advanced_llm_service import AdvancedLLMService, integrate_with_existing_chatbot
    HAS_ADVANCED_LLM = True
except ImportError:
    HAS_ADVANCED_LLM = False
    print("Advanced LLM service not available")


class OpenSourceChatbotService:
    def __init__(self):
        self.use_local = os.getenv('USE_LOCAL_MODEL', 'True').lower() == 'true'
        self.hf_token = os.getenv('HUGGINGFACE_API_TOKEN')
        
        # Configure multiple API providers
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.cohere_key = os.getenv('COHERE_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.mistral_key = os.getenv('MISTRAL_API_KEY')
        self.together_key = os.getenv('TOGETHER_API_KEY')
        
        # Create list of available providers
        self.providers = []
        if self.openrouter_key and HAS_OPENAI:
            self.providers.append({
                'name': 'openrouter',
                'client': None,
                'key': self.openrouter_key,
                'models': ['google/gemma-2-9b-it:free', 'tngtech/deepseek-r1t2-chimera:free']
            })
        if self.cohere_key and HAS_COHERE:
            self.providers.append({
                'name': 'cohere',
                'client': None,
                'key': self.cohere_key,
                'models': ['command-r', 'command-r-plus', 'command']
            })
        if self.groq_key and HAS_GROQ:
            self.providers.append({
                'name': 'groq',
                'client': None,
                'key': self.groq_key,
                'models': ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
            })
        if self.mistral_key and HAS_MISTRAL:
            self.providers.append({
                'name': 'mistral',
                'client': None,
                'key': self.mistral_key,
                'models': ['mistral-tiny', 'mistral-small', 'mistral-medium', 'mistral-large-latest']
            })
        if self.together_key and HAS_TOGETHER:
            self.providers.append({
                'name': 'together',
                'client': None,
                'key': self.together_key,
                'models': ['meta-llama/Llama-2-70b-chat-hf', 'meta-llama/Meta-Llama-3-70B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1', 'togethercomputer/RedPajama-INCITE-7B-Chat']
            })
        
        self.current_provider_index = 0  # Track which provider we're currently using
        
        # Determine which method to use
        if HAS_TRANSFORMERS and self.use_local:
            self.method = "local_transformers"
            print("🤖 Loading local transformers model...")
            try:
                # Initialize local model (simplified for demo)
                self.model_name = "microsoft/DialoGPT-medium"
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                print("✅ Local model loaded successfully!")
            except Exception as e:
                print(f"❌ Failed to load local model: {e}")
                self.method = "simple"
        else:
            if self.providers:
                self.method = "multi_api"
                print(f"🚀 Using Multi-API with {len(self.providers)} provider(s):")
                for i, provider in enumerate(self.providers):
                    print(f"  {i+1}. {provider['name'].title()} API")
                # Initialize first provider
                self._init_current_provider()
            elif self.hf_token:
                self.method = "huggingface_api"
                print("� Using Hugging Face Inference API")
            else:
                self.method = "simple"
                print("💡 Using simple responses (no API key provided)")
        
        print(f"✅ Chatbot initialized successfully with method: {self.method}")
        
        # Initialize Advanced LLM Service
        self.advanced_llm = None
        if HAS_ADVANCED_LLM:
            try:
                self.advanced_llm = integrate_with_existing_chatbot(self)
                print("🧠 Advanced LLM service integrated - Enhanced complex question handling enabled")
            except Exception as e:
                print(f"⚠️  Advanced LLM integration failed: {e}")

    def _init_current_provider(self):
        """Initialize the current API provider"""
        if self.current_provider_index < len(self.providers):
            provider = self.providers[self.current_provider_index]
            provider_name = provider['name']
            
            try:
                if provider_name == 'openrouter':
                    provider['client'] = OpenAI(
                        api_key=provider['key'],
                        base_url="https://openrouter.ai/api/v1",
                    )
                    print(f"🔑 OpenRouter API initialized")
                    
                elif provider_name == 'cohere':
                    provider['client'] = cohere.Client(api_key=provider['key'])
                    print(f"🔑 Cohere API initialized")
                    
                elif provider_name == 'groq':
                    provider['client'] = Groq(api_key=provider['key'])
                    print(f"🔑 Groq API initialized")
                    
                elif provider_name == 'mistral':
                    provider['client'] = MistralClient(api_key=provider['key'])
                    print(f"🔑 Mistral AI initialized")
                    
                elif provider_name == 'together':
                    provider['client'] = Together(api_key=provider['key'])
                    print(f"🔑 Together AI initialized")
                    
                return True
                
            except Exception as e:
                print(f"❌ Failed to initialize {provider_name}: {e}")
                return False
        return False
    
    def _switch_to_next_provider(self):
        """Switch to the next available API provider"""
        if self.current_provider_index + 1 < len(self.providers):
            self.current_provider_index += 1
            next_provider = self.providers[self.current_provider_index]['name']
            print(f"🔄 Switching to {next_provider.title()} API")
            return self._init_current_provider()
        else:
            print("❌ All API providers exhausted, falling back to built-in responses")
            return False

    async def get_response(self, message: str, conversation_history: list = None) -> str:
        """Get response using the best available method with advanced LLM enhancement"""
        
        message_lower = message.lower().strip()
        
        # Handle special commands FIRST, before any LLM processing
        if message_lower.startswith('/'):
            return await self._handle_special_commands(message_lower)
        
        # Check if we should use advanced LLM for complex questions
        if self.advanced_llm:
            try:
                # Analyze question complexity
                complexity_analysis = self.advanced_llm.analyze_question_complexity(message)
                
                # Use advanced LLM for medium/complex questions
                if complexity_analysis['complexity'] in ['medium', 'complex']:
                    print(f"🧠 Using Advanced LLM for {complexity_analysis['complexity']} question")
                    enhanced_response = await self.advanced_llm.generate_enhanced_response(
                        message, conversation_history
                    )
                    # Ensure response is not None
                    if enhanced_response and enhanced_response.get('response'):
                        return enhanced_response['response']
                    else:
                        print("⚠️ Advanced LLM returned None or empty response, falling back")
                        # Fall through to standard processing
            except Exception as e:
                print(f"⚠️  Advanced LLM failed, falling back to standard processing: {e}")
        
        # Standard processing for simple questions or if advanced LLM unavailable
        if self.method == "local_transformers":
            return await self._get_local_response(message, conversation_history)
        elif self.method == "multi_api":
            return await self._get_multi_api_response(message, conversation_history)
        elif self.method == "huggingface_api":
            return await self._get_huggingface_api_response(message)
        else:
            return await self._get_simple_response(message)

    async def _get_local_response(self, message: str, conversation_history: list = None) -> str:
        """Generate response using local transformers model"""
        try:
            # Prepare input for the model
            context = "Human: " + message + " Clang:"
            
            # Tokenize and generate
            inputs = self.tokenizer.encode(context, return_tensors='pt')
            
            with torch.no_grad():
                response = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 50,
                    num_return_sequences=1,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            full_response = self.tokenizer.decode(response[0], skip_special_tokens=True)
            bot_response = full_response[len(context):].strip()
            
            return bot_response if bot_response else "I'm thinking... could you ask me something else?"
            
        except Exception as e:
            print(f"Error with local model: {e}")
            return await self._get_simple_response(message)

    async def _get_multi_api_response(self, message: str, conversation_history: list = None) -> str:
        """Generate response using multiple API providers with intelligent fallback"""
        try:
            # Check for special commands first
            message_lower = message.lower().strip()
            if message_lower.startswith('/'):
                return await self._handle_special_commands(message_lower)
            
            # Check for model comparison command
            if message_lower.startswith('compare models:') or message_lower.startswith('test models:'):
                query = message[len('compare models:'):].strip() or message[len('test models:'):].strip()
                if query:
                    return await self._test_all_providers(query)
                else:
                    return "Please provide a query for model comparison. Example: 'compare models: What is AI?'"
            
            # Check for mathematical expressions
            if self._is_math_expression(message):
                try:
                    result = self._calculate_math(message)
                    if not result.startswith("Error:"):
                        return f"🧮 Mathematical Result: {result}"
                    else:
                        print(f"❌ Math calculation error: {result}")
                        # Continue to AI providers if calculation fails
                except Exception as e:
                    print(f"❌ Math parsing error: {e}")
                    # Continue to AI providers if parsing fails
            
            # Check for prime number queries
            if self._is_prime_query(message):
                return self._handle_prime_query(message)
            
            # Get response from current provider
            current_provider = self.providers[self.current_provider_index]
            
            if current_provider['name'] == 'openrouter':
                return await self._get_openrouter_api_response(message, conversation_history, current_provider)
            elif current_provider['name'] == 'cohere':
                return await self._get_cohere_api_response(message, conversation_history, current_provider)
            elif current_provider['name'] == 'groq':
                return await self._get_groq_api_response(message, conversation_history, current_provider)
            elif current_provider['name'] == 'mistral':
                return await self._get_mistral_api_response(message, conversation_history, current_provider)
            elif current_provider['name'] == 'together':
                return await self._get_together_api_response(message, conversation_history, current_provider)
            else:
                return await self._get_simple_response(message)
                
        except Exception as e:
            error_msg = str(e)
            print(f"Error with {self.providers[self.current_provider_index]['name']} API: {e}")
            
            # Try to switch to next provider on error
            if self._switch_to_next_provider():
                print("🔄 Retrying with next provider...")
                try:
                    return await self._get_multi_api_response(message, conversation_history)
                except:
                    pass
            
            # Fall back to simple responses
            return await self._get_simple_response(message)

    async def _get_openrouter_api_response(self, message: str, conversation_history: list, provider: dict) -> str:
        """Generate response using OpenRouter API"""
        # Prepare conversation history
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."}
        ]
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-6:]:  # Last 6 messages for context
                role = "assistant" if msg.get("message_type") == "assistant" else "user"
                messages.append({"role": role, "content": msg.get("content", "")})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Intelligent model selection for OpenRouter
        selected_model = self._select_openrouter_model(message)
        
        # Make API call
        completion = provider['client'].chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8007",
                "X-Title": "Clang AI Assistant Multi-Provider",
            },
            model=selected_model,
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )
        
        response_content = completion.choices[0].message.content
        return response_content.strip() if response_content else "I'm having trouble generating a response right now."
    
    async def _get_cohere_api_response(self, message: str, conversation_history: list, provider: dict) -> str:
        """Generate response using Cohere API"""
        try:
            # Prepare conversation history for Cohere format
            chat_history = []
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    role = "CHATBOT" if msg.get("message_type") == "assistant" else "USER"
                    chat_history.append({
                        "role": role,
                        "message": msg.get("content", "")
                    })
            
            # Select Cohere model based on task complexity
            selected_model = self._select_cohere_model(message)
            print(f"🔷 Using Cohere {selected_model} model")
            
            # Make API call to Cohere
            response = provider['client'].chat(
                model=selected_model,
                message=message,
                chat_history=chat_history,
                max_tokens=400,
                temperature=0.7
            )
            
            return response.text.strip() if response.text else "I'm having trouble generating a response right now."
            
        except Exception as e:
            print(f"Cohere API error: {e}")
            raise e  # Re-raise to trigger provider switching

    async def _get_groq_api_response(self, message: str, conversation_history: list, provider: dict) -> str:
        """Generate response using Groq API for ultra-fast inference"""
        try:
            # Prepare conversation history for Groq (OpenAI-compatible format)
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."}
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    role = "assistant" if msg.get("message_type") == "assistant" else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Select Groq model based on task complexity
            selected_model = self._select_groq_model(message)
            print(f"⚡ Using Groq {selected_model} model")
            
            # Make API call to Groq (ultra-fast inference)
            completion = provider['client'].chat.completions.create(
                model=selected_model,
                messages=messages,
                max_tokens=400,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            
            response_content = completion.choices[0].message.content
            return response_content.strip() if response_content else "I'm having trouble generating a response right now."
            
        except Exception as e:
            print(f"Groq API error: {e}")
            raise e  # Re-raise to trigger provider switching

    def _select_openrouter_model(self, message: str) -> str:
        """Select best OpenRouter model based on task"""
        # Check if user has manually selected a model
        if hasattr(self, '_forced_model') and self._forced_model:
            print(f"🔒 Using manually selected model")
            return self._forced_model
        
        message_lower = message.lower()
        
        # Task classification for OpenRouter models
        if any(word in message_lower for word in [
            "analyze", "reasoning", "complex", "problem", "solve", "logic", 
            "think", "reason", "explain how", "why", "because", "theory",
            "philosophy", "meaning", "deep", "analyze", "examine", "pros and cons",
            "code", "program", "function", "debug", "algorithm", "programming"
        ]):
            selected = "tngtech/deepseek-r1t2-chimera:free"
            print(f"🧠 Using DeepSeek model for complex task")
            return selected
        else:
            selected = "google/gemma-2-9b-it:free"
            print(f"💬 Using Gemini model for general conversation")
            return selected
    
    def _select_cohere_model(self, message: str) -> str:
        """Select best Cohere model based on task"""
        message_lower = message.lower()
        
        # Task classification for Cohere models
        if any(word in message_lower for word in [
            "complex", "detailed", "analysis", "research", "comprehensive",
            "technical", "professional", "business", "academic"
        ]):
            return "command-r-plus"  # Most capable model
        elif any(word in message_lower for word in [
            "code", "program", "script", "technical", "development"
        ]):
            return "command-r"  # Good for technical tasks
        else:
            return "command"  # Fast general purpose model
    
    def _select_groq_model(self, message: str) -> str:
        """Select best Groq model based on task complexity"""
        message_lower = message.lower()
        
        # Task classification for Groq models
        if any(word in message_lower for word in [
            "complex", "detailed", "comprehensive", "analysis", "research",
            "technical", "professional", "academic", "reasoning", "logic"
        ]):
            return "llama3-70b-8192"  # Most capable model for complex tasks
        elif any(word in message_lower for word in [
            "code", "program", "script", "algorithm", "function", "debug",
            "math", "calculation", "problem solving"
        ]):
            return "mixtral-8x7b-32768"  # Great for coding and math
        else:
            return "llama3-8b-8192"  # Fast general purpose model

    async def _get_mistral_api_response(self, message: str, conversation_history: list, provider: dict) -> str:
        """Generate response using Mistral AI API"""
        try:
            # Prepare conversation history for Mistral
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."}
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    role = "assistant" if msg.get("message_type") == "assistant" else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Select Mistral model based on task complexity
            selected_model = self._select_mistral_model(message)
            print(f"🔮 Using Mistral {selected_model} model")
            
            # Make API call to Mistral
            
            # Convert messages to Mistral format
            response = provider['client'].chat(
                model=selected_model,
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            return response_content.strip() if response_content else "I'm having trouble generating a response right now."
            
        except Exception as e:
            print(f"Mistral API error: {e}")
            raise e  # Re-raise to trigger provider switching

    def _select_mistral_model(self, message: str) -> str:
        """Select best Mistral model based on task complexity"""
        message_lower = message.lower()
        
        # Task classification for Mistral models
        if any(word in message_lower for word in [
            "complex", "detailed", "comprehensive", "analysis", "research",
            "technical", "professional", "academic", "reasoning", "logic",
            "creative writing", "story", "essay", "poem", "creative"
        ]):
            return "mistral-large-latest"  # Most capable model for complex tasks
        elif any(word in message_lower for word in [
            "code", "program", "script", "algorithm", "function", "debug",
            "technical", "software", "development"
        ]):
            return "mistral-medium"  # Good for coding tasks
        elif any(word in message_lower for word in [
            "translate", "translation", "language", "french", "spanish", 
            "german", "italian", "portuguese"
        ]):
            return "mistral-small"  # Good for multilingual tasks
        else:
            return "mistral-tiny"  # Fast general purpose model

    async def _get_together_api_response(self, message: str, conversation_history: list, provider: dict) -> str:
        """Generate response using Together AI API"""
        try:
            # Prepare conversation history for Together AI
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."}
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    role = "assistant" if msg.get("message_type") == "assistant" else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Select Together model based on task complexity
            selected_model = self._select_together_model(message)
            print(f"🚀 Using Together AI {selected_model} model")
            
            # Make API call to Together AI
            response = provider['client'].chat.completions.create(
                model=selected_model,
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            return response_content.strip() if response_content else "I'm having trouble generating a response right now."
            
        except Exception as e:
            print(f"Together AI API error: {e}")
            raise e  # Re-raise to trigger provider switching

    def _select_together_model(self, message: str) -> str:
        """Select best Together AI model based on task complexity"""
        message_lower = message.lower()
        
        # Task classification for Together AI models
        if any(word in message_lower for word in [
            "complex", "detailed", "comprehensive", "analysis", "research",
            "technical", "professional", "academic", "reasoning", "logic"
        ]):
            return "meta-llama/Meta-Llama-3-70B-Instruct"  # Most capable model for complex tasks
        elif any(word in message_lower for word in [
            "code", "program", "script", "algorithm", "function", "debug",
            "technical", "software", "development"
        ]):
            return "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Good for coding tasks
        elif any(word in message_lower for word in [
            "creative writing", "story", "essay", "poem", "creative",
            "write", "compose", "imagine", "fictional"
        ]):
            return "meta-llama/Llama-2-70b-chat-hf"  # Good for creative tasks
        else:
            return "togethercomputer/RedPajama-INCITE-7B-Chat"  # Fast general purpose model

    async def _test_all_providers(self, message: str) -> str:
        """Test a message against all available providers for comparison"""
        results = {}
        
        for i, provider in enumerate(self.providers):
            try:
                provider_name = provider['name']
                print(f"Testing {provider_name}...")
                
                if provider_name == 'openrouter':
                    response = await self._get_openrouter_api_response(message, None, provider)
                    results[f"OpenRouter"] = {
                        "response": response,
                        "status": "success"
                    }
                elif provider_name == 'cohere':
                    response = await self._get_cohere_api_response(message, None, provider)
                    results[f"Cohere"] = {
                        "response": response,
                        "status": "success"
                    }
                elif provider_name == 'groq':
                    response = await self._get_groq_api_response(message, None, provider)
                    results[f"Groq"] = {
                        "response": response,
                        "status": "success"
                    }
                elif provider_name == 'mistral':
                    response = await self._get_mistral_api_response(message, None, provider)
                    results[f"Mistral"] = {
                        "response": response,
                        "status": "success"
                    }
                elif provider_name == 'together':
                    response = await self._get_together_api_response(message, None, provider)
                    results[f"Together"] = {
                        "response": response,
                        "status": "success"
                    }
                    
            except Exception as e:
                provider_name = provider['name']
                results[f"{provider_name.title()}"] = {
                    "response": f"Error: {str(e)}",
                    "status": "error"
                }
        
        # Format comparison results
        comparison = "🔥 Multi-Provider Comparison Results:\n\n"
        for provider_name, result in results.items():
            status = "✅" if result['status'] == 'success' else "❌"
            response_text = result['response'][:150] + "..." if len(result['response']) > 150 else result['response']
            comparison += f"{status} **{provider_name}**: {response_text}\n\n"
        
        return comparison

    async def _get_openrouter_response(self, message: str, conversation_history: list = None) -> str:
        """Generate response using OpenRouter API with intelligent model selection"""
        try:
            # Check for special commands first
            message_lower = message.lower().strip()
            if message_lower.startswith('/'):
                return await self._handle_special_commands(message_lower)
            
            # Check for model comparison command
            if message_lower.startswith('compare models:') or message_lower.startswith('test models:'):
                query = message[len('compare models:'):].strip() or message[len('test models:'):].strip()
                if query:
                    results = await self._test_all_models(query)
                    response = "🔥 **Model Comparison Results:**\n\n"
                    for model, result in results.items():
                        model_name = model.split('/')[-1].replace(':free', '').replace('-', ' ').title()
                        status = "✅" if result['status'] == 'success' else "❌"
                        response_text = result.get('response', '') or ''  # Handle None response
                        response_text = response_text[:150] + "..." if len(response_text) > 150 else response_text
                        response += f"{status} **{model_name}**: {response_text}\n\n"
                    return response
                else:
                    return "Please provide a query for model comparison. Example: 'compare models: What is AI?'"
            
            # Check for mathematical expressions
            if self._is_math_expression(message):
                try:
                    result = self._calculate_math(message)
                    return f"🧮 Mathematical Result: {result}"
                except:
                    pass  # Fall back to AI if math parsing fails
            
            # Check for prime number queries
            if self._is_prime_query(message):
                return self._handle_prime_query(message)
            
            # Prepare conversation history
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses. For coding questions, provide working code examples. For math problems, show the solution step by step. For writing tasks, give structured guidance."}
            ]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    role = "assistant" if msg.get("message_type") == "assistant" else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Intelligent model selection based on the task
            selected_model = self._select_best_model(message)
            
            # Make API call using OpenAI client
            completion = self.openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:8002",  # Your site URL
                    "X-Title": "Clang AI Assistant",  # Your site name
                },
                model=selected_model,
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            response_content = completion.choices[0].message.content
            return response_content.strip() if response_content else "I'm having trouble generating a response right now."
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error with OpenRouter API (Key #{self.current_key_index + 1}): {e}")
            
            # Check if it's a credits/quota issue and we have backup keys
            if ("402" in error_msg or "credits" in error_msg.lower() or 
                "quota" in error_msg.lower() or "insufficient" in error_msg.lower()):
                
                # Try to switch to next API key
                if self._switch_to_next_key():
                    print("🔄 Retrying with backup API key...")
                    # Recursively retry with the new key
                    try:
                        return await self._get_openrouter_response(message, conversation_history)
                    except:
                        # If backup key also fails, fall back to simple responses
                        pass
                
                return "💳 All OpenRouter API credits exhausted. Using built-in responses."
            
            elif "401" in error_msg or "Unauthorized" in error_msg:
                # Try next key if unauthorized
                if self._switch_to_next_key():
                    print("🔄 Retrying with backup API key...")
                    try:
                        return await self._get_openrouter_response(message, conversation_history)
                    except:
                        pass
                
                return "❌ All API keys invalid. Please check your OpenRouter API keys."
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                return "⏱️ Rate limit reached. Please wait a moment and try again."
            else:
                # For other errors, try backup key once
                if self.current_key_index == 0 and len(self.openrouter_keys) > 1:
                    if self._switch_to_next_key():
                        print("🔄 Retrying with backup API key due to error...")
                        try:
                            return await self._get_openrouter_response(message, conversation_history)
                        except:
                            pass
                
                # Fall back to simple responses
                return await self._get_simple_response(message)

    def _select_best_model(self, message: str) -> str:
        """Intelligently select the best model based on the task"""
        
        # Check if user has manually selected a model
        if hasattr(self, '_forced_model') and self._forced_model:
            model_name = self._forced_model.split('/')[-1].replace(':free', '').replace('-', ' ').title()
            print(f"🔒 Using manually selected {model_name} model")
            return self._forced_model
        
        # Otherwise, use intelligent selection
        message_lower = message.lower()
        
        # Task classification for complex reasoning and analysis
        if any(word in message_lower for word in [
            "analyze", "reasoning", "complex", "problem", "solve", "logic", 
            "think", "reason", "explain how", "why", "because", "theory",
            "philosophy", "meaning", "deep", "analyze", "examine", "pros and cons",
            "advantages", "disadvantages", "compare", "contrast", "evaluation"
        ]):
            selected = "tngtech/deepseek-r1t2-chimera:free"
            print(f"🧠 Using DeepSeek model for complex reasoning task")
            return selected
        
        # Technical and coding tasks
        elif any(word in message_lower for word in [
            "code", "program", "function", "debug", "algorithm", "programming",
            "python", "javascript", "css", "html", "sql", "api", "technical",
            "coding", "script", "development", "bug", "syntax", "implement"
        ]):
            selected = "tngtech/deepseek-r1t2-chimera:free"
            print(f"💻 Using DeepSeek model for technical/coding task")
            return selected
        
        # Mathematical and scientific tasks
        elif any(word in message_lower for word in [
            "math", "equation", "calculate", "formula", "science", "physics",
            "chemistry", "statistics", "probability", "theorem", "proof"
        ]):
            selected = "tngtech/deepseek-r1t2-chimera:free"
            print(f"� Using DeepSeek model for mathematical/scientific task")
            return selected
        
        else:
            # Use Gemini for general conversation and knowledge
            selected = "google/gemma-2-9b-it:free"
            print(f"💬 Using Gemini model for general conversation")
            return selected

    async def _test_all_models(self, message: str) -> dict:
        """Test a message against all available models for comparison"""
        results = {}
        
        models_to_test = [
            "google/gemma-2-9b-it:free",
            "tngtech/deepseek-r1t2-chimera:free"
        ]
        
        for model in models_to_test:
            try:
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message}
                ]
                
                completion = self.openai_client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "http://localhost:8002",
                        "X-Title": "Clang AI Assistant - Model Test",
                    },
                    model=model,
                    messages=messages,
                    max_tokens=200,
                    temperature=0.7
                )
                
                results[model] = {
                    "response": completion.choices[0].message.content.strip(),
                    "status": "success"
                }
                
            except Exception as e:
                results[model] = {
                    "response": f"Error: {str(e)}",
                    "status": "error"
                }
        
        return results

    async def _get_huggingface_api_response(self, message: str) -> str:
        """Generate response using Hugging Face Inference API"""
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

    async def _get_simple_response(self, message: str) -> str:
        """Enhanced rule-based responses - ALWAYS WORKS"""
        message_lower = message.lower().strip()
        
        # Special commands and integrations
        if message_lower.startswith('/'):
            return await self._handle_special_commands(message_lower)
        
        # Model comparison command
        if message_lower.startswith('compare models:') or message_lower.startswith('test models:'):
            if hasattr(self, 'openai_client'):
                query = message[len('compare models:'):].strip() or message[len('test models:'):].strip()
                if query:
                    results = await self._test_all_models(query)
                    response = "🔥 Model Comparison Results:\n\n"
                    for model, result in results.items():
                        model_name = model.split('/')[-1].replace(':free', '').title()
                        status = "✅" if result['status'] == 'success' else "❌"
                        safe_response = result.get('response', '') or ''  # Handle None response
                        response += f"{status} **{model_name}**: {safe_response[:100]}{'...' if len(safe_response) > 100 else ''}\n\n"
                    return response
            return "Model comparison requires OpenRouter API. Please set up your API key."
        
        # Mathematical calculations
        if self._is_math_expression(message):
            try:
                result = self._calculate_math(message)
                return f"🧮 The answer is: {result}"
            except:
                return "I can help with basic math! Try simple expressions like '2+3', '10-4', '6*7', or '15/3'."
        
        # Prime number queries
        if self._is_prime_query(message):
            return self._handle_prime_query(message)
        
        # Complex task detection (coding, writing, etc.)
        complex_tasks = [
            "write", "essay", "paragraph", "code", "program", "function", 
            "explain how", "create", "develop", "build", "design",
            "help me with", "can you", "generate", "make", "tutorial"
        ]
        
        if any(task in message_lower for task in complex_tasks):
            result = await self._handle_complex_task(message)
            if result is None:
                # Let enhanced AI handle it - return None to pass through
                return None
            return result
        
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
        }
        
        # Enhanced conversational responses with more intelligence
        greetings = {
            "hello": "Hello! I'm Clang, your AI assistant. I can help with math, answer questions, and chat. Try asking me '3+5' or 'What is Python?'",
            "hi": "Hi there! I'm Clang, ready to help with calculations, questions, or just conversation. What's on your mind?",
            "hey": "Hey! I can do math, answer questions about technology, science, and more. What would you like to know?",
            "good morning": "Good morning! Hope you're having a great day! I'm Clang, and I can help with math problems or answer questions.",
            "good afternoon": "Good afternoon! How's your day going? I'm Clang, here to help with calculations or any questions.",
            "good evening": "Good evening! I'm Clang, your AI assistant. How can I assist you? I can solve math problems or discuss various topics.",
            "what is your name": "I'm Clang, your AI assistant! I'm here to help with complex questions, math problems, and engaging conversations.",
            "who are you": "I'm Clang, an advanced AI assistant powered by multiple LLM providers. I can handle everything from simple math to complex interdisciplinary questions!",
            "what's your name": "My name is Clang! I'm your AI assistant, ready to help with questions, calculations, and intelligent conversations."
        }
        
        # Check for knowledge base topics first
        for topic, response in knowledge_responses.items():
            if topic in message_lower:
                return response
        
        # Check for greetings
        for greeting, response in greetings.items():
            if greeting in message_lower:
                return response
        
        # Enhanced question detection and responses
        if "?" in message:
            if any(word in message_lower for word in ["what is", "what are", "define", "explain"]):
                topic = message_lower.replace("what is", "").replace("what are", "").replace("define", "").replace("explain", "").replace("?", "").strip()
                if len(topic) > 2:
                    return f"That's a great question about {topic}! While I have basic knowledge on many topics, I'd recommend checking authoritative sources for detailed information. What specific aspect of {topic} interests you most?"
        
        # Default responses based on message characteristics
        words = message.split()
        if len(words) > 5:
            return f"I can see you're asking about something related to '{' '.join(words[:3])}...'. While I have general knowledge on many topics, I'd be happy to discuss what I know or point you toward better resources. What specifically would you like to know?"
        elif len(words) == 1:
            return f"'{message}' - that's an interesting topic! Could you tell me more about what you'd like to know? I'm here to help with information and conversation."
        else:
            return f"That's an interesting point about '{message}'. I'd love to hear more about what you're thinking or what specific information you're looking for!"

    async def _handle_complex_task(self, message: str):
        """Handle complex tasks like coding, writing, etc."""
        message_lower = message.lower()
        
        # For essay writing, return None to let enhanced AI handle it
        if any(word in message_lower for word in ["write", "essay"]):
            result = self._writing_assistance(message)
            if result is None:
                return None  # Let enhanced AI handle essay writing
            return result
        elif "paragraph" in message_lower:
            return self._writing_assistance(message)
        elif any(word in message_lower for word in ["code", "program", "function", "python", "javascript"]):
            return self._coding_assistance(message)
        elif any(word in message_lower for word in ["explain how", "tutorial", "step by step"]):
            return self._tutorial_assistance(message)
        else:
            return self._general_complex_assistance(message)
    
    def _writing_assistance(self, message: str):
        """Provide writing assistance - delegate to enhanced AI for actual content creation"""
        if "essay" in message.lower():
            # For essay requests, return None to let enhanced AI handle it
            return None
        
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

    async def _handle_special_commands(self, command: str) -> str:
        """Handle special slash commands for advanced integrations"""
        
        if command == '/help' or command == '/commands':
            help_text = """**Built-in Tools:**
- 🧮 **Math Calculator**: `2+3`, `15*8-10`, `(5+3)*2`
- 🔢 **Prime Numbers**: `prime numbers from 1 to 100`, `primes between 10 and 50`
- 📝 **Text Processing**: Questions, summaries, explanations
- 💻 **Code Help**: Programming questions and examples

**AI Model Controls:**
- `compare models: [your question]` - Test question on all available providers (OpenRouter, Cohere, Groq, Mistral AI, Together AI)

**Advanced LLM Features:**
- `/analyze [question]` - Analyze question complexity
- `/knowledge add [text]` - Add knowledge to Clang's database
- `/training stats` - Show training and performance statistics
- `/feedback [rating] [comment]` - Provide feedback on last response

**Integrations:**
- `/weather [city]` - Get weather information
- `/news` - Get latest news headlines  
- `/time [timezone]` - Get current time
- `/joke` - Get a random joke
- `/quote` - Get an inspirational quote

**System:**
- `/status` - Check system status
- `/stats` - Usage statistics  
- `/help` - Show this help

Try: `prime numbers from 1 to 50` or `compare models: explain quantum physics`"""
            
            # Add advanced features note if available
            if self.advanced_llm:
                help_text += "\n\n🧠 **Clang's Advanced LLM Features Active** - Complex questions automatically get enhanced processing!"
            
            return help_text

        elif command == '/models':
            current_method = getattr(self, 'method', 'Unknown')
            current_selection = 'Auto' if not hasattr(self, '_forced_model') else getattr(self, '_forced_model', 'Auto')
            
            return f"Available AI Models:\n\nCurrently Active: {current_method}\n\nAvailable Models:\n- Gemini: Best for general conversation\n- DeepSeek: Best for complex reasoning and coding\n\nModel Selection: {current_selection}\n\nUse /switch gemini or /switch deepseek to change models"

        elif command.startswith('/switch '):
            model_name = command[8:].strip().lower()
            if model_name == 'gemini':
                self._forced_model = 'google/gemma-2-9b-it:free'
                return "✅ Switched to **Gemini** model. All responses will use Gemini until you switch back to auto."
            elif model_name == 'deepseek':
                self._forced_model = 'tngtech/deepseek-r1t2-chimera:free'
                return "✅ Switched to **DeepSeek** model. All responses will use DeepSeek until you switch back to auto."
            else:
                return "❌ Unknown model. Available: `gemini`, `deepseek`. Use `/models` to see all options."

        elif command == '/auto':
            if hasattr(self, '_forced_model'):
                delattr(self, '_forced_model')
            return "✅ Switched to **Automatic** model selection. I'll pick the best model for each task."

        elif command == '/status':
            # Multi-provider API status
            api_status = "Not configured"
            provider_info = "None"
            
            if hasattr(self, 'providers') and self.providers:
                current_provider = self.providers[self.current_provider_index]
                total_providers = len(self.providers)
                current_num = self.current_provider_index + 1
                provider_info = f"{current_provider['name'].title()} ({current_num}/{total_providers})"
                api_status = "Connected"
            
            current_method = getattr(self, 'method', 'Unknown')
            model_selection = 'Manual' if hasattr(self, '_forced_model') else 'Automatic'
            
            providers_list = "\n".join([f"- {p['name'].title()} API" for p in getattr(self, 'providers', [])])
            
            status_info = f"System Status:\n\n"
            status_info += f"AI Service: {current_method}\n"
            status_info += f"Model Selection: {model_selection}\n"
            status_info += f"Current Provider: {provider_info}\n"
            status_info += f"API Status: {api_status}\n"
            status_info += f"Math Calculator: Built-in\n"
            status_info += f"Prime Numbers: Built-in\n\n"
            status_info += f"Available Providers:\n{providers_list if providers_list else '- None configured'}\n\n"
            status_info += f"Features:\n- Mathematical calculations\n- Prime number generation\n- Multi-provider AI conversations\n- Code generation\n- Automatic provider switching\n- Intelligent model selection\n\n"
            status_info += f"Configuration:\n- Total Providers: {len(getattr(self, 'providers', []))}\n- Active Provider: {provider_info}\n- Fallback Mode: {'Enabled' if len(getattr(self, 'providers', [])) > 1 else 'Single provider only'}"
            
            return status_info

        elif command.startswith('/weather '):
            city = command[9:].strip()
            return f"🌤️ Weather integration coming soon! You asked about: **{city}**\n\nFor now, try asking the AI: 'What's the typical weather like in {city}?'"

        elif command == '/news':
            return "📰 News integration coming soon! For now, try asking the AI: 'What are some recent important world events?'"

        elif command.startswith('/time '):
            timezone = command[6:].strip()
            import datetime
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"🕐 **Current Time:** {current_time} (Local)\n\nTimezone-specific times coming soon! You asked about: **{timezone}**"

        elif command == '/joke':
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "Why did the AI go to therapy? It had too many deep learning issues! 🤖",
                "What do you call an AI assistant named Clang? A code-savvy companion! 💻",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"
            ]
            import random
            return f"😄 {random.choice(jokes)}"

        elif command == '/quote':
            quotes = [
                "\"The best way to predict the future is to create it.\" - Peter Drucker 💡",
                "\"Intelligence is the ability to adapt to change.\" - Stephen Hawking 🧠", 
                "\"The only way to do great work is to love what you do.\" - Steve Jobs ❤️",
                "\"Innovation distinguishes between a leader and a follower.\" - Steve Jobs 🚀"
            ]
            import random
            return f"✨ {random.choice(quotes)}"

        # Advanced LLM Commands
        elif command.startswith('/analyze '):
            if not self.advanced_llm:
                return "❌ Advanced LLM features not available. Please check system configuration."
            
            question = command[9:].strip()
            if not question:
                return "❌ Please provide a question to analyze. Usage: `/analyze How does quantum computing work?`"
            
            analysis = self.advanced_llm.analyze_question_complexity(question)
            return f"""🧠 **Question Analysis:**

**Question:** {question}

**Complexity Level:** {analysis['complexity'].title()} (Confidence: {analysis['confidence']:.1%})
**Word Count:** {analysis['word_count']} words
**Requires RAG:** {'Yes' if analysis['requires_rag'] else 'No'}
**Chain of Thought:** {'Yes' if analysis['requires_chain_of_thought'] else 'No'}
**Estimated Processing:** {analysis['estimated_processing_time']}

**Recommendation:** This question would be best handled with {'advanced processing and context retrieval' if analysis['complexity'] == 'complex' else 'standard AI processing' if analysis['complexity'] == 'medium' else 'quick response generation'}."""

        elif command.startswith('/knowledge add '):
            if not self.advanced_llm:
                return "❌ Advanced LLM features not available. Please check system configuration."
            
            knowledge_text = command[15:].strip()
            if not knowledge_text:
                return "❌ Please provide text to add. Usage: `/knowledge add Your important information here`"
            
            # Add knowledge asynchronously
            try:
                import asyncio
                result = await self.advanced_llm.add_knowledge_documents([knowledge_text], [{'source': 'user_input'}])
                if result:
                    return f"✅ **Knowledge Added Successfully!**\n\nAdded {len(knowledge_text)} characters to the knowledge base. This information will now be used to enhance responses to related questions."
                else:
                    return "❌ Failed to add knowledge. Please check system configuration and try again."
            except Exception as e:
                return f"❌ Error adding knowledge: {str(e)}"

        elif command == '/training stats':
            if not self.advanced_llm:
                return "❌ Advanced LLM features not available. Please check system configuration."
            
            try:
                stats = self.advanced_llm.get_training_statistics()
                suggestions = await self.advanced_llm.suggest_training_improvements()
                
                stats_text = f"""📊 **Training & Performance Statistics:**

**Interaction Data:**
- Total Interactions: {stats.get('total_interactions', 0)}
- Simple Questions: {stats.get('complexity_distribution', {}).get('simple', 0)}
- Medium Questions: {stats.get('complexity_distribution', {}).get('medium', 0)}
- Complex Questions: {stats.get('complexity_distribution', {}).get('complex', 0)}

**System Capabilities:**
- Knowledge Base Documents: {stats.get('knowledge_base_documents', 0)}
- Feedback Entries: {stats.get('feedback_entries', 0)}
- Embeddings Available: {'✅' if stats.get('embeddings_available', False) else '❌'}
- Local Models Available: {'✅' if stats.get('local_models_available', False) else '❌'}

**Improvement Suggestions:**"""

                for suggestion in suggestions[:3]:  # Show top 3 suggestions
                    stats_text += f"\n{suggestion}"
                
                if not suggestions:
                    stats_text += "\n✅ System is performing well! No immediate improvements needed."
                
                return stats_text
                
            except Exception as e:
                return f"❌ Error getting training statistics: {str(e)}"

        elif command.startswith('/feedback '):
            if not self.advanced_llm:
                return "❌ Advanced LLM features not available. Please check system configuration."
            
            feedback_parts = command[10:].strip().split(' ', 1)
            if len(feedback_parts) < 1:
                return "❌ Please provide a rating (1-5). Usage: `/feedback 4 Great response!`"
            
            try:
                rating = float(feedback_parts[0])
                if rating < 1 or rating > 5:
                    return "❌ Rating must be between 1 and 5."
                
                comment = feedback_parts[1] if len(feedback_parts) > 1 else ""
                
                # For now, we'll just acknowledge the feedback
                # In a full implementation, you'd track the last response
                await self.advanced_llm.add_feedback("Recent question", "Recent response", rating, comment)
                
                return f"""✅ **Feedback Recorded!**

**Rating:** {rating}/5 stars
**Comment:** {comment if comment else "No comment provided"}

Thank you for helping improve Clang! Your feedback helps train better responses."""
                
            except ValueError:
                return "❌ Invalid rating. Please provide a number between 1 and 5."
            except Exception as e:
                return f"❌ Error recording feedback: {str(e)}"

        else:
            return f"❌ Unknown command: `{command}`\n\nType `/help` to see available commands."

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
        
        # Check for simple math questions like "what is 2+2" or "calculate 15*8-10"
        if any(word in original_text.lower() for word in ['what is', 'calculate', 'what\'s', 'solve', 'compute']):
            # Extract math from the question - be more flexible with spaces and punctuation
            cleaned_text = original_text.replace('?', '').replace('!', '')
            # Look for numbers and math symbols - simpler approach
            math_part = re.search(r'(\d+(?:\.\d+)?[\s]*[+\-*/^][\s]*\d+(?:\.\d+)?(?:[\s]*[+\-*/^][\s]*\d+(?:\.\d+)?)*)', cleaned_text)
            if math_part:
                math_text = math_part.group().replace(" ", "")
                # Additional check for patterns with spaces
                if re.match(r'^[0-9+\-*/().^*]+$', math_text) and len(math_text) > 2:
                    # Check if it has at least one operator and number
                    has_operator = any(op in math_text for op in ['+', '-', '*', '/', '^'])
                    has_digit = any(c.isdigit() for c in math_text)
                    if has_operator and has_digit:
                        return True
        
        # Check if it matches any math pattern
        return bool(re.match(pattern, text)) and any(re.match(p, text) for p in simple_patterns)
    
    def _is_prime_query(self, text: str) -> bool:
        """Check if the text is asking about prime numbers"""
        import re
        text_lower = text.lower()
        prime_keywords = ['prime number', 'prime numbers', 'primes', 'prime from', 'prime between']
        return any(keyword in text_lower for keyword in prime_keywords)
    
    def _handle_prime_query(self, text: str) -> str:
        """Handle prime number queries"""
        import re
        text_lower = text.lower()
        
        # Extract numbers from the query
        numbers = re.findall(r'\d+', text)
        
        if len(numbers) >= 2:
            start = int(numbers[0])
            end = int(numbers[1])
        elif 'to 100' in text_lower or 'from 1' in text_lower:
            start, end = 1, 100
        elif 'to 50' in text_lower:
            start, end = 1, 50
        elif 'to 20' in text_lower:
            start, end = 1, 20
        elif len(numbers) == 1:
            end = int(numbers[0])
            start = 1 if end > 10 else 2
        else:
            start, end = 1, 100  # Default range
        
        # Generate prime numbers in the range
        primes = self._get_primes_in_range(start, end)
        
        if not primes:
            return f"No prime numbers found between {start} and {end}."
        
        primes_str = ", ".join(map(str, primes))
        count = len(primes)
        
        result = f"🔢 **Prime Numbers from {start} to {end}:**\n\n"
        result += f"**{primes_str}**\n\n"
        result += f"📊 **Total Count:** {count} prime numbers\n\n"
        result += f"💡 **Note:** A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself."
        
        return result
    
    def _get_primes_in_range(self, start: int, end: int) -> list:
        """Get all prime numbers in a given range using Sieve of Eratosthenes"""
        if end < 2:
            return []
        
        # Sieve of Eratosthenes
        sieve = [True] * (end + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(end**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, end + 1, i):
                    sieve[j] = False
        
        # Collect primes in the specified range
        primes = [i for i in range(max(2, start), end + 1) if sieve[i]]
        return primes

    def _calculate_math(self, expression: str) -> str:
        """Safely calculate mathematical expressions"""
        try:
            # Clean the expression - remove question words
            import re
            original_expr = expression
            
            # Handle questions like "what is 2+2" or "calculate 15 * 8 - 10"
            if any(word in expression.lower() for word in ['what is', 'calculate', 'what\'s', 'solve', 'compute']):
                # More flexible regex to capture math expressions with spaces and remove punctuation
                clean_expr = expression.replace('?', '').replace('!', '').replace(',', '')
                math_match = re.search(r'(\d+(?:\.\d+)?[\s]*[+\-*/^][\s]*\d+(?:\.\d+)?(?:[\s]*[+\-*/^][\s]*\d+(?:\.\d+)?)*)', clean_expr)
                if math_match:
                    expression = math_match.group()
                    # Clean up the expression
                    expression = re.sub(r'\b(what is|what\'s|calculate|solve|compute)\b', '', expression.lower()).strip()
            else:
                expression = re.sub(r'\b(what is|what\'s|calculate|solve|compute)\b', '', expression.lower()).strip()
            
            # Remove spaces and punctuation
            expression = expression.replace(" ", "").replace("?", "").replace("!", "")
            
            # Convert ^ to ** for power operations
            expression = expression.replace("^", "**")
            
            # Only allow safe characters (including ** for power)
            if not re.match(r'^[0-9+\-*/().]+$', expression):
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
            return "Error: Invalid mathematical expression"


# Simplified service for Chainlit
class ChainlitChatbotService:
    def __init__(self):
        self.chatbot = OpenSourceChatbotService()
    
    async def get_response(self, message: str, conversation_history: list = None) -> str:
        return await self.chatbot.get_response(message, conversation_history)
    
    def generate_session_id(self) -> str:
        return str(uuid.uuid4())
