"""Events and Livestream models."""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField


class EventType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#123F78')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, max_length=420)
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    featured_image = models.ImageField(upload_to='events/%Y/', blank=True, null=True)
    poster = models.ImageField(upload_to='events/posters/%Y/', blank=True, null=True)
    short_description = models.TextField(blank=True, max_length=400)
    description = HTMLField(blank=True)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=300, blank=True)
    address = models.TextField(blank=True)
    location = models.CharField(max_length=300, blank=True, help_text='City, Country')
    google_maps_url = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    organizer = models.CharField(max_length=300, blank=True)
    guest_artists = models.TextField(blank=True)
    guest_speakers = models.TextField(blank=True)
    registration_url = models.URLField(blank=True)
    ticket_info = models.TextField(blank=True)
    ticket_price = models.CharField(max_length=100, blank=True, help_text='e.g. Free, 2000 RWF')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    youtube_livestream_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    seo_title = models.CharField(max_length=300, blank=True)
    seo_description = models.TextField(blank=True, max_length=300)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'start_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'slug': self.slug})

    @property
    def start_datetime(self):
        from datetime import datetime
        if self.start_time:
            return timezone.make_aware(
                datetime.combine(self.start_date, self.start_time)
            )
        return None

    @property
    def is_past(self):
        return self.start_date < timezone.now().date()

    @property
    def countdown_target(self):
        """ISO string for countdown timer."""
        if self.start_datetime:
            return self.start_datetime.isoformat()
        from datetime import datetime
        return datetime.combine(self.start_date, datetime.min.time()).isoformat()


class LiveStream(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('ended', 'Ended'),
    ]

    title = models.CharField(max_length=300)
    youtube_url = models.URLField()
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='streams/', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='streams')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    show_on_homepage = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_datetime']
        verbose_name = 'Live Stream'
        verbose_name_plural = 'Live Streams'

    def __str__(self):
        return self.title

    @property
    def youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        import re
        if not self.youtube_url:
            return ''
        patterns = [
            r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})',
        ]
        for pattern in patterns:
            m = re.search(pattern, self.youtube_url)
            if m:
                return f'https://www.youtube.com/embed/{m.group(1)}?autoplay=1&rel=0'
        return self.youtube_url

    @property
    def youtube_video_id(self):
        import re
        m = re.search(r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})', self.youtube_url or '')
        return m.group(1) if m else ''
