"""Django sitemaps for SEO."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from apps.cms.models import Article
from apps.events.models import Event
from apps.music.models import Album, Song


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home', 'core:about', 'core:history',
            'core:mission-vision', 'core:committee', 'core:partners',
            'music:album-list', 'events:event-list', 'gallery:gallery',
            'contact:contact', 'sponsors:become-sponsor',
        ]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Event.objects.filter(status__in=['upcoming', 'ongoing'])

    def lastmod(self, obj):
        return obj.updated_at


class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Album.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class SongSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Song.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
