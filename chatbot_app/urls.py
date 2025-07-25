from django.urls import path
from .views import ChatView, ChatSessionListView, ChatSessionDetailView, delete_session, home
from .admin_views import (
    system_capabilities, test_capabilities, analyze_text, 
    demo_interface, math_solver
)

urlpatterns = [
    # Main chat interface
    path('', home, name='home'),
    
    # Chat API endpoints
    path('api/chat/', ChatView.as_view(), name='chat'),
    path('api/sessions/', ChatSessionListView.as_view(), name='chat_sessions'),
    path('api/sessions/<str:session_id>/', ChatSessionDetailView.as_view(), name='chat_session_detail'),
    path('api/sessions/<str:session_id>/delete/', delete_session, name='delete_session'),
    
    # Enhanced capabilities and admin endpoints
    path('api/capabilities/', system_capabilities, name='system_capabilities'),
    path('api/test/', test_capabilities, name='test_capabilities'),
    path('api/analyze/', analyze_text, name='analyze_text'),
    path('api/math/', math_solver, name='math_solver'),
    path('demo/', demo_interface, name='demo_interface'),
]
