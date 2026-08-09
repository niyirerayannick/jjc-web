from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, SliderSlide, MediaLibrary, CommitteeMember, Partner


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {'fields': ('site_name', 'tagline', 'logo', 'logo_white', 'favicon')}),
        ('Contact', {'fields': ('email', 'phone', 'phone_2', 'address', 'city', 'country')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'youtube', 'tiktok', 'whatsapp', 'twitter')}),
        ('Footer', {'fields': ('footer_text', 'copyright_text')}),
        ('Sponsor CTA', {'fields': ('sponsor_cta_text', 'sponsor_cta_url')}),
        ('SEO', {'fields': ('default_seo_description', 'default_seo_image')}),
        ('Analytics', {'fields': ('google_analytics_id',)}),
        ('Other', {'fields': ('google_maps_embed', 'working_hours', 'maintenance_mode')}),
    )


@admin.register(SliderSlide)
class SliderSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'is_featured', 'schedule_start', 'schedule_end')
    list_editable = ('order', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    ordering = ('order',)


@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'get_file_size_display', 'uploaded_by', 'created_at')
    list_filter = ('media_type',)
    search_fields = ('title', 'alt_text', 'tags')
    readonly_fields = ('file_size', 'mime_type', 'width', 'height', 'created_at')


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
