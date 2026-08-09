"""Ministry models: Testimonies, Evangelization."""
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class Testimony(models.Model):
    title = models.CharField(max_length=300)
    person_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='testimonies/photos/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='testimonies/', blank=True, null=True)
    testimony_text = HTMLField(blank=True)
    video_url = models.URLField(blank=True)
    testimony_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_public_submission = models.BooleanField(default=False)
    submitter_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-testimony_date', '-created_at']
        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'

    def __str__(self):
        return f'{self.title} — {self.person_name}'

    @property
    def has_video(self):
        return bool(self.video_url)


class EvangelizationReport(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=320)
    featured_image = models.ImageField(upload_to='evangelization/%Y/', blank=True, null=True)
    content = HTMLField(blank=True)
    location = models.CharField(max_length=300, blank=True)
    event_date = models.DateField(blank=True, null=True)
    participants_count = models.PositiveIntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    related_event = models.ForeignKey(
        'events.Event', on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date', '-created_at']
        verbose_name = 'Evangelization Report'
        verbose_name_plural = 'Evangelization Reports'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
