from django.db import models

from accounts.models import User

# Create your models here.


class Content(models.Model):
    title = models.CharField(max_length=63)
    text = models.CharField(max_length=255)
    image = models.ImageField()
    likes = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
