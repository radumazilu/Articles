from django.conf.urls import url, include
from . import views

app_name = 'articles'

urlpatterns = [
    # /articles/
    url(r'^$', views.index, name='index'),

    # /articles/register/
    url(r'^register/$', views.register, name='register'),

    # /articles/login_user/
    url(r'^login_user/$', views.login_user, name='login_user'),

    # /articles/logout_user/
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # /articles/<playlist_id>/
    url(r'^(?P<playlist_id>[0-9]+)/$', views.detail, name='detail'),

    # /articles/<article_id>/favourite
    url(r'^(?P<article_id>[0-9]+)/favourite/$', views.favourite, name='favourite'),

    # /articles/articles/all
    url(r'^articles/(?P<filter_by>[a-zA-Z]+)/$', views.articles, name='articles'),

    # /articles/playlist/add
    url(r'^create_playlist/$', views.create_playlist, name='create_playlist'),

    # /articles/playlist/<playlist_id>/delete
    url(r'^(?P<playlist_id>[0-9]+)/delete_playlist/$', views.delete_playlist, name='delete_playlist'),

    # /articles/<playlist_id>/create_article
    url(r'^(?P<playlist_id>[0-9]+)/create_article/$', views.create_article, name='create_article'),

    # /articles/<playlist_id>/create_article
    url(r'^(?P<playlist_id>[0-9]+)/delete_article/(?P<article_id>[0-9]+)/$', views.delete_article, name='delete_article'),

    # /articles/<playlist_id>/favourite_playlist
    url(r'^(?P<playlist_id>[0-9]+)/favourite_playlist/$', views.favourite_playlist, name='favourite_playlist'),

    # /articles/playlist/<playlist_id>
    #url(r'playlist/(?P<pk>[0-9]+)/$', views.PlaylistUpdate.as_view(), name='playlist-update'),

]
