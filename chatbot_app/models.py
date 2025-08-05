from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """Model to store chat sessions"""
    session_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Chat Session: {self.session_id}"

    class Meta:
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """Model to store individual chat messages"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

    class Meta:
        ordering = ['timestamp']


class MessageFeedback(models.Model):
    """Model to store user feedback on messages for UX analytics"""
    REACTION_CHOICES = [
        ('helpful', 'Helpful'),
        ('not-helpful', 'Not Helpful'),
        ('love', 'Love'),
        ('copy', 'Copy'),
        ('share', 'Share'),
    ]

    message_content = models.TextField(max_length=200)  # Truncated for privacy
    reaction = models.CharField(max_length=20, choices=REACTION_CHOICES)
    user_ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.reaction} - {self.message_content[:30]}..."
    
    class Meta:
        ordering = ['-timestamp']
