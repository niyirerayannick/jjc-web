from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('albums/', views.album_list, name='album-list'),
    path('albums/<slug:slug>/', views.album_detail, name='album-detail'),
    path('songs/', views.song_list, name='song-list'),
    path('songs/<slug:slug>/', views.song_detail, name='song-detail'),
]
