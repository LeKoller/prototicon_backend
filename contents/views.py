from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContentSerializer, ContentImageSerializer
from .models import Content
from accounts.models import User


class ContentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['user']

        try:
            user = User.objects.get(username=username)

            try:
                content_data = {
                    'title': request.data['title'],
                    'text': request.data['text'],
                    'is_private': request.data['is_private'],
                    'user_id': user.id
                }
            except:
                content_data = {
                    'title': request.data['title'],
                    'is_private': request.data['is_private'],
                    'user_id': user.id
                }
            finally:
                content = Content.objects.create(**content_data)
                serializer = ContentSerializer(content)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ContentImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = Content.objects.get(id=request.data['content_id'])
            content.image = request.data['image']
            content.save()

            return Response({'message': f'{content.image.name} was saved.'}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
