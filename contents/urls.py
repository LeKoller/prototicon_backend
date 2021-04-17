from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ContentImageView, LikesView, ContentViewSet)

router = DefaultRouter()

router.register(r'contents', ContentViewSet, basename='Content')

urlpatterns = [
    path('contents/image/', ContentImageView.as_view()),
    path('contents/like/<int:content_id>/', LikesView.as_view()),
    path('', include(router.urls)),
]
