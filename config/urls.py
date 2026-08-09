"""URL configuration for Jehovah Jireh Choir – ULK."""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemaps import (
    StaticViewSitemap, ArticleSitemap, EventSitemap,
    AlbumSitemap, SongSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticleSitemap,
    'events': EventSitemap,
    'albums': AlbumSitemap,
    'songs': SongSitemap,
}

urlpatterns = [
    # Django admin (keep as fallback)
    path('admin/', admin.site.urls),

    # Public site
    path('', include('apps.core.urls')),
    path('', include('apps.cms.urls')),
    path('music/', include('apps.music.urls')),
    path('events/', include('apps.events.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('ministry/', include('apps.ministry.urls')),
    path('sponsors/', include('apps.sponsors.urls')),
    path('advertising/', include('apps.advertising.urls')),
    path('newsletter/', include('apps.newsletter.urls')),
    path('contact/', include('apps.contact.urls')),

    # Authentication
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Custom Dashboard
    path('dashboard/', include('apps.dashboard.urls')),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),

    # Sitemap & robots
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif getattr(settings, 'SERVE_MEDIA_FILES', False):
    # Coolify may route directly to Gunicorn. Serve persistent uploads through
    # Django in that deployment mode; Nginx can still take over /media later.
    from django.views.static import serve as serve_media
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve_media,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': False},
            name='production-media',
        ),
    ]
