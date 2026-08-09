from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'status', 'subscribed_at')
    list_filter = ('status',)
    search_fields = ('email', 'name')
