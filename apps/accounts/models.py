"""User accounts, roles, and permissions."""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'Super Administrator'
    ADMIN = 'admin', 'Website Administrator'
    EDITOR = 'editor', 'Editor'
    AUTHOR = 'author', 'Author'
    MUSIC_MANAGER = 'music_manager', 'Music Manager'
    EVENTS_MANAGER = 'events_manager', 'Events Manager'
    GALLERY_MANAGER = 'gallery_manager', 'Gallery Manager'
    SPONSOR_MANAGER = 'sponsor_manager', 'Sponsor Manager'
    AD_MANAGER = 'ad_manager', 'Advertisement Manager'
    SPONSOR = 'sponsor', 'Sponsor'
    VIEWER = 'viewer', 'Viewer'


class UserProfile(models.Model):
    """Extended user profile with roles and choir membership info."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.VIEWER)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    is_choir_member = models.BooleanField(default=False)
    voice_part = models.CharField(max_length=50, blank=True,
                                  help_text='Soprano, Alto, Tenor, Bass, etc.')
    date_joined_choir = models.DateField(blank=True, null=True)
    # For sponsor accounts
    sponsor_application = models.OneToOneField(
        'sponsors.SponsorApplication', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='user_profile'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.get_role_display()})'

    def has_dashboard_access(self):
        return self.role not in [Role.VIEWER, Role.SPONSOR]

    def can_manage(self, area):
        """Check if user can manage a specific area."""
        full_access = [Role.SUPER_ADMIN, Role.ADMIN]
        permissions = {
            'content': full_access + [Role.EDITOR, Role.AUTHOR],
            'music': full_access + [Role.MUSIC_MANAGER],
            'events': full_access + [Role.EVENTS_MANAGER],
            'gallery': full_access + [Role.GALLERY_MANAGER],
            'sponsors': full_access + [Role.SPONSOR_MANAGER],
            'advertising': full_access + [Role.AD_MANAGER],
            'users': full_access,
            'settings': full_access,
        }
        allowed = permissions.get(area, full_access)
        return self.role in allowed
