from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContentSerializer
from .models import Content
from accounts.models import User


class ContentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        print(request.data)
        serializer = ContentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['user']

        try:
            user = User.objects.get(username=username)
            content_data = {
                'title': request.data['title'],
                'text': request.data['text'],
                'image': request.data['image'],
                'is_private': request.data['is_private'],
                'user_id': user.id
            }

            content = Content.objects.create(**content_data)
            serializer = ContentSerializer(content)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
