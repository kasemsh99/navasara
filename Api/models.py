from django.db import models

class Music(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    lyrics = models.TextField()
    views = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
