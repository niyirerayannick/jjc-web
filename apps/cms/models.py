"""CMS models: Articles, Categories, Tags."""
from urllib.parse import parse_qs, urlparse

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#123F78', help_text='Hex color')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cms:category', kwargs={'slug': self.slug})


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=520)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='articles')
    featured_image = models.ImageField(upload_to='articles/%Y/%m/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=300, blank=True)
    excerpt = models.TextField(blank=True, max_length=500, help_text='Short summary shown in listings')
    content = HTMLField()
    video_url = models.URLField(blank=True, help_text='Embedded video URL (YouTube/Vimeo)')
    youtube_url = models.URLField(blank=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    # SEO
    seo_title = models.CharField(max_length=300, blank=True)
    seo_description = models.TextField(blank=True, max_length=300)
    seo_image = models.ImageField(upload_to='articles/seo/', blank=True, null=True)
    canonical_url = models.URLField(blank=True)
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['status', '-published_date']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cms:article-detail', kwargs={'slug': self.slug})

    def get_seo_title(self):
        return self.seo_title or self.title

    def get_seo_description(self):
        return self.seo_description or self.excerpt or ''

    def increment_views(self):
        Article.objects.filter(pk=self.pk).update(views=models.F('views') + 1)

    @property
    def has_video(self):
        return bool(self.video_url or self.youtube_url)

    @property
    def youtube_embed_url(self):
        """Return an embeddable URL for common YouTube link formats."""
        if not self.youtube_url:
            return ''

        parsed = urlparse(self.youtube_url)
        host = parsed.netloc.lower().removeprefix('www.')
        video_id = ''

        if host == 'youtu.be':
            video_id = parsed.path.strip('/').split('/')[0]
        elif host in {'youtube.com', 'm.youtube.com'}:
            if parsed.path == '/watch':
                video_id = parse_qs(parsed.query).get('v', [''])[0]
            elif parsed.path.startswith(('/embed/', '/shorts/')):
                video_id = parsed.path.strip('/').split('/')[1]

        return f'https://www.youtube.com/embed/{video_id}' if video_id else self.youtube_url

    @property
    def reading_time(self):
        """Estimated reading time in minutes."""
        from django.utils.html import strip_tags
        word_count = len(strip_tags(self.content).split())
        minutes = max(1, round(word_count / 200))
        return minutes
