from django.contrib import admin
from .models import Testimony, EvangelizationReport


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('title', 'person_name', 'is_approved', 'is_featured', 'testimony_date')
    list_filter = ('is_approved', 'is_featured', 'is_public_submission')
    list_editable = ('is_approved', 'is_featured')
    search_fields = ('title', 'person_name', 'testimony_text')


@admin.register(EvangelizationReport)
class EvangelizationReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_date', 'participants_count', 'is_published')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
