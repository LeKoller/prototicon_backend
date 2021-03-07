from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    likes = serializers.CharField(required=False)
    author_id = serializers.IntegerField(required=False, write_only=True)
    author_username = serializers.CharField(required=False)
    content_id = serializers.IntegerField()


class CommentsListSerializer(serializers.Serializer):
    comments = CommentSerializer(many=True)
