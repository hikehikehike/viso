from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .openai_utils import ask_ai


class ConversationListCreate(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageListCreate(APIView):
    def get(self, request):
        messages = Message.objects.filter(sender=request.user)
        return Response(MessageSerializer(messages, many=True).data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_msg = serializer.save(sender=request.user)

        conv_msgs = Message.objects.filter(conversation=user_msg.conversation).order_by("timestamp")
        assistant_reply = ask_ai(conv_msgs)

        assistant_msg = Message.objects.create(
            is_assistant=True,
            conversation=user_msg.conversation,
            sender=request.user,
            content=assistant_reply
        )

        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "assistant_message": MessageSerializer(assistant_msg).data
        })
