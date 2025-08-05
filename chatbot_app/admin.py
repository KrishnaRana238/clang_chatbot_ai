from django.contrib import admin
from .models import ChatSession, ChatMessage, MessageFeedback


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_id', 'title', 'user__username']
    readonly_fields = ['session_id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"


@admin.register(MessageFeedback)
class MessageFeedbackAdmin(admin.ModelAdmin):
    list_display = ['reaction', 'message_preview', 'user_ip', 'timestamp', 'session_id']
    list_filter = ['reaction', 'timestamp']
    search_fields = ['message_content', 'user_ip']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message_content[:30] + "..." if len(obj.message_content) > 30 else obj.message_content
    message_preview.short_description = "Message Preview"
