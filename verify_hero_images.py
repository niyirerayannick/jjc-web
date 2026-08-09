#!/usr/bin/env python
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from apps.core.models import SliderSlide
from django.core.files.storage import default_storage

print("\n" + "="*70)
print("HERO SLIDER IMAGES - DATABASE VERIFICATION")
print("="*70)

slides = SliderSlide.objects.all().order_by('order')
for slide in slides:
    print(f"\n--- Slide {slide.order}: {slide.title} ---")
    if slide.desktop_image:
        path = slide.desktop_image.name
        size = default_storage.size(path) if default_storage.exists(path) else "N/A"
        print(f"  Desktop: {path}")
        print(f"    Size: {size} bytes")
        print(f"    URL: {slide.desktop_image.url}")
    else:
        print(f"  Desktop: None")
    
    if slide.mobile_image:
        path = slide.mobile_image.name
        size = default_storage.size(path) if default_storage.exists(path) else "N/A"
        print(f"  Mobile:  {path}")
        print(f"    Size: {size} bytes")
        print(f"    URL: {slide.mobile_image.url}")
    else:
        print(f"  Mobile: None")
    
    print(f"  Description: {slide.description[:50]}...")
    print(f"  Active: {slide.is_active}, Featured: {slide.is_featured}")

print("\n" + "="*70)
print(f"Total Slides: {slides.count()}")
print("="*70 + "\n")
