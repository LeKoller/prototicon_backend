from django.urls import path

from .views import ContentsView, ContentImageView, FeedViews, LikesView

urlpatterns = [
    path('contents/', ContentsView.as_view()),
    path('contents/<int:content_id>/', ContentsView.as_view()),
    path('contents/image/', ContentImageView.as_view()),
    path('contents/<str:target_username>/', FeedViews.as_view()),
    path('contents/like/<int:content_id>/', LikesView.as_view())
]
