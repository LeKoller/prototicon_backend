from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        default=0
    )

    def follow_or_unfollow(self, target_username):
        following_set = set()
        for user in self.following.iterable:
            print(user)
        target_set = set(target_username)

        if target_set.issubset(following_set):
            self.unfollow(target_username)
        else:
            self.follow(target_username)

    def follow(self, target_username):
        followed = User.objects.get(username=target_username)
        self.following.add(followed)
        self.save()

    def unfollow(self, target_username):
        followed = User.objects.get(username=target_username)
        self.following.remove(followed)
        self.save()

    def get_friends(self):
        following_set = set(self.following)
        followers_set = set(self.followers)

        return list(followers_set.intersection(followers_set))
