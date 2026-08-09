"""Context processor to inject active ads into all templates."""
from django.utils import timezone


def active_ads(request):
    from .models import AdCampaign
    today = timezone.now().date()
    try:
        ads = AdCampaign.objects.filter(
            status='active',
            start_date__lte=today,
            end_date__gte=today,
        ).select_related('position')
        ads_by_position = {}
        for ad in ads:
            if ad.position:
                ads_by_position.setdefault(ad.position.slug, []).append(ad)
        return {'active_ads': ads_by_position}
    except Exception:
        return {'active_ads': {}}
