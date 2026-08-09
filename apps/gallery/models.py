"""Gallery models."""
from django.db import models
from django.utils.text import slugify


class GalleryAlbum(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    related_event = models.ForeignKey(
        'events.Event', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='gallery_albums'
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Gallery Album'
        verbose_name_plural = 'Gallery Albums'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def media_count(self):
        return self.media.count()


class GalleryMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='media')
    file = models.ImageField(upload_to='gallery/%Y/%m/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    caption = models.CharField(max_length=500, blank=True)
    alt_text = models.CharField(max_length=300, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Gallery Media'
        verbose_name_plural = 'Gallery Media'

    def __str__(self):
        return self.caption or f'{self.album.name} — #{self.pk}'
