from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    likes = serializers.CharField(required=False)
    author_id = serializers.IntegerField(required=False)
    content_id = serializers.IntegerField()
