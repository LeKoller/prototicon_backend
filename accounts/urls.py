from django.urls import path

from .views import AccountsView, LoginView, FollowView, UserAvatarView, UserWallpaperView

urlpatterns = [
    path('accounts/', AccountsView.as_view()),
    path('accounts/avatar/', UserAvatarView.as_view()),
    path('accounts/wallpaper/', UserWallpaperView.as_view()),
    path('accounts/<str:user_username>/', AccountsView.as_view()),
    path('login/', LoginView.as_view()),
    path('follow/<str:target_username>/', FollowView.as_view()),
    path('follow/', FollowView.as_view())
]
