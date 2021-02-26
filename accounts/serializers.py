from rest_framework import serializers

from .models import User


class FollowerSerializer(serializers.Serializer):
    username = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    following = FollowerSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
