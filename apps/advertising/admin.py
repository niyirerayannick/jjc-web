from django.contrib import admin
from .models import AdPosition, AdPackage, AdCampaign, AdImpression


@admin.register(AdPosition)
class AdPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AdPackage)
class AdPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'position', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'position')
    list_editable = ('status',)
    search_fields = ('business_name', 'email')
