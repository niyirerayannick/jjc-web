#!/usr/bin/env python
"""
Populate hero slider with real images from Jehovah Jireh Choir Flickr account.
Downloads high-quality images from Flickr and creates/updates SliderSlide records.
"""
import os
import sys
import django
import requests
from io import BytesIO
from urllib.parse import urlparse
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.files.base import ContentFile
from apps.core.models import SliderSlide

# Define high-quality Flickr images from Jehovah Jireh Choir
# Using direct URLs with multiple size options (_c for 800px, _z for 640px, _w for 400px)
HERO_SLIDES = [
    {
        "order": 1,
        "title": "WORSHIP",
        "heading": "WE WORSHIP.\nWE EVANGELIZE.\nWE TRANSFORM LIVES.",
        "highlighted_text": "WE TRANSFORM LIVES.",
        "description": "Encounter God through worship and experience His transforming presence in spirit-filled music.",
        "desktop_image_url": "https://live.staticflickr.com/65535/55317900765_4785ffc819_c.jpg",  # 800px wide
        "mobile_image_url": "https://live.staticflickr.com/65535/55317900765_4785ffc819_w.jpg",  # 400px wide
        "alt_text": "Jehovah Jireh Choir worship performance - full choir singing with joy",
        "button_1_text": "LISTEN TO OUR MUSIC",
        "button_1_url": "/music/albums/",
        "button_2_text": "UPCOMING EVENTS",
        "button_2_url": "/events/",
        "text_align": "left",
        "overlay_opacity": 0.55,
    },
    {
        "order": 2,
        "title": "LIVE CONCERT",
        "heading": "Experience Live Worship\nLIVE CONCERT",
        "highlighted_text": "LIVE CONCERT",
        "description": "Experience the power of live worship as we transform lives together through spirit-filled performances and ministry.",
        "desktop_image_url": "https://live.staticflickr.com/65535/54784120160_fd46fed347_z.jpg",  # 640px wide
        "mobile_image_url": "https://live.staticflickr.com/65535/54784120160_fd46fed347_w.jpg",  # 400px wide
        "alt_text": "Jehovah Jireh Choir live concert performance on stage",
        "button_1_text": "UPCOMING CONCERTS",
        "button_1_url": "/events/",
        "button_2_text": "WATCH LIVE",
        "button_2_url": "/",
        "text_align": "left",
        "overlay_opacity": 0.55,
    },
    {
        "order": 3,
        "title": "EVANGELIZATION",
        "heading": "Spreading the Gospel\nEVANGELIZATION",
        "highlighted_text": "EVANGELIZATION",
        "description": "Reaching souls with the message of Christ and making disciples through music, outreach, and community ministry.",
        "desktop_image_url": "https://live.staticflickr.com/65535/55317715224_bcb61cbb63_z.jpg",  # 640px wide
        "mobile_image_url": "https://live.staticflickr.com/65535/55317715224_bcb61cbb63_w.jpg",  # 400px wide
        "alt_text": "Jehovah Jireh Choir Pentecost celebration with community gathering",
        "button_1_text": "OUR MISSION",
        "button_1_url": "/about/",
        "button_2_text": "GET INVOLVED",
        "button_2_url": "/events/",
        "text_align": "left",
        "overlay_opacity": 0.55,
    },
    {
        "order": 4,
        "title": "OUR STORY",
        "heading": "A Legacy of Worship\nSINCE 1998",
        "highlighted_text": "SINCE 1998",
        "description": "Discover the journey of Jehovah Jireh Choir and the mission that continues to inspire lives through worship.",
        "desktop_image_url": "https://live.staticflickr.com/65535/55317900765_4785ffc819_c.jpg",
        "mobile_image_url": "https://live.staticflickr.com/65535/55317900765_4785ffc819_w.jpg",
        "alt_text": "Jehovah Jireh Choir members worshipping together",
        "button_1_text": "OUR STORY",
        "button_1_url": "/about/",
        "button_2_text": "MEET THE CHOIR",
        "button_2_url": "/about/#committee",
        "text_align": "left",
        "overlay_opacity": 0.55,
    },
]

def download_image(url, filename):
    """Download image from URL and save locally"""
    try:
        print(f"  Downloading: {filename}...", end=" ")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print(f"✓ ({len(response.content) / 1024:.1f} KB)")
        return ContentFile(response.content, name=filename)
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def populate_hero_slides():
    """Create or update hero slider slides with real Flickr images"""
    print("\n" + "="*70)
    print("POPULATING HERO SLIDER WITH FLICKR IMAGES")
    print("="*70 + "\n")
    
    # Delete existing slides (optional - comment out to keep them)
    print("Clearing existing slides...")
    SliderSlide.objects.all().delete()
    print("✓ Cleared\n")
    
    for slide_data in HERO_SLIDES:
        print(f"Processing: {slide_data['title']} (Slide #{slide_data['order']})")
        
        # Download desktop image
        desktop_filename = f"choir-hero-{slide_data['order']:02d}-desktop.jpg"
        desktop_image = download_image(slide_data['desktop_image_url'], desktop_filename)
        
        # Download mobile image
        mobile_filename = f"choir-hero-{slide_data['order']:02d}-mobile.jpg"
        mobile_image = download_image(slide_data['mobile_image_url'], mobile_filename)
        
        # Create slide record
        slide = SliderSlide.objects.create(
            order=slide_data['order'],
            title=slide_data['title'],
            heading=slide_data['heading'],
            highlighted_text=slide_data['highlighted_text'],
            description=slide_data['description'],
            button_1_text=slide_data['button_1_text'],
            button_1_url=slide_data['button_1_url'],
            button_2_text=slide_data['button_2_text'],
            button_2_url=slide_data['button_2_url'],
            text_align=slide_data['text_align'],
            overlay_opacity=slide_data['overlay_opacity'],
            is_active=True,
            is_featured=True,
        )
        
        # Attach downloaded images
        if desktop_image:
            slide.desktop_image.save(desktop_filename, desktop_image, save=False)
        if mobile_image:
            slide.mobile_image.save(mobile_filename, mobile_image, save=False)
        
        slide.save()
        print(f"  ✓ Slide created: ID={slide.id}, order={slide.order}\n")
    
    print("="*70)
    print(f"✓ Successfully created {SliderSlide.objects.count()} hero slides")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        populate_hero_slides()
        print("Hero slider populated successfully!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
