from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Testimony, EvangelizationReport


def testimonies(request):
    items = Testimony.objects.filter(is_approved=True).order_by('-testimony_date')
    paginator = Paginator(items, 9)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'ministry/testimonies.html', {
        'testimonies': page,
        'page_title': 'Testimonies',
        'breadcrumb': [('Home', '/'), ('Ministry', '#'), ('Testimonies', '')],
    })


def share_testimony(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        person_name = request.POST.get('person_name', '').strip()
        email = request.POST.get('email', '').strip()
        text = request.POST.get('testimony_text', '').strip()
        if title and person_name and text:
            Testimony.objects.create(
                title=title,
                person_name=person_name,
                submitter_email=email,
                testimony_text=text,
                is_public_submission=True,
                is_approved=False,
            )
            messages.success(request, 'Thank you for sharing your testimony! It will be reviewed before publishing.')
            return redirect('ministry:testimonies')
        messages.error(request, 'Please fill in all required fields.')
    return render(request, 'ministry/share_testimony.html', {
        'page_title': 'Share Your Testimony',
    })


def evangelization(request):
    from apps.core.models import ContentPage, MinistryArea
    reports = EvangelizationReport.objects.filter(is_published=True).order_by('-event_date')
    paginator = Paginator(reports, 9)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'ministry/evangelization.html', {
        'reports': page,
        'content_page': ContentPage.objects.filter(slug='evangelization', is_published=True).first(),
        'ministry_areas': MinistryArea.objects.filter(is_active=True),
        'page_title': 'Evangelization',
        'breadcrumb': [('Home', '/'), ('Ministry', '#'), ('Evangelization', '')],
    })
