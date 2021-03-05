from django.db import models

from accounts.models import User


class Content(models.Model):
    title = models.CharField(max_length=63)
    text = models.CharField(max_length=511, blank=True)
    image = models.ImageField(upload_to='media/')
    likes = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
