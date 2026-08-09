from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Album, Song


def album_list(request):
    albums = Album.objects.filter(status='published').prefetch_related('songs')
    return render(request, 'music/album_list.html', {
        'albums': albums,
        'page_title': 'Albums',
        'breadcrumb': [('Home', '/'), ('Music', '#'), ('Albums', '')],
    })


def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, status='published')
    songs = album.songs.filter(is_published=True).order_by('track_number', 'title')
    return render(request, 'music/album_detail.html', {
        'album': album,
        'songs': songs,
        'page_title': album.title,
    })


def song_list(request):
    songs = Song.objects.filter(is_published=True).select_related('album').order_by('-created_at')
    paginator = Paginator(songs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'music/song_list.html', {
        'songs': page,
        'page_title': 'All Songs',
        'breadcrumb': [('Home', '/'), ('Music', '#'), ('All Songs', '')],
    })


def song_detail(request, slug):
    song = get_object_or_404(Song, slug=slug, is_published=True)
    song.increment_views()
    related_songs = Song.objects.filter(
        is_published=True, album=song.album
    ).exclude(pk=song.pk)[:5] if song.album else []
    return render(request, 'music/song_detail.html', {
        'song': song,
        'related_songs': related_songs,
        'page_title': song.title,
    })
