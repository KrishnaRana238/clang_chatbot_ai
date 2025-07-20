import chainlit as cl
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our open-source chatbot service
try:
    import sys
    sys.path.append('.')
    from chatbot_app.chatbot_service import OpenSourceChatbotService
    
    # Initialize the chatbot service
    chatbot_service = OpenSourceChatbotService()
    print(f"✅ Chainlit using chatbot method: {getattr(chatbot_service, 'method', 'unknown')}")
    
except Exception as e:
    print(f"⚠️  Failed to import chatbot service: {e}")
    chatbot_service = None


class ChainlitSimpleBot:
    """Simple fallback bot for Chainlit when main service fails"""
    async def get_response(self, message: str) -> str:
        message_lower = message.lower().strip()
        
        responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing well, thank you! How are you?",
            "bye": "Goodbye! Have a great day!",
            "help": "I'm here to help! You can ask me questions and I'll do my best to assist you.",
            "what can you do": "I can chat with you! Try asking me questions or just say hello.",
        }
        
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return "That's interesting! I'm Clang, your AI assistant. Try saying hello, asking how I am, or asking what I can do."


# Initialize fallback bot
simple_bot = ChainlitSimpleBot()


@cl.on_chat_start
async def start():
    """Called when a new chat session starts"""
    if chatbot_service and hasattr(chatbot_service, 'method'):
        if chatbot_service.method == "local_transformers":
            welcome_msg = "🤖 Welcome to Clang - Your AI Assistant!\n\n" \
                         "✨ I'm powered by **local transformers models** - no API keys needed!\n" \
                         "🔒 Your conversations stay private on your machine.\n\n" \
                         "What would you like to talk about today?"
        elif chatbot_service.method == "huggingface_api":
            welcome_msg = "🤖 Welcome to Clang - Your AI Assistant!\n\n" \
                         "🌐 I'm powered by **Hugging Face** open-source models!\n" \
                         "💬 Ready for a conversation - what's on your mind?"
        else:
            welcome_msg = "🤖 Welcome to Clang - Your Simple AI Assistant!\n\n" \
                         "💡 I use rule-based responses - try saying hello or asking for help!"
    else:
        welcome_msg = "🤖 Welcome to Clang!\n\n" \
                     "I'm here to help you with questions and have conversations. " \
                     "What would you like to talk about today?"
    
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def main(message: cl.Message):
    """Main message handler"""
    user_message = message.content
    
    # Show typing indicator
    async with cl.Step(name="thinking", type="tool") as step:
        step.output = "Processing your message..."
        
        try:
            if chatbot_service:
                # Use the main chatbot service
                bot_response = await chatbot_service.get_response(user_message)
            else:
                # Use simple fallback
                bot_response = await simple_bot.get_response(user_message)
                
        except Exception as e:
            print(f"Error in chatbot response: {e}")
            bot_response = await simple_bot.get_response(user_message)
    
    # Send the response
    await cl.Message(content=bot_response).send()


@cl.on_stop
async def stop():
    """Called when the chat session ends"""
    print("Chat session ended")


# Optional: Add custom CSS styling
@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates"""
    pass
