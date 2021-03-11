from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommentSerializer, CommentsListSerializer
from .models import Comment
from accounts.models import User
from contents.models import Content


class CommentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = request.user

            comment_data = {
                'text': request.data['text'],
                'author_id': author.id,
                'author_username': author.username,
                'content_id': request.data['content_id']
            }

            comment = Comment.objects.create(**comment_data)
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
            comments = Comment.objects.filter(content=content)

            serializer = CommentsListSerializer({'comments': comments})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, comment_id: int):
        try:
            comment = Comment.objects.get(id=comment_id)
            user = request.user

            if comment.author_username == user.username:
                comment.delete()
            else:
                return Response({'message': "it's not your comment to delete"}, status=status.HTTP_403_FORBIDDEN)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
