from django.contrib.auth.models import User
from django import forms

from .models import Article, Playlist

class PlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ['playlist_creator', 'playlist_title', 'playlist_topic']

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['article_title', 'article_url']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
