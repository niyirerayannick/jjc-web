"""Custom dashboard views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count, Q
from django.views.decorators.http import require_POST

from .decorators import dashboard_required, can_manage


# ─── Dashboard Home ────────────────────────────────────────────────────────────

@dashboard_required
def home(request):
    from apps.cms.models import Article
    from apps.music.models import Album, Song
    from apps.events.models import Event, LiveStream
    from apps.sponsors.models import SponsorApplication
    from apps.advertising.models import AdCampaign
    from apps.contact.models import ContactMessage
    from apps.newsletter.models import Subscriber
    from apps.ministry.models import Testimony

    now = timezone.now()
    today = now.date()

    stats = {
        'published_articles': Article.objects.filter(status='published').count(),
        'total_songs': Song.objects.filter(is_published=True).count(),
        'total_albums': Album.objects.filter(status='published').count(),
        'upcoming_events': Event.objects.filter(status='upcoming', start_date__gte=today).count(),
        'active_sponsors': SponsorApplication.objects.filter(status='approved').count(),
        'pending_sponsors': SponsorApplication.objects.filter(status='pending').count(),
        'active_ads': AdCampaign.objects.filter(status='active', start_date__lte=today, end_date__gte=today).count(),
        'new_messages': ContactMessage.objects.filter(status='new').count(),
        'subscribers': Subscriber.objects.filter(status='active').count(),
        'pending_testimonies': Testimony.objects.filter(is_approved=False, is_public_submission=True).count(),
    }

    recent_articles = Article.objects.select_related('category', 'author').order_by('-created_at')[:5]
    upcoming_events = Event.objects.filter(status='upcoming', start_date__gte=today).order_by('start_date')[:5]
    recent_messages = ContactMessage.objects.filter(status='new').order_by('-created_at')[:5]
    recent_sponsors = SponsorApplication.objects.filter(status='pending').order_by('-created_at')[:5]

    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'recent_articles': recent_articles,
        'upcoming_events': upcoming_events,
        'recent_messages': recent_messages,
        'recent_sponsors': recent_sponsors,
        'page_title': 'Dashboard',
    })


# ─── Articles ──────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('content')
def articles(request):
    from apps.cms.models import Article
    qs = Article.objects.select_related('category', 'author').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        qs = qs.filter(status=status_filter)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/cms/articles.html', {
        'articles': page,
        'page_title': 'Articles',
        'active_nav': 'articles',
    })


@dashboard_required
@can_manage('content')
def article_create(request):
    from apps.cms.models import Article, Category
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        from django.utils.text import slugify
        title = request.POST.get('title', '')
        slug = request.POST.get('slug') or slugify(title)
        article = Article(
            title=title,
            slug=slug,
            category_id=request.POST.get('category') or None,
            author=request.user,
            excerpt=request.POST.get('excerpt', ''),
            content=request.POST.get('content', ''),
            status=request.POST.get('status', 'draft'),
            is_featured=request.POST.get('is_featured') == 'on',
            seo_title=request.POST.get('seo_title', ''),
            seo_description=request.POST.get('seo_description', ''),
            youtube_url=request.POST.get('youtube_url', ''),
        )
        if 'featured_image' in request.FILES:
            article.featured_image = request.FILES['featured_image']
        article.save()
        messages.success(request, 'Article created successfully.')
        return redirect('dashboard:article-edit', pk=article.pk)
    return render(request, 'dashboard/cms/article_form.html', {
        'categories': categories,
        'page_title': 'New Article',
        'active_nav': 'articles',
    })


@dashboard_required
@can_manage('content')
def article_edit(request, pk):
    from apps.cms.models import Article, Category
    article = get_object_or_404(Article, pk=pk)
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        from django.utils.text import slugify
        article.title = request.POST.get('title', article.title)
        article.slug = request.POST.get('slug') or slugify(article.title)
        article.category_id = request.POST.get('category') or None
        article.excerpt = request.POST.get('excerpt', '')
        article.content = request.POST.get('content', '')
        article.status = request.POST.get('status', article.status)
        article.is_featured = request.POST.get('is_featured') == 'on'
        article.seo_title = request.POST.get('seo_title', '')
        article.seo_description = request.POST.get('seo_description', '')
        article.youtube_url = request.POST.get('youtube_url', '')
        if 'featured_image' in request.FILES:
            article.featured_image = request.FILES['featured_image']
        article.save()
        messages.success(request, 'Article updated successfully.')
        return redirect('dashboard:article-edit', pk=pk)
    return render(request, 'dashboard/cms/article_form.html', {
        'article': article,
        'categories': categories,
        'page_title': f'Edit: {article.title}',
        'active_nav': 'articles',
    })


@dashboard_required
@can_manage('content')
@require_POST
def article_delete(request, pk):
    from apps.cms.models import Article
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, 'Article deleted.')
    return redirect('dashboard:articles')


# ─── Music ─────────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('music')
def albums(request):
    from apps.music.models import Album
    items = Album.objects.annotate(song_count=Count('songs')).order_by('-release_date')
    return render(request, 'dashboard/music/albums.html', {
        'albums': items, 'page_title': 'Albums', 'active_nav': 'albums',
    })


@dashboard_required
@can_manage('music')
def album_form(request, pk=None):
    from apps.music.models import Album
    album = get_object_or_404(Album, pk=pk) if pk else None
    if request.method == 'POST':
        from django.utils.text import slugify
        data = request.POST
        if album:
            album.title = data.get('title', album.title)
            album.slug = data.get('slug') or slugify(album.title)
            album.description = data.get('description', '')
            album.release_date = data.get('release_date') or None
            album.status = data.get('status', 'draft')
            album.is_featured = data.get('is_featured') == 'on'
            album.spotify_url = data.get('spotify_url', '')
            if 'cover' in request.FILES:
                album.cover = request.FILES['cover']
            album.save()
        else:
            album = Album(
                title=data.get('title', ''),
                slug=data.get('slug') or slugify(data.get('title', '')),
                description=data.get('description', ''),
                release_date=data.get('release_date') or None,
                status=data.get('status', 'draft'),
                is_featured=data.get('is_featured') == 'on',
                spotify_url=data.get('spotify_url', ''),
            )
            if 'cover' in request.FILES:
                album.cover = request.FILES['cover']
            album.save()
        messages.success(request, 'Album saved.')
        return redirect('dashboard:albums')
    return render(request, 'dashboard/music/album_form.html', {
        'album': album,
        'page_title': f'Edit Album: {album.title}' if album else 'New Album',
        'active_nav': 'albums',
    })


@dashboard_required
@can_manage('music')
def songs(request):
    from apps.music.models import Song
    items = Song.objects.select_related('album').order_by('-created_at')
    paginator = Paginator(items, 25)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/music/songs.html', {
        'songs': page, 'page_title': 'Songs', 'active_nav': 'songs',
    })


@dashboard_required
@can_manage('music')
def song_form(request, pk=None):
    from apps.music.models import Song, Album
    song = get_object_or_404(Song, pk=pk) if pk else None
    albums = Album.objects.filter(status='published')
    if request.method == 'POST':
        from django.utils.text import slugify
        d = request.POST
        fields = {
            'title': d.get('title', ''),
            'slug': d.get('slug') or slugify(d.get('title', '')),
            'album_id': d.get('album') or None,
            'track_number': d.get('track_number') or None,
            'description': d.get('description', ''),
            'lyrics': d.get('lyrics', ''),
            'youtube_url': d.get('youtube_url', ''),
            'spotify_url': d.get('spotify_url', ''),
            'composer': d.get('composer', ''),
            'lead_singer': d.get('lead_singer', ''),
            'producer': d.get('producer', ''),
            'is_published': d.get('is_published') == 'on',
            'is_featured': d.get('is_featured') == 'on',
        }
        if song:
            for k, v in fields.items():
                setattr(song, k, v)
        else:
            song = Song(**fields)
        if 'audio_file' in request.FILES:
            song.audio_file = request.FILES['audio_file']
        song.save()
        messages.success(request, 'Song saved.')
        return redirect('dashboard:songs')
    return render(request, 'dashboard/music/song_form.html', {
        'song': song, 'albums': albums,
        'page_title': f'Edit: {song.title}' if song else 'New Song',
        'active_nav': 'songs',
    })


# ─── Events ────────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('events')
def events(request):
    from apps.events.models import Event
    items = Event.objects.select_related('event_type').order_by('-start_date')
    paginator = Paginator(items, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/events/events.html', {
        'events': page, 'page_title': 'Events', 'active_nav': 'events',
    })


@dashboard_required
@can_manage('events')
def event_form(request, pk=None):
    from apps.events.models import Event, EventType
    event = get_object_or_404(Event, pk=pk) if pk else None
    event_types = EventType.objects.filter(is_active=True)
    if request.method == 'POST':
        from django.utils.text import slugify
        d = request.POST
        fields = {
            'title': d.get('title', ''),
            'slug': d.get('slug') or slugify(d.get('title', '')),
            'event_type_id': d.get('event_type') or None,
            'short_description': d.get('short_description', ''),
            'description': d.get('description', ''),
            'start_date': d.get('start_date'),
            'start_time': d.get('start_time') or None,
            'end_date': d.get('end_date') or None,
            'venue': d.get('venue', ''),
            'address': d.get('address', ''),
            'location': d.get('location', ''),
            'ticket_price': d.get('ticket_price', ''),
            'contact_email': d.get('contact_email', ''),
            'contact_phone': d.get('contact_phone', ''),
            'youtube_livestream_url': d.get('youtube_livestream_url', ''),
            'status': d.get('status', 'draft'),
            'is_featured': d.get('is_featured') == 'on',
            'created_by': request.user,
        }
        if event:
            for k, v in fields.items():
                setattr(event, k, v)
        else:
            event = Event(**fields)
        for img_field in ['featured_image', 'poster']:
            if img_field in request.FILES:
                setattr(event, img_field, request.FILES[img_field])
        event.save()
        messages.success(request, 'Event saved.')
        return redirect('dashboard:events')
    return render(request, 'dashboard/events/event_form.html', {
        'event': event, 'event_types': event_types,
        'page_title': f'Edit: {event.title}' if event else 'New Event',
        'active_nav': 'events',
    })


@dashboard_required
@can_manage('events')
def livestreams(request):
    from apps.events.models import LiveStream
    items = LiveStream.objects.select_related('event').order_by('-start_datetime')
    return render(request, 'dashboard/events/livestreams.html', {
        'streams': items, 'page_title': 'Live Streams', 'active_nav': 'livestreams',
    })


@dashboard_required
@can_manage('events')
def livestream_form(request, pk=None):
    from apps.events.models import LiveStream, Event
    stream = get_object_or_404(LiveStream, pk=pk) if pk else None
    events_qs = Event.objects.filter(status__in=['upcoming', 'ongoing']).order_by('start_date')
    if request.method == 'POST':
        d = request.POST
        fields = {
            'title': d.get('title', ''),
            'youtube_url': d.get('youtube_url', ''),
            'description': d.get('description', ''),
            'event_id': d.get('event') or None,
            'start_datetime': d.get('start_datetime'),
            'end_datetime': d.get('end_datetime') or None,
            'status': d.get('status', 'scheduled'),
            'show_on_homepage': d.get('show_on_homepage') == 'on',
            'is_featured': d.get('is_featured') == 'on',
        }
        if stream:
            for k, v in fields.items():
                setattr(stream, k, v)
        else:
            stream = LiveStream(**fields)
        if 'thumbnail' in request.FILES:
            stream.thumbnail = request.FILES['thumbnail']
        stream.save()
        messages.success(request, 'Live stream saved.')
        return redirect('dashboard:livestreams')
    return render(request, 'dashboard/events/livestream_form.html', {
        'stream': stream, 'events': events_qs,
        'page_title': f'Edit Stream: {stream.title}' if stream else 'New Live Stream',
        'active_nav': 'livestreams',
    })


# ─── Gallery ───────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('gallery')
def gallery(request):
    from apps.gallery.models import GalleryAlbum
    albums = GalleryAlbum.objects.annotate(media_count=Count('media')).order_by('-created_at')
    return render(request, 'dashboard/gallery/albums.html', {
        'albums': albums, 'page_title': 'Gallery', 'active_nav': 'gallery',
    })


@dashboard_required
@can_manage('gallery')
def gallery_album_form(request, pk=None):
    from apps.gallery.models import GalleryAlbum
    album = get_object_or_404(GalleryAlbum, pk=pk) if pk else None
    if request.method == 'POST':
        from django.utils.text import slugify
        d = request.POST
        if album:
            album.name = d.get('name', album.name)
            album.slug = d.get('slug') or slugify(album.name)
            album.description = d.get('description', '')
            album.date = d.get('date') or None
            album.is_featured = d.get('is_featured') == 'on'
            if 'cover' in request.FILES:
                album.cover = request.FILES['cover']
            album.save()
        else:
            name = d.get('name', '')
            album = GalleryAlbum(
                name=name,
                slug=d.get('slug') or slugify(name),
                description=d.get('description', ''),
                date=d.get('date') or None,
                is_featured=d.get('is_featured') == 'on',
            )
            if 'cover' in request.FILES:
                album.cover = request.FILES['cover']
            album.save()
        messages.success(request, 'Gallery album saved.')
        return redirect('dashboard:gallery-album-media', pk=album.pk)
    return render(request, 'dashboard/gallery/album_form.html', {
        'album': album, 'page_title': f'Edit Album: {album.name}' if album else 'New Album',
        'active_nav': 'gallery',
    })


@dashboard_required
@can_manage('gallery')
def gallery_album_media(request, pk):
    from apps.gallery.models import GalleryAlbum, GalleryMedia
    album = get_object_or_404(GalleryAlbum, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        for f in files:
            GalleryMedia.objects.create(album=album, file=f, media_type='image', alt_text=album.name)
        messages.success(request, f'{len(files)} image(s) uploaded.')
        return redirect('dashboard:gallery-album-media', pk=pk)
    media = album.media.all().order_by('order', '-created_at')
    return render(request, 'dashboard/gallery/album_media.html', {
        'album': album, 'media': media,
        'page_title': f'Media: {album.name}', 'active_nav': 'gallery',
    })


# ─── Sponsors ──────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('sponsors')
def sponsor_applications(request):
    from apps.sponsors.models import SponsorApplication
    status_filter = request.GET.get('status', 'pending')
    qs = SponsorApplication.objects.select_related('sponsor_group').order_by('-created_at')
    if status_filter != 'all':
        qs = qs.filter(status=status_filter)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/sponsors/applications.html', {
        'applications': page, 'status_filter': status_filter,
        'page_title': 'Sponsor Applications', 'active_nav': 'sponsors',
    })


@dashboard_required
@can_manage('sponsors')
def sponsor_application_detail(request, pk):
    from apps.sponsors.models import SponsorApplication
    application = get_object_or_404(SponsorApplication, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected', 'more_info']:
            application.status = new_status
            application.admin_notes = request.POST.get('admin_notes', '')
            if new_status == 'approved':
                application.approved_by = request.user
                application.approved_at = timezone.now()
            application.save()
            messages.success(request, f'Application {new_status}.')
    return render(request, 'dashboard/sponsors/application_detail.html', {
        'application': application, 'page_title': f'Application: {application.full_name}',
        'active_nav': 'sponsors',
    })


@dashboard_required
@can_manage('sponsors')
def sponsor_groups(request):
    from apps.sponsors.models import SponsorGroup
    groups = SponsorGroup.objects.all().order_by('order')
    return render(request, 'dashboard/sponsors/groups.html', {
        'groups': groups, 'page_title': 'Sponsor Groups', 'active_nav': 'sponsors',
    })


# ─── Advertising ───────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('advertising')
def ad_campaigns(request):
    from apps.advertising.models import AdCampaign
    qs = AdCampaign.objects.select_related('position', 'package').order_by('-created_at')
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/advertising/campaigns.html', {
        'campaigns': page, 'page_title': 'Ad Campaigns', 'active_nav': 'advertising',
    })


@dashboard_required
@can_manage('advertising')
def ad_packages(request):
    from apps.advertising.models import AdPackage
    packages = AdPackage.objects.all().order_by('order')
    return render(request, 'dashboard/advertising/packages.html', {
        'packages': packages, 'page_title': 'Ad Packages', 'active_nav': 'advertising',
    })


# ─── Messages ──────────────────────────────────────────────────────────────────

@dashboard_required
def messages_list(request):
    from apps.contact.models import ContactMessage
    status_filter = request.GET.get('status', 'new')
    qs = ContactMessage.objects.order_by('-created_at')
    if status_filter != 'all':
        qs = qs.filter(status=status_filter)
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/messages/list.html', {
        'messages_list': page, 'status_filter': status_filter,
        'page_title': 'Contact Messages', 'active_nav': 'messages',
    })


@dashboard_required
def message_detail(request, pk):
    from apps.contact.models import ContactMessage
    msg = get_object_or_404(ContactMessage, pk=pk)
    if msg.status == 'new':
        msg.status = 'read'
        msg.save()
    if request.method == 'POST':
        msg.status = request.POST.get('status', msg.status)
        msg.admin_notes = request.POST.get('admin_notes', '')
        msg.save()
        messages.success(request, 'Message updated.')
    return render(request, 'dashboard/messages/detail.html', {
        'msg': msg, 'page_title': f'Message from {msg.full_name}',
        'active_nav': 'messages',
    })


# ─── Newsletter ────────────────────────────────────────────────────────────────

@dashboard_required
def newsletter_subscribers(request):
    from apps.newsletter.models import Subscriber
    subs = Subscriber.objects.order_by('-subscribed_at')
    paginator = Paginator(subs, 25)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/newsletter/subscribers.html', {
        'subscribers': page, 'page_title': 'Newsletter Subscribers', 'active_nav': 'newsletter',
    })


# ─── Media Library ─────────────────────────────────────────────────────────────

@dashboard_required
def media_library(request):
    from apps.core.models import MediaLibrary
    qs = MediaLibrary.objects.all().order_by('-created_at')
    media_type = request.GET.get('type')
    if media_type:
        qs = qs.filter(media_type=media_type)
    paginator = Paginator(qs, 30)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/media/library.html', {
        'media': page, 'page_title': 'Media Library', 'active_nav': 'media',
    })


@dashboard_required
@require_POST
def upload_media(request):
    from apps.core.models import MediaLibrary
    files = request.FILES.getlist('files')
    uploaded = []
    for f in files:
        obj = MediaLibrary.objects.create(
            title=f.name,
            file=f,
            media_type='image' if f.content_type.startswith('image') else 'document',
            uploaded_by=request.user,
        )
        uploaded.append({'id': obj.pk, 'title': obj.title, 'url': obj.file.url})
    return JsonResponse({'files': uploaded})


@require_POST
@dashboard_required
def upload_tinymce_image(request):
    """TinyMCE image upload endpoint."""
    from apps.core.models import MediaLibrary
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file'}, status=400)
    f = request.FILES['file']
    obj = MediaLibrary.objects.create(
        title=f.name,
        file=f,
        media_type='image',
        uploaded_by=request.user,
    )
    return JsonResponse({'location': obj.file.url})


# ─── Settings ──────────────────────────────────────────────────────────────────

@dashboard_required
def site_settings(request):
    from apps.core.models import SiteSettings
    from django.core.cache import cache
    settings_obj = SiteSettings.get_settings()
    if request.method == 'POST':
        d = request.POST
        for field in ['site_name', 'tagline', 'email', 'phone', 'phone_2', 'address',
                       'city', 'country', 'facebook', 'instagram', 'youtube', 'tiktok',
                       'whatsapp', 'twitter', 'footer_text', 'copyright_text',
                       'sponsor_cta_text', 'sponsor_cta_url', 'default_seo_description',
                       'google_analytics_id', 'google_maps_embed', 'working_hours']:
            setattr(settings_obj, field, d.get(field, ''))
        settings_obj.maintenance_mode = d.get('maintenance_mode') == 'on'
        for img_field in ['logo', 'logo_white', 'favicon', 'default_seo_image']:
            if img_field in request.FILES:
                setattr(settings_obj, img_field, request.FILES[img_field])
        settings_obj.save()
        cache.delete('site_settings')
        messages.success(request, 'Settings updated successfully.')
        return redirect('dashboard:settings')
    return render(request, 'dashboard/settings.html', {
        'settings_obj': settings_obj,
        'page_title': 'Website Settings',
        'active_nav': 'settings',
    })


# ─── Slider ────────────────────────────────────────────────────────────────────

@dashboard_required
def slider(request):
    from apps.core.models import SliderSlide
    slides = SliderSlide.objects.all().order_by('order')
    return render(request, 'dashboard/slider/list.html', {
        'slides': slides, 'page_title': 'Hero Slider', 'active_nav': 'slider',
    })


@dashboard_required
def slider_form(request, pk=None):
    from apps.core.models import SliderSlide
    slide = get_object_or_404(SliderSlide, pk=pk) if pk else None
    if request.method == 'POST':
        d = request.POST
        fields = {
            'title': d.get('title', ''),
            'heading': d.get('heading', ''),
            'highlighted_text': d.get('highlighted_text', ''),
            'description': d.get('description', ''),
            'button_1_text': d.get('button_1_text', ''),
            'button_1_url': d.get('button_1_url', ''),
            'button_2_text': d.get('button_2_text', ''),
            'button_2_url': d.get('button_2_url', ''),
            'text_align': d.get('text_align', 'left'),
            'overlay_opacity': float(d.get('overlay_opacity', 0.55)),
            'order': int(d.get('order', 0)),
            'is_active': d.get('is_active') == 'on',
            'is_featured': d.get('is_featured') == 'on',
            'schedule_start': d.get('schedule_start') or None,
            'schedule_end': d.get('schedule_end') or None,
        }
        if slide:
            for k, v in fields.items():
                setattr(slide, k, v)
        else:
            slide = SliderSlide(**fields)
        if 'desktop_image' in request.FILES:
            slide.desktop_image = request.FILES['desktop_image']
        if 'mobile_image' in request.FILES:
            slide.mobile_image = request.FILES['mobile_image']
        slide.save()
        messages.success(request, 'Slide saved.')
        return redirect('dashboard:slider')
    return render(request, 'dashboard/slider/form.html', {
        'slide': slide,
        'page_title': f'Edit Slide: {slide.title}' if slide else 'New Slide',
        'active_nav': 'slider',
    })


@dashboard_required
@require_POST
def slider_delete(request, pk):
    from apps.core.models import SliderSlide
    slide = get_object_or_404(SliderSlide, pk=pk)
    slide.delete()
    messages.success(request, 'Slide deleted.')
    return redirect('dashboard:slider')


# ─── Committee & Partners ──────────────────────────────────────────────────────

@dashboard_required
def committee(request):
    from apps.core.models import CommitteeMember
    members = CommitteeMember.objects.all().order_by('order')
    return render(request, 'dashboard/committee/list.html', {
        'members': members, 'page_title': 'Committee', 'active_nav': 'committee',
    })


@dashboard_required
def partners(request):
    from apps.core.models import Partner
    partners_qs = Partner.objects.all().order_by('order')
    return render(request, 'dashboard/partners/list.html', {
        'partners': partners_qs, 'page_title': 'Partners', 'active_nav': 'partners',
    })


# ─── Reports ───────────────────────────────────────────────────────────────────

@dashboard_required
def reports(request):
    from apps.advertising.models import AdCampaign, AdImpression
    from apps.cms.models import Article
    from django.db.models import Sum
    today = timezone.now().date()
    active_ads = AdCampaign.objects.filter(status='active', start_date__lte=today, end_date__gte=today)
    total_impressions = AdImpression.objects.filter(is_click=False).count()
    total_clicks = AdImpression.objects.filter(is_click=True).count()
    top_articles = Article.objects.filter(status='published').order_by('-views')[:10]
    return render(request, 'dashboard/reports.html', {
        'active_ads': active_ads,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'top_articles': top_articles,
        'page_title': 'Reports', 'active_nav': 'reports',
    })


# ─── Categories ────────────────────────────────────────────────────────────────

@dashboard_required
@can_manage('content')
def categories(request):
    from apps.cms.models import Category
    cats = Category.objects.annotate(article_count=Count('articles')).order_by('order')
    if request.method == 'POST':
        from django.utils.text import slugify
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name, slug=slugify(name))
            messages.success(request, 'Category created.')
        return redirect('dashboard:categories')
    return render(request, 'dashboard/cms/categories.html', {
        'categories': cats, 'page_title': 'Categories', 'active_nav': 'articles',
    })
