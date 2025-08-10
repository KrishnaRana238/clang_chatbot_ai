from django.apps import AppConfig


class MinimalChatbotAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot_app'
    
    def ready(self):
        # Skip loading complex services for minimal deployment
        pass
