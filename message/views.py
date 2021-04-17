from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import MessageSerializer
from .models import Message
from accounts.models import User
from cache.message import MessageCache
from message_notification.message_notification_service import notify_message


class MessageViewSet(ModelViewSet):
    def queryset(self):
        author = self.request.GET.get('author')
        target = self.request.user.username

        queryset = self.queryset.filter(
            author_username=author, target_username=target)

        return queryset.order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            target_username = request.data['target_username']
            target = User.objects.get(username=target_username)
            author = request.user
            author_username = author.username
            message_cache = MessageCache(author, target)

            message = Message.objects.create(
                **request.data, target=target, author=author, author_username=author_username)
            serializer = MessageSerializer(message)
            # notify_message(serializer.data)
            message_cache.clear()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
