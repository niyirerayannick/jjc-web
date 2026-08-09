"""Advertising models: Packages, Positions, Campaigns, Analytics."""
from django.db import models
from django.utils import timezone


class AdPosition(models.Model):
    """Where ads can appear on the site."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    recommended_width = models.PositiveIntegerField(blank=True, null=True)
    recommended_height = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ad Position'
        verbose_name_plural = 'Ad Positions'

    def __str__(self):
        return self.name


class AdPackage(models.Model):
    """Admin-managed advertising packages."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    positions = models.ManyToManyField(AdPosition, blank=True)
    impressions_limit = models.PositiveIntegerField(blank=True, null=True,
                                                     help_text='0 = unlimited')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']
        verbose_name = 'Ad Package'
        verbose_name_plural = 'Ad Packages'

    def __str__(self):
        return self.name


class AdCampaign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    # Advertiser info
    business_name = models.CharField(max_length=300)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    # Ad content
    ad_image = models.ImageField(upload_to='ads/%Y/')
    destination_url = models.URLField()
    alt_text = models.CharField(max_length=300, blank=True)
    # Configuration
    position = models.ForeignKey(AdPosition, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(AdPackage, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ad Campaign'
        verbose_name_plural = 'Ad Campaigns'

    def __str__(self):
        return f'{self.business_name} — {self.position}'

    @property
    def is_currently_active(self):
        today = timezone.now().date()
        return (
            self.status == 'active' and
            self.start_date <= today <= self.end_date
        )


class AdImpression(models.Model):
    """Track ad impressions and clicks."""
    campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE,
                                  related_name='impressions')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_click = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Ad Impression'
        verbose_name_plural = 'Ad Impressions'

    def __str__(self):
        action = 'click' if self.is_click else 'impression'
        return f'{self.campaign} — {action} at {self.timestamp}'
