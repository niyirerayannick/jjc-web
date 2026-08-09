from django.contrib import admin
from .models import EventType, Event, LiveStream


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'status', 'is_featured')
    list_filter = ('status', 'event_type', 'is_featured')
    search_fields = ('title', 'venue', 'location')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    date_hierarchy = 'start_date'


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_datetime', 'show_on_homepage', 'is_featured')
    list_filter = ('status', 'show_on_homepage')
    list_editable = ('status', 'show_on_homepage')
