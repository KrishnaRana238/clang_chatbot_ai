import json
import os

def handler(event, context):
    """
    Simple Netlify function for chatbot API
    """
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                },
                'body': ''
            }
        
        # Parse request body
        body = event.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body
            
        message = data.get('message', '')
        
        # Simple chatbot response logic
        if not message:
            response = "Hello! I'm your AI assistant. How can I help you today?"
        elif any(word in message.lower() for word in ['hello', 'hi', 'hey']):
            response = "Hello there! 😊 I'm your friendly AI chatbot. What would you like to talk about?"
        elif any(word in message.lower() for word in ['how are you', 'how do you feel']):
            response = "I'm doing great, thank you for asking! 😄 I'm here and ready to help you with anything you need."
        elif any(word in message.lower() for word in ['sad', 'depressed', 'down']):
            response = "I'm sorry to hear you're feeling down. 💙 Remember that it's okay to feel this way sometimes. Would you like to talk about what's bothering you?"
        elif any(word in message.lower() for word in ['medical', 'health', 'doctor', 'symptoms']):
            response = "I can provide general health information, but please remember I'm not a substitute for professional medical advice. What health topic would you like to know about? 🏥"
        elif any(word in message.lower() for word in ['essay', 'write', 'homework']):
            response = "I'd be happy to help you with writing! 📝 What type of essay or writing project are you working on?"
        else:
            response = f"That's an interesting question about '{message}'. I'm here to help with conversations, health information, writing assistance, and emotional support. How can I assist you further? 🤔"
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            },
            'body': json.dumps({
                'response': response,
                'status': 'success'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e),
                'response': "Sorry, I encountered an error. Please try again! 😅"
            })
        }
