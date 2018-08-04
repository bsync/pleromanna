from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now

class Lesson(models.Model):
   uploaded = models.DateTimeField(auto_now_add=True)
   recorded = models.DateTimeField(default=now)
   name = models.CharField(max_length=20)
   description = models.CharField(max_length=256)
   theFile = models.FileField()

class Series(models.Model):
   lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE)
   name = models.CharField(max_length=20)
   description = models.CharField(max_length=256)

class Catalog(models.Model):
   series = models.ForeignKey(Series, on_delete=models.CASCADE)
   name = models.CharField(max_length=20)
   description = models.CharField(max_length=256)

