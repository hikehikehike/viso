from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="conversation_messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    is_assistant = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
