"""Music models: Albums and Songs."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField


class Album(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=320)
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    description = HTMLField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    spotify_url = models.URLField(blank=True)
    apple_music_url = models.URLField(blank=True)
    boomplay_url = models.URLField(blank=True)
    youtube_playlist_url = models.URLField(blank=True)
    seo_title = models.CharField(max_length=300, blank=True)
    seo_description = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date', '-created_at']
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.release_date and not self.year:
            self.year = self.release_date.year
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('music:album-detail', kwargs={'slug': self.slug})

    @property
    def song_count(self):
        return self.songs.filter(is_published=True).count()


class Song(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=320)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='songs')
    track_number = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    lyrics = HTMLField(blank=True)
    audio_file = models.FileField(upload_to='songs/audio/', blank=True, null=True)
    youtube_url = models.URLField(blank=True)
    spotify_url = models.URLField(blank=True)
    apple_music_url = models.URLField(blank=True)
    boomplay_url = models.URLField(blank=True)
    composer = models.CharField(max_length=300, blank=True)
    lead_singer = models.CharField(max_length=300, blank=True)
    producer = models.CharField(max_length=300, blank=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, help_text='HH:MM:SS')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['album', 'track_number', 'title']
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('music:song-detail', kwargs={'slug': self.slug})

    @property
    def duration_display(self):
        if not self.duration:
            return ''
        total = int(self.duration.total_seconds())
        m, s = divmod(total, 60)
        h, m = divmod(m, 60)
        if h:
            return f'{h}:{m:02d}:{s:02d}'
        return f'{m}:{s:02d}'

    def increment_views(self):
        Song.objects.filter(pk=self.pk).update(views=models.F('views') + 1)
