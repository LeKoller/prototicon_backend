from django.db import models
from accounts.models import User


class Message(models.Model):
    author_username = models.CharField(max_length=255)
    target_username = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    in_reply_of = models.OneToOneField(
        to='self', on_delete=models.CASCADE, default=None, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_author')
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_target')
