from django.db import models

from accounts.models import User
from contents.models import Content


class Notification(models.Model):
    of_type = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    user_username = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, default=None, null=True)

    def see(self):
        self.is_seen = True
        self.save()
