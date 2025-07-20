import asyncio
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatRequestSerializer, ChatMessageSerializer
from .chatbot_service import OpenSourceChatbotService, ChainlitChatbotService
import json
import os


# Initialize chatbot service
try:
    chatbot = OpenSourceChatbotService()
    print(f"✅ Chatbot initialized successfully with method: {getattr(chatbot, 'method', 'unknown')}")
except Exception as e:
    chatbot = ChainlitChatbotService()
    print(f"⚠️  Fallback to chainlit chatbot: {e}")


def home(request):
    """Home page view"""
    return render(request, 'chatbot_app/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    """API view for chat interactions"""
    
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
            
            # Get bot response with better error handling
            try:
                bot_response = asyncio.run(chatbot.get_response(message, conversation_history))
                
                # Ensure we always have a valid response
                if not bot_response or bot_response.strip() == "":
                    bot_response = "Hello! I'm Clang, your AI assistant. Could you please rephrase your message?"
                    
            except Exception as e:
                print(f"Error getting bot response: {e}")
                # Provide a helpful fallback response
                bot_response = "I'm Clang, and I'm experiencing some technical difficulties. Try asking me something simple like 'hello' or 'how are you?'"
            
            # Save bot response
            bot_message = ChatMessage.objects.create(
                session=chat_session,
                message_type='assistant',
                content=bot_response
            )
            
            return Response({
                'session_id': session_id,
                'user_message': ChatMessageSerializer(user_message).data,
                'bot_response': ChatMessageSerializer(bot_message).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Unexpected error in ChatView: {e}")
            return Response(
                {'error': 'An unexpected error occurred. Please try again.'}, 
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
