from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorGroup, SponsorApplication


def become_sponsor(request):
    groups = SponsorGroup.objects.filter(is_active=True).order_by('order')
    if request.method == 'POST':
        SponsorApplication.objects.create(
            full_name=request.POST.get('full_name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            organization=request.POST.get('organization', ''),
            location=request.POST.get('location', ''),
            sponsor_group_id=request.POST.get('sponsor_group') or None,
            contribution_amount=request.POST.get('contribution_amount') or None,
            contribution_frequency=request.POST.get('contribution_frequency', 'one_time'),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Thank you! Your application has been received. We will contact you soon.')
        return redirect('sponsors:become-sponsor')
    return render(request, 'sponsors/become_sponsor.html', {
        'groups': groups,
        'page_title': 'Become a Sponsor',
        'breadcrumb': [('Home', '/'), ('Sponsors', '')],
    })


def sponsor_portal(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/?next=/sponsors/portal/')
    try:
        application = request.user.sponsor_application
    except Exception:
        application = None
    return render(request, 'sponsors/portal.html', {
        'application': application,
        'page_title': 'Sponsor Portal',
    })
