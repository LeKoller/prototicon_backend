from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate

from .serializers import UserSerializer, LoginSerializer
from .models import User


class AccountsView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**request.data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, user_username: str):
        try:
            user = User.objects.get(username=user_username)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_username: str):
        try:
            user = User.objects.get(username=user_username)
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
