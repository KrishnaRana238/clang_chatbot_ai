"""
URL configuration for chatbot project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot_app.urls')),
    path('', include('chatbot_app.urls')),
]
