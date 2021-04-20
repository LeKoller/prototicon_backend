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
from .pagination import CustomPageNumberPagination


class MessageViewSet(ModelViewSet):
    def get_queryset(self):
        friend = self.request.GET.get('username')
        user = self.request.user.username

        a_queryset = self.queryset.filter(
            author_username=friend, target_username=user)
        b_queryset = self.queryset.filter(
            author_username=user, target_username=friend)
        queryset = a_queryset.union(b_queryset)

        return queryset.order_by('-id')

    def list(self, request, *args, **kwargs):
        friend = request.GET.get('username')
        user = request.user.username

        message_cache = MessageCache(friend, user)
        messages_list = message_cache.get_messages_list()

        if messages_list:
            return Response(messages_list)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            message_cache.set_messages_list(paginated_response.data)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        message_cache.set_messages_list(serializer.data)

        return Response(serializer.data)

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
            notify_message(serializer.data)
            print('passed from notify_message call.')
            message_cache.clear()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        author = instance.author_username
        target = instance.target_username

        if self.request.user.username != author:
            return Response(status=status.HTTP_403_FORBIDDEN)

        message_cache = MessageCache(author, target)
        message_cache.clear()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    pagination_class = CustomPageNumberPagination
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
