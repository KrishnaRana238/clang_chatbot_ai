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
            
            # Get bot response with enhanced capabilities
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
                    # Use fixed OpenSourceChatbotService with math and medical capabilities
                    if asyncio.iscoroutinefunction(chatbot.get_response):
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            bot_response = loop.run_until_complete(chatbot.get_response(message, conversation_history))
                        finally:
                            loop.close()
                    else:
                        # Fallback to sync version if available
                        if hasattr(chatbot, 'get_response_sync'):
                            bot_response = chatbot.get_response_sync(message, conversation_history)
                        else:
                            bot_response = f"I'm Clang! I can help with math, coding, and general questions. You asked: {message}"
                
                # Ensure we always have a valid response
                if not bot_response or bot_response.strip() == "":
                    bot_response = "Hello! I'm Clang, your AI assistant. Could you please rephrase your message?"
                    
            except Exception as e:
                print(f"Error getting bot response: {e}")
                # Provide a helpful fallback response
                bot_response = "I'm Clang, and I'm experiencing some technical difficulties. Try asking me something like 'what is Python programming?' or 'solve 2+2'."
            
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
