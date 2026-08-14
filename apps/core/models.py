"""Core models: SiteSettings, Slider, MediaLibrary, Committee, Partners."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    """Global website settings — singleton model."""
    site_name = models.CharField(max_length=200, default='Jehovah Jireh Choir – ULK')
    tagline = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    logo_white = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    phone_2 = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, default='Kigali')
    country = models.CharField(max_length=100, blank=True, default='Rwanda')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    twitter = models.URLField(blank=True)
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=300, blank=True)
    sponsor_cta_text = models.CharField(max_length=200, blank=True, default='Become a Sponsor')
    sponsor_cta_url = models.CharField(max_length=200, blank=True, default='/sponsors/become-a-sponsor/')
    default_seo_description = models.TextField(blank=True)
    default_seo_image = models.ImageField(upload_to='site/seo/', blank=True, null=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_maps_embed = models.TextField(blank=True, help_text='Google Maps embed HTML')
    working_hours = models.TextField(blank=True)
    # About, Mission, Vision
    about = HTMLField(blank=True, help_text='About the choir — shown on About page')
    mission = HTMLField(blank=True, help_text='Mission statement')
    vision = HTMLField(blank=True, help_text='Vision statement')
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Singleton: only allow one instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SliderSlide(models.Model):
    """Hero slider slides managed from dashboard."""
    ALIGN_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]

    title = models.CharField(max_length=200)
    heading = models.CharField(max_length=300, blank=True)
    highlighted_text = models.CharField(max_length=200, blank=True,
                                        help_text='Text shown in gold color')
    description = models.TextField(blank=True)
    desktop_image = models.ImageField(upload_to='slider/', blank=True, null=True)
    mobile_image = models.ImageField(upload_to='slider/', blank=True, null=True)
    button_1_text = models.CharField(max_length=100, blank=True)
    button_1_url = models.CharField(max_length=500, blank=True)
    button_2_text = models.CharField(max_length=100, blank=True)
    button_2_url = models.CharField(max_length=500, blank=True)
    text_align = models.CharField(max_length=10, choices=ALIGN_CHOICES, default='left')
    overlay_opacity = models.FloatField(default=0.55, help_text='0.0 to 1.0')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    schedule_start = models.DateTimeField(blank=True, null=True)
    schedule_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Slider Slide'
        verbose_name_plural = 'Slider Slides'

    def __str__(self):
        return self.title

    @property
    def is_scheduled_active(self):
        now = timezone.now()
        if self.schedule_start and now < self.schedule_start:
            return False
        if self.schedule_end and now > self.schedule_end:
            return False
        return self.is_active


class MediaLibrary(models.Model):
    """Reusable media library for the entire platform."""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]

    title = models.CharField(max_length=300)
    file = models.FileField(upload_to='library/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image')
    alt_text = models.CharField(max_length=300, blank=True)
    caption = models.TextField(blank=True)
    file_size = models.PositiveBigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    uploaded_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='media_uploads'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Library'

    def __str__(self):
        return self.title

    def get_file_size_display(self):
        if not self.file_size:
            return '—'
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            try:
                self.file_size = self.file.size
            except Exception:
                pass
        super().save(*args, **kwargs)


class CommitteeMember(models.Model):
    """Choir committee / leadership members."""
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='committee/', blank=True, null=True)
    short_bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'full_name']
        verbose_name = 'Committee Member'
        verbose_name_plural = 'Committee Members'

    def __str__(self):
        return f'{self.full_name} — {self.position}'


class Partner(models.Model):
    """Choir ministry partners."""
    PARTNER_TYPES = [
        ('ministry', 'Ministry Partner'),
        ('media', 'Media Partner'),
        ('sponsor', 'Sponsor Partner'),
        ('educational', 'Educational Partner'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, default='ministry')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    """Reusable contact information block."""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    icon = models.CharField(max_length=50, blank=True, help_text='Heroicon name')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.label}: {self.value}'


class ContentPage(models.Model):
    """Editable long-form public page content."""
    slug = models.SlugField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    eyebrow = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True, max_length=600)
    featured_image = models.ImageField(upload_to='content/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=250, blank=True)
    body = HTMLField(blank=True)
    closing_statement = models.CharField(max_length=300, blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Content Page'

    def __str__(self):
        return self.title


class SiteStatistic(models.Model):
    """Editable facts displayed on the homepage and About pages."""
    key = models.SlugField(unique=True, max_length=80)
    value = models.CharField(max_length=30)
    label = models.CharField(max_length=120)
    detail = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'label']

    def __str__(self):
        return f'{self.value} — {self.label}'


class TimelineMilestone(models.Model):
    """A dated or present-day milestone in the choir's history."""
    year = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'year']

    def __str__(self):
        return f'{self.year} — {self.title}'


class MinistryArea(models.Model):
    """Editable ministry cards used on the homepage and ministry pages."""
    slug = models.SlugField(unique=True, max_length=100)
    title = models.CharField(max_length=160)
    summary = models.TextField(max_length=500)
    body = HTMLField(blank=True)
    link_url = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
