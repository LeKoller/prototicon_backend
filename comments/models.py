from django.db import models

from accounts.models import User
from contents.models import Content


class Comment(models.Model):
    text = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
