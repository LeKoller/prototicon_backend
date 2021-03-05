from rest_framework import serializers

from .models import Content


class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    text = serializers.CharField(required=False)
    likes = serializers.IntegerField(required=False)
    is_private = serializers.BooleanField()
    user_id = serializers.IntegerField(required=False)


class ContentImageSerializer(serializers.Serializer):
    content_id = serializers.IntegerField()
    image = serializers.ImageField()
