from django.urls import path

from .views import ContentsView, ContentImageView

urlpatterns = [
    path('contents/', ContentsView.as_view()),
    path('contents/image/', ContentImageView.as_view())
]
