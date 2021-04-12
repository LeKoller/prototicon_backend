from rest_framework import serializers

from .models import Content
from accounts.serializers import UserSerializer


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

    user = UserSerializer(required=False, write_only=True)
    text = serializers.CharField(required=False)
    image = serializers.ImageField(read_only=True)
    likes = UserSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(required=False, write_only=True)
    author_username = serializers.CharField(required=False)


class ContentImageSerializer(serializers.Serializer):
    content_id = serializers.IntegerField()
    image = serializers.ImageField()


class FeedSerializer(serializers.Serializer):
    contents = ContentSerializer(many=True)


class EditContentSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    image = serializers.ImageField(read_only=True, required=False)
    is_private = serializers.BooleanField(required=False)
