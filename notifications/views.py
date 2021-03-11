from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import NotificationSerializer
from .models import Notification
from accounts.models import User


class NotificationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nt = request.data['of_type']

        if nt != 'liked' and nt != 'followed' and nt != 'commented':
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            user = User.objects.get(username=request.data['user_username'])
            notification_data = {
                'of_type': request.data['of_type'],
                'message': request.data['message'],
                'user_username': request.data['user_username'],
                'user_id': user.id,
            }

            notification = Notification.objects.create(**notification_data)
            serializer = NotificationSerializer(notification)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, notification_id: int):
        try:
            notification = Notification.objects.get(id=notification_id)
            serializer = NotificationSerializer(notification)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, notification_id: int):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.see()

            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
