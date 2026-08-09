from django.contrib import admin
from .models import GalleryAlbum, GalleryMedia


class GalleryMediaInline(admin.TabularInline):
    model = GalleryMedia
    extra = 3
    fields = ('file', 'media_type', 'caption', 'alt_text', 'is_featured', 'order')


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'is_featured', 'media_count')
    list_editable = ('is_featured',)
    inlines = [GalleryMediaInline]


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'album', 'media_type', 'is_featured', 'order')
    list_filter = ('media_type', 'album', 'is_featured')
    list_editable = ('is_featured', 'order')
