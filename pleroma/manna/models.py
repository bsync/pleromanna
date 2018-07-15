from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from manna.storage_backends import PrivateMediaStorage

class Upload(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    theFile = models.FileField()

class PrivateUpload(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    theFile = models.FileField(storage=PrivateMediaStorage())
    user = models.ForeignKey(User, related_name='uploads')
