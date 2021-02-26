from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
import ipdb

from .serializers import UserSerializer, LoginSerializer
from .models import User


class AccountsView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(**request.data)
        serializer = UserSerializer(user)
        # ipdb.set_trace()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
