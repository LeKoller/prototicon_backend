from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        default=0
    )
    image = models.ImageField(
        upload_to='avatars/', null=True, blank=True)

    def follow_or_unfollow(self, target_username):
        target_user = User.objects.get(username=target_username)
        following_set = set()
        target_set = set()
        target_set.add(target_user)

        for user in self.following.all():
            following_set.add(user)

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
        following_set = set(self.following.all())
        followers_set = set(self.followers.all())
        friends_list = list(followers_set.intersection(followers_set))

        return {'friends': friends_list}
