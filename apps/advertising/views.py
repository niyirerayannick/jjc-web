from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import AdCampaign, AdImpression


def advertise(request):
    from .models import AdPackage, AdPosition
    packages = AdPackage.objects.filter(is_active=True).order_by('order')
    positions = AdPosition.objects.filter(is_active=True)
    if request.method == 'POST':
        AdCampaign.objects.create(
            business_name=request.POST.get('business_name', ''),
            contact_name=request.POST.get('contact_name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            website=request.POST.get('website', ''),
            destination_url=request.POST.get('destination_url', ''),
            position_id=request.POST.get('position') or None,
            package_id=request.POST.get('package') or None,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            ad_image=request.FILES.get('ad_image'),
        )
        from django.contrib import messages
        messages.success(request, 'Your advertising request has been submitted! We will contact you shortly.')
        return redirect('advertising:advertise')
    return render(request, 'advertising/advertise.html', {
        'packages': packages,
        'positions': positions,
        'page_title': 'Advertise With Us',
    })


@require_POST
def track_impression(request, campaign_id):
    try:
        campaign = AdCampaign.objects.get(pk=campaign_id, status='active')
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ',' in ip:
            ip = ip.split(',')[0].strip()
        AdImpression.objects.create(
            campaign=campaign,
            ip_address=ip[:45] if ip else None,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            is_click=request.POST.get('is_click') == '1',
        )
        return JsonResponse({'ok': True})
    except AdCampaign.DoesNotExist:
        return JsonResponse({'ok': False}, status=404)
