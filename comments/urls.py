from django.urls import path

from .views import CommentsView

urlpatterns = [
    path('comments/', CommentsView.as_view()),
    path('comments/<int:content_id>/', CommentsView.as_view()),
    path('comments/delete/<int:comment_id>/', CommentsView.as_view())
]
