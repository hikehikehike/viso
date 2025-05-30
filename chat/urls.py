from django.urls import path
from .views import ConversationListCreate, MessageListCreate

urlpatterns = [
    path("conversations/", ConversationListCreate.as_view()),
    path("messages/", MessageListCreate.as_view()),
]
