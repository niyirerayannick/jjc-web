"""Sponsor models: Groups, Applications, Contributions."""
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class SponsorGroup(models.Model):
    """Sponsorship tiers/groups."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = HTMLField(blank=True)
    benefits = HTMLField(blank=True)
    suggested_contribution = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    image = models.ImageField(upload_to='sponsors/groups/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#DCA928')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Sponsor Group'
        verbose_name_plural = 'Sponsor Groups'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SponsorApplication(models.Model):
    FREQUENCY_CHOICES = [
        ('one_time', 'One-time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info', 'More Information Required'),
    ]

    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=300, blank=True)
    sponsor_group = models.ForeignKey(SponsorGroup, on_delete=models.SET_NULL, null=True, blank=True)
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    contribution_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='one_time')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='sponsor_application')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_sponsors')
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sponsor Application'
        verbose_name_plural = 'Sponsor Applications'

    def __str__(self):
        return f'{self.full_name} — {self.get_status_display()}'


class SponsorContribution(models.Model):
    sponsor = models.ForeignKey(SponsorApplication, on_delete=models.CASCADE,
                                related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    receipt_file = models.FileField(upload_to='sponsors/receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.sponsor.full_name} — {self.amount} on {self.date}'
