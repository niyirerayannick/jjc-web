"""Core views: homepage, about, history, search, robots.txt."""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Prefetch, Q

from .models import SliderSlide, CommitteeMember, Partner, SiteSettings


def home(request):
    """Homepage view."""
    from apps.events.models import Event, LiveStream
    from apps.music.models import Album, Song
    from apps.cms.models import Article
    from apps.gallery.models import GalleryAlbum, GalleryMedia
    from apps.sponsors.models import SponsorGroup
    from apps.advertising.models import AdCampaign

    now = timezone.now()

    # Hero slider
    slides = SliderSlide.objects.filter(is_active=True).order_by('order')
    slides = [s for s in slides if s.is_scheduled_active]

    # Active livestream
    active_stream = LiveStream.objects.filter(
        status='live', show_on_homepage=True
    ).first()

    # Upcoming events
    upcoming_event = (
        Event.objects
        .filter(status='upcoming', start_date__gte=now.date())
        .select_related('event_type')
        .order_by('start_date', 'start_time')
        .first()
    )
    
    # Multiple upcoming events for the events section
    upcoming_events = (
        Event.objects
        .filter(status='upcoming', start_date__gte=now.date())
        .select_related('event_type')
        .order_by('start_date', 'start_time')[:5]
    )

    # Latest music
    published_tracks = Song.objects.filter(is_published=True).order_by('track_number', 'title')
    latest_album = (
        Album.objects
        .filter(status='published')
        .prefetch_related(Prefetch('songs', queryset=published_tracks, to_attr='homepage_tracks'))
        .order_by('-is_featured', '-release_date', '-created_at')
        .first()
    )

    # Paginated editorial ministry feed.
    from apps.cms.services import ministry_feed_context
    ministry_context = ministry_feed_context(request)

    # Gallery highlights
    gallery_media = (
        GalleryMedia.objects
        .filter(is_featured=True, media_type='image')
        .select_related('album')
        .order_by('-created_at')[:8]
    )
    if gallery_media.count() < 4:
        gallery_media = (
            GalleryMedia.objects
            .filter(media_type='image')
            .select_related('album')
            .order_by('-created_at')[:8]
        )

    # Partners
    partners = Partner.objects.filter(is_active=True).order_by('order')

    # Sponsor groups
    sponsor_groups = SponsorGroup.objects.filter(is_active=True).order_by('order')

    # Active advertisement for homepage mid-banner
    from apps.advertising.models import AdPosition
    mid_banner_ad = (
        AdCampaign.objects
        .filter(
            status='active',
            start_date__lte=now.date(),
            end_date__gte=now.date(),
            position__slug='homepage-mid-banner',
        )
        .order_by('?')
        .first()
    )

    context = {
        'slides': slides,
        'active_stream': active_stream,
        'upcoming_event': upcoming_event,
        'upcoming_events': upcoming_events,
        'latest_album': latest_album,
        'gallery_media': gallery_media,
        'partners': partners,
        'sponsor_groups': sponsor_groups,
        'mid_banner_ad': mid_banner_ad,
        'page_title': 'Home',
        **ministry_context,
    }
    return render(request, 'public/home.html', context)


def about(request):
    committee = CommitteeMember.objects.filter(is_active=True).order_by('order')
    context = {
        'committee': committee,
        'page_title': 'About Us',
        'breadcrumb': [('Home', '/'), ('Who We Are', '#'), ('About Us', '')],
    }
    return render(request, 'public/about.html', context)


def history(request):
    return render(request, 'public/history.html', {
        'page_title': 'Our History',
        'breadcrumb': [('Home', '/'), ('Who We Are', '#'), ('Our History', '')],
    })


def mission_vision(request):
    return render(request, 'public/mission.html', {
        'page_title': 'Mission & Vision',
        'breadcrumb': [('Home', '/'), ('Who We Are', '#'), ('Mission & Vision', '')],
    })


def committee(request):
    members = CommitteeMember.objects.filter(is_active=True).order_by('order')
    return render(request, 'public/committee.html', {
        'members': members,
        'page_title': 'Our Committee',
        'breadcrumb': [('Home', '/'), ('Who We Are', '#'), ('Committee', '')],
    })


def partners_page(request):
    partners = Partner.objects.filter(is_active=True).order_by('order')
    return render(request, 'public/partners.html', {
        'partners': partners,
        'page_title': 'Our Partners',
        'breadcrumb': [('Home', '/'), ('Who We Are', '#'), ('Partners', '')],
    })


def search(request):
    """Global search across all content types."""
    query = request.GET.get('q', '').strip()
    results = {}
    total = 0

    if query:
        from apps.cms.models import Article
        from apps.music.models import Album, Song
        from apps.events.models import Event
        from apps.ministry.models import Testimony, EvangelizationReport

        articles = Article.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        ).distinct()[:10]

        albums = Album.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:5]

        songs = Song.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) | Q(lyrics__icontains=query)
        )[:5]

        events = Event.objects.filter(
            status__in=['upcoming', 'ongoing']
        ).filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )[:5]

        testimonies = Testimony.objects.filter(
            is_approved=True
        ).filter(
            Q(title__icontains=query) | Q(testimony_text__icontains=query)
        )[:5]

        results = {
            'articles': articles,
            'albums': albums,
            'songs': songs,
            'events': events,
            'testimonies': testimonies,
        }
        total = sum(r.count() for r in results.values())

    return render(request, 'public/search.html', {
        'query': query,
        'results': results,
        'total': total,
        'page_title': f'Search: {query}' if query else 'Search',
    })


def robots_txt(request):
    content = (
        'User-agent: *\n'
        'Disallow: /dashboard/\n'
        'Disallow: /admin/\n'
        'Disallow: /accounts/\n'
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}\n'
    )
    return HttpResponse(content, content_type='text/plain')
