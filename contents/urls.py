from django.urls import path

from .views import ContentsView

urlpatterns = [
    path('contents/', ContentsView.as_view())
]
