from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact(request):
    from apps.core.models import SiteSettings
    settings = SiteSettings.get_settings()
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if full_name and email and subject and message:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            if ip and ',' in ip:
                ip = ip.split(',')[0].strip()
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                phone=request.POST.get('phone', ''),
                subject=subject,
                message=message,
                ip_address=ip[:45] if ip else None,
            )
            messages.success(request, 'Your message has been sent! We will get back to you soon.')
            return redirect('contact:contact')
        messages.error(request, 'Please fill in all required fields.')
    return render(request, 'contact/contact.html', {
        'settings': settings,
        'page_title': 'Contact Us',
        'breadcrumb': [('Home', '/'), ('Contact Us', '')],
    })
