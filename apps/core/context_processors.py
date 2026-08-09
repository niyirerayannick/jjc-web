"""Context processors to inject site-wide data into all templates."""
from django.core.cache import cache

from .models import SiteSettings, SliderSlide


def site_settings(request):
    """Inject SiteSettings into every template."""
    settings_obj = cache.get('site_settings')
    if settings_obj is None:
        settings_obj = SiteSettings.get_settings()
        cache.set('site_settings', settings_obj, 300)
    return {'site_settings': settings_obj}


def navigation(request):
    """Inject navigation context (active livestream, etc.)."""
    from apps.events.models import LiveStream
    from django.utils import timezone

    now = timezone.now()
    active_stream = (
        LiveStream.objects
        .filter(status='live', show_on_homepage=True)
        .first()
    )
    return {
        'active_livestream': active_stream,
        'current_path': request.path,
    }
