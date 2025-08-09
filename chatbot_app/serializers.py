from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'timestamp', 'metadata']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'title', 'created_at', 'updated_at', 'messages', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=5000, allow_blank=True)
    session_id = serializers.CharField(max_length=255, required=False)
