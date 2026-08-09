from django.contrib import admin
from .models import SponsorGroup, SponsorApplication, SponsorContribution


@admin.register(SponsorGroup)
class SponsorGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'suggested_contribution', 'order', 'is_active')
    list_editable = ('order', 'is_active')


class SponsorContributionInline(admin.TabularInline):
    model = SponsorContribution
    extra = 0


@admin.register(SponsorApplication)
class SponsorApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'sponsor_group', 'contribution_frequency', 'status', 'created_at')
    list_filter = ('status', 'sponsor_group', 'contribution_frequency')
    search_fields = ('full_name', 'email', 'organization')
    list_editable = ('status',)
    inlines = [SponsorContributionInline]
