from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    recipient =models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    verb = models.TextField()
    target = GenericForeignKey()
    timestamp = models.DateTimeField(auto_now=True)
