from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Subscriber


@require_POST
def subscribe(request):
    email = request.POST.get('email', '').strip().lower()
    name = request.POST.get('name', '').strip()
    if not email:
        if request.htmx:
            return JsonResponse({'error': 'Email is required.'}, status=400)
        messages.error(request, 'Please enter your email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    obj, created = Subscriber.objects.get_or_create(
        email=email,
        defaults={'name': name, 'status': 'active'},
    )
    if not created and obj.status == 'unsubscribed':
        obj.status = 'active'
        obj.save()
        created = True

    if request.htmx:
        msg = 'You have been subscribed!' if created else 'You are already subscribed.'
        return JsonResponse({'message': msg, 'created': created})

    if created:
        messages.success(request, 'Thank you for subscribing to our newsletter!')
    else:
        messages.info(request, 'You are already subscribed.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def unsubscribe(request, email):
    from django.utils import timezone
    try:
        sub = Subscriber.objects.get(email=email)
        sub.status = 'unsubscribed'
        sub.unsubscribed_at = timezone.now()
        sub.save()
    except Subscriber.DoesNotExist:
        pass
    return redirect('core:home')
