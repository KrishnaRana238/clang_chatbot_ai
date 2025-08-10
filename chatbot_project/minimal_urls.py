from django.urls import path, include

urlpatterns = [
    path('', include('chatbot_app.minimal_urls')),
]
