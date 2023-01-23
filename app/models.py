from django.contrib.auth.models import AbstractUser
from django.db import models


class Achievement(models.Model):
    POST_TYPE = "achievement"

    title = models.CharField(max_length=200)
    conditions = models.TextField()
    icon = models.ImageField(upload_to='media/achievement/icons', null=True)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)


class Ad(models.Model):
    POST_TYPE = "ad"

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/ads/images', null=True)
    foreign_url = models.URLField()
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    published = models.DateTimeField(null=True, blank=True)


class User(AbstractUser):
    achievements = models.ManyToManyField(Achievement)


class Note(models.Model):
    POST_TYPE = "note"

    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
