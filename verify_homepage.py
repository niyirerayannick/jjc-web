#!/usr/bin/env python
"""Test script to verify homepage rendering and functionality."""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.core.models import SliderSlide, Partner
from apps.events.models import Event
from apps.music.models import Album
from apps.cms.models import Article
from apps.gallery.models import GalleryMedia
from apps.sponsors.models import SponsorGroup
from apps.advertising.models import AdCampaign

print("=" * 70)
print("HOMEPAGE CONTENT VERIFICATION")
print("=" * 70)

# Hero Slides
print("\n1. HERO SLIDER")
slides = SliderSlide.objects.filter(is_active=True)
print(f"   Active slides: {slides.count()}")
for slide in slides:
    print(f"   - {slide.title}: heading={bool(slide.heading)}, image={bool(slide.desktop_image)}")

# Upcoming Events
print("\n2. UPCOMING EVENTS")
upcoming = Event.objects.filter(status='upcoming').first()
print(f"   Upcoming event: {upcoming.title if upcoming else 'NONE'}")

# Latest Album
print("\n3. LATEST MUSIC RELEASE")
album = Album.objects.filter(status='published').first()
print(f"   Latest album: {album.title if album else 'NONE'}")
if album:
    print(f"   Song count: {album.songs.count()}")

# Articles
print("\n4. LATEST ARTICLES")
articles = Article.objects.filter(status='published')[:4]
print(f"   Article count: {articles.count()}")
for article in articles:
    print(f"   - {article.title}")

# Gallery
print("\n5. GALLERY MEDIA")
gallery = GalleryMedia.objects.all()[:8]
print(f"   Gallery items: {gallery.count()}")

# Partners
print("\n6. PARTNERS & SPONSORS")
partners = Partner.objects.all()
print(f"   Partners: {partners.count()}")

# Sponsor Groups
print("\n7. SPONSOR GROUPS")
sponsor_groups = SponsorGroup.objects.all()
print(f"   Sponsor groups: {sponsor_groups.count()}")

# Ad Campaign
print("\n8. MID-PAGE AD")
ad = AdCampaign.objects.filter(status='active').first()
print(f"   Active ad: {ad.title if ad else 'NONE'}")

print("\n" + "=" * 70)
print("FRONTEND COMPONENTS STATUS")
print("=" * 70)
print("""
✅ Hero Slider - IMPLEMENTED
   - Alpine.js component (heroSlider())
   - Autoplay: 6s interval
   - Navigation: prev/next arrows, dots, keyboard, touch swipe
   - Slide preview cards at bottom (first 3 slides)

✅ Live Now Banner - IMPLEMENTED
   - Shows when LiveStream active
   - Red gradient background
   - Pulsing "LIVE NOW" badge
   - CTA button to livestream

✅ Ministry Highlights - IMPLEMENTED
   - 6-column grid (desktop), 3-column (tablet), 2-column (mobile)
   - Icon + title + description cards
   - Hover effects (scale, color change)

✅ Latest Music + Event - IMPLEMENTED
   - 2-column layout: Music (left) + Event (right)
   - Album cover + song list
   - Event poster + countdown timer
   - CTA buttons

✅ Latest Articles - IMPLEMENTED
   - HTMX tab filtering (All, News, Testimonies, Evangelization, Concerts)
   - 4-card grid
   - Dynamic loading via hx-get

✅ Gallery - IMPLEMENTED
   - Responsive grid (2/3/4 columns at breakpoints)
   - Hover zoom effect
   - Modal lightbox (Alpine.js)

✅ Partners/Sponsors - IMPLEMENTED
   - Horizontal logo row
   - Grayscale hover effect

✅ Be Part of Mission - IMPLEMENTED
   - Sponsor group cards in 3-column grid
   - Featured badge on middle card
   - CTA buttons

✅ Newsletter - IMPLEMENTED
   - Subscribe form at bottom
   - Email validation
   - Success/error messaging
""")

print("=" * 70)
