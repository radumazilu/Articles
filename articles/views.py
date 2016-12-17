from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from .models import Playlist, Article
from .forms import UserForm, ArticleForm, PlaylistForm


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'articles/login.html')
    else:
        playlists = Playlist.objects.filter(user=request.user)
        article_results = Article.objects.all()
        user_results = User.objects.all()

        # If there is a query, return results based on the search
        query = request.GET.get('q')

        if query:
            playlists = playlists.filter(
                Q(playlist_title__icontains=query) |
                Q(playlist_topic__icontains=query)
            ).distinct()
            article_results = article_results.filter(
                Q(article_title__icontains=query)
            ).distinct()
            user_results = user_results.filter(
                Q(username__icontains=query)
            ).distinct()
            return render(request, 'articles/index.html', {'playlists': playlists, 'articles': article_results, 'users': user_results})

        else:
            return render(request, 'articles/index.html', {'playlists': playlists})


def detail(request, playlist_id):
    if not request.user.is_authenticated():
        return render(request, 'articles/login.html')

    else:
        user = request.user
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        return render(request, 'articles/detail.html', {'playlist': playlist, 'user': user})


def register(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # Clean (normalised) data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        # returns User Object if credentials are correct
        user = authenticate(username=username, password=password)

        if user is not None:

            # Login the user
            if user.is_active:
                login(request, user)
                playlists = Playlist.objects.filter(user=request.user)
                return render(request, 'articles/index.html', {'playlists': playlists})

    context = {
        'form': form,
    }
    return render(request, 'articles/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                playlists = Playlist.objects.filter(user=request.user)
                return render(request, 'articles/index.html', {'playlists': playlists})
            else:
                return render(request, 'articles/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'articles/login.html', {'error_message': 'Invalid login'})
    return render(request, 'articles/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'articles/login.html', context)


def favourite(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        if article.is_favourite:
            article.is_favourite = False
        else:
            article.is_favourite = True
        article.save()
    except (KeyError, Article.DoesNotExist):
        return render(request, 'articles/articles.html', {'filter_by': 'favourite'})
    else:
        return render(request, 'articles/articles.html', {'filter_by': 'all'})


def favourite_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    playlists = Playlist.objects.filter(user=request.user)
    try:
        if playlist.is_favourite:
            playlist.is_favourite = False
        else:
            playlist.is_favourite = True
        playlist.save()
    except (KeyError, Playlist.DoesNotExist):
        return render(request, 'articles/index.html', {'playlists': playlists})
    else:
        return render(request, 'articles/index.html', {'playlists': playlists})



def articles(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'articles/login.html')
    else:
        try:
            article_ids = []
            for playlist in Playlist.objects.filter(user=request.user):
                for article in playlist.article_set.all():
                    article_ids.append(article.pk)
            users_articles = Article.objects.filter(pk__in=article_ids)
            if filter_by == 'favorites':
                users_articles = users_articles.filter(is_favorite=True)
        except Playlist.DoesNotExist:
            users_articles = []
        return render(request, 'articles/articles.html', {
            'article_list': users_articles,
            'filter_by': filter_by,
        })


def create_playlist(request):
    if not request.user.is_authenticated():
        return render(request, 'articles/login.html')
    else:
        form = PlaylistForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            # file_type = album.album_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            #if file_type not in IMAGE_FILE_TYPES:
            #    context = {
            #        'album': album,
            #        'form': form,
            #        'error_message': 'Image file must be PNG, JPG, or JPEG',
            #    }
            #    return render(request, 'music/create_album.html', context)
            playlist.save()
            return render(request, 'articles/detail.html', {'playlist': playlist})
        context = {
            "form": form,
        }
        return render(request, 'articles/create_playlist.html', context)


def delete_playlist(request, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)
    playlist.delete()
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'articles/index.html', {'playlists': playlists})



def create_article(request, playlist_id):
    form = ArticleForm(request.POST or None, request.FILES or None)
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if form.is_valid():
        playlists_articles = playlist.article_set.all()
        for a in playlists_articles:
            if a.article_title == form.cleaned_data.get("article_title"):
                context = {
                    'playlist': playlist,
                    'form': form,
                    'error_message': 'You already added that article',
                }
                return render(request, 'articles/create_article.html', context)
        article = form.save(commit=False)
        article.playlist = playlist
        #article.audio_file = request.FILES['audio_file']
        #file_type = article.audio_file.url.split('.')[-1]
        #file_type = file_type.lower()
        #if file_type not in AUDIO_FILE_TYPES:
        #    context = {
        #        'album': album,
        #        'form': form,
        #        'error_message': 'Audio file must be WAV, MP3, or OGG',
        #    }
        #    return render(request, 'music/create_article.html', context)

        article.save()
        return render(request, 'articles/detail.html', {'playlist': playlist})
    context = {
        'playlist': playlist,
        'form': form,
    }
    return render(request, 'articles/create_article.html', context)


def delete_article(request, playlist_id, article_id):
    playlist = get_object_or_404(Playlist, pk=album_id)
    article = Article.objects.get(pk=article_id)
    article.delete()
    return render(request, 'music/detail.html', {'playlist': playlist})
