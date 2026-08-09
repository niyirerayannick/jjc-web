from django.contrib import admin
from .models import Album, Song


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'status', 'is_featured', 'song_count')
    list_filter = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'track_number', 'is_published', 'is_featured', 'views')
    list_filter = ('is_published', 'is_featured', 'album')
    search_fields = ('title', 'lyrics', 'composer', 'lead_singer')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
