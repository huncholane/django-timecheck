from django.db import models


class Post(models.Model):
    lastUpdated = models.DateTimeField()
    text = models.TextField()
