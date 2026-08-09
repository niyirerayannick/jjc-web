from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum, GalleryMedia


def gallery(request):
    albums = GalleryAlbum.objects.prefetch_related('media').order_by('-date', '-created_at')
    active_album_slug = request.GET.get('album')
    active_album = None
    media = GalleryMedia.objects.select_related('album').order_by('album', 'order')

    if active_album_slug:
        active_album = get_object_or_404(GalleryAlbum, slug=active_album_slug)
        media = media.filter(album=active_album)

    if request.htmx:
        return render(request, 'gallery/partials/media_grid.html', {
            'media': media,
            'active_album': active_album,
        })

    return render(request, 'gallery/gallery.html', {
        'albums': albums,
        'media': media,
        'active_album': active_album,
        'page_title': 'Gallery',
        'breadcrumb': [('Home', '/'), ('Gallery', '')],
    })


def album_gallery(request, slug):
    album = get_object_or_404(GalleryAlbum, slug=slug)
    media = album.media.all().order_by('order', '-created_at')
    return render(request, 'gallery/album_gallery.html', {
        'album': album,
        'media': media,
        'page_title': album.name,
    })
