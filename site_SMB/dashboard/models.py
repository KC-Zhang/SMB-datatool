from django.db import models
from django.contrib.auth.models import User

class FileModel(models.Model):
    fileField = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None) # Delete files when user is deleted
    session_key = models.CharField(max_length=40, default=None, null=True)
