from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContentSerializer, ContentImageSerializer, FeedSerializer
from .models import Content
from accounts.models import User
from tot.services import get_user_contents


class ContentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user

            try:
                content_data = {
                    'title': request.data['title'],
                    'text': request.data['text'],
                    'is_private': request.data['is_private'],
                    'user_id': user.id,
                    'author_username': user.username
                }
            except:
                content_data = {
                    'title': request.data['title'],
                    'is_private': request.data['is_private'],
                    'user_id': user.id,
                    'author_username': user.username
                }
            finally:
                content = Content.objects.create(**content_data)
                serializer = ContentSerializer(content)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)

            if request.user == content.user:
                content.delete()
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            return Response(status=status.HTTP_204_NO_CONTENT)
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


class FeedViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, target_username: str):
        try:
            contents = get_user_contents(target_username)
            # contents['author_username'] = target_username
            # print(contents['author_username'])
            serializer = FeedSerializer(contents)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
