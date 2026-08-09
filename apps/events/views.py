from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Event, EventType, LiveStream


def event_list(request):
    now = timezone.now().date()
    event_type_slug = request.GET.get('type')
    tab = request.GET.get('tab', 'upcoming')

    if tab == 'past':
        events = Event.objects.filter(status='completed').order_by('-start_date')
    else:
        events = Event.objects.filter(
            status__in=['upcoming', 'ongoing'],
            start_date__gte=now
        ).order_by('start_date')

    event_types = EventType.objects.filter(is_active=True)
    if event_type_slug:
        events = events.filter(event_type__slug=event_type_slug)

    paginator = Paginator(events, 9)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'events/event_list.html', {
        'events': page,
        'event_types': event_types,
        'active_tab': tab,
        'page_title': 'Events',
        'breadcrumb': [('Home', '/'), ('Events', '')],
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related = Event.objects.filter(
        status__in=['upcoming', 'ongoing'],
        event_type=event.event_type,
    ).exclude(pk=event.pk)[:3]
    return render(request, 'events/event_detail.html', {
        'event': event,
        'related_events': related,
        'page_title': event.title,
    })


def live_stream_page(request):
    streams = LiveStream.objects.all().order_by('-start_datetime')[:10]
    active = LiveStream.objects.filter(status='live').first()
    return render(request, 'events/live.html', {
        'streams': streams,
        'active_stream': active,
        'page_title': 'Live Stream',
        'breadcrumb': [('Home', '/'), ('Events', '/events/'), ('Live Stream', '')],
    })
