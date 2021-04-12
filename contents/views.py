from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .serializers import ContentSerializer, ContentImageSerializer, FeedSerializer, EditContentSerializer
from .models import Content
from accounts.models import User
from tot.services import get_user_contents
from .pagination import CustomPageNumberPagination


class ContentViewSet(ModelViewSet):
    @method_decorator(cache_page(99999999999))
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.prefetch_related('likes')
        queryset = queryset.prefetch_related('likes__following')
        queryset = queryset.prefetch_related('likes__followers')
        queryset = queryset.prefetch_related('likes__liked_content')
        author = self.request.GET.get('author')

        if author:
            queryset = queryset.filter(author_username=author)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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

    pagination_class = CustomPageNumberPagination
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


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


class LikesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
            liker = request.user

            content.like_or_dislike(liker)

            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
