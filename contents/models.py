from django.db import models

from accounts.models import User


class Content(models.Model):
    title = models.CharField(max_length=63)
    text = models.CharField(max_length=511, blank=True)
    image = models.ImageField(upload_to='media/')
    likes = models.ManyToManyField(User, related_name="liked_content")
    is_private = models.BooleanField(default=False)
    author_username = models.CharField(max_length=63, default="Anonymous")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like_or_dislike(self, liker):
        liked_set = set()
        liker_set = set()
        liker_set.add(liker)

        for user in self.likes.all():
            liked_set.add(user)

        if liker_set.issubset(liked_set):
            self.dislike(liker)
        else:
            self.like(liker)

    def like(self, liker):
        self.likes.add(liker)
        self.save()

    def dislike(self, liker):
        self.likes.remove(liker)
        self.save()
