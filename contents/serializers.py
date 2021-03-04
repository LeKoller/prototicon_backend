from rest_framework import serializers

from .models import Content
from accounts.models import User


class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    likes = serializers.IntegerField(read_only=True)
    is_private = serializers.BooleanField()
    user_id = serializers.IntegerField(read_only=True)
