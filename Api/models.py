from django.db import models
from django.contrib.auth.models import AbstractUser


class Artist(models.Model):
    country = models.CharField(max_length=150, null=True, blank=True)
    genre = models.CharField(max_length=150, null=True, blank=True)
    user = models.OneToOneField('Api.CustomUser', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)


class CustomUser(AbstractUser):
    is_artist = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            super(CustomUser, self).save(*args, **kwargs)
            if self.is_artist:
                Artist.objects.create(user=self)
            return self


class Media(models.Model):
    title = models.CharField(max_length=50)
    type = models.IntegerField(choices=[(1, 'Music'), (2, 'Music Video'), (3, 'Book')], default=1)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True)
    genre = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lyrics = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
