from django.urls import path
from ultra_minimal_views import home, health

urlpatterns = [
    path('', home, name='home'),
    path('health/', health, name='health'),
]
