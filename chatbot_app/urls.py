from django.urls import path
from .views import (
    home, 
    ChatView, 
    ChatSessionListView, 
    ChatSessionDetailView, 
    delete_session
)

urlpatterns = [
    path('', home, name='home'),
    path('api/chat/', ChatView.as_view(), name='chat'),
    path('api/sessions/', ChatSessionListView.as_view(), name='chat_sessions'),
    path('api/sessions/<str:session_id>/', ChatSessionDetailView.as_view(), name='chat_session_detail'),
    path('api/sessions/<str:session_id>/delete/', delete_session, name='delete_session'),
]
