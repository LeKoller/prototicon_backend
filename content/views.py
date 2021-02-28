from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import ipdb

from .serializers import ContentSerializer
from .models import Content


class ContentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ipdb.set_trace()
        content = Content.objects.create(**request.data)
        serializer = UserSerializer(content)

        return Response(serializer.data, status=status.HTTP_201_CREATED)