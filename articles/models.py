from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse

class Playlist(models.Model):
    user = models.ForeignKey(User, default=1)
    playlist_creator = models.CharField(max_length=200)
    playlist_title = models.CharField(max_length=200)
    playlist_topic = models.CharField(max_length=200)
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.playlist_title

class Article(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=1000)
    article_url = models.CharField(max_length=1500)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.article_title
