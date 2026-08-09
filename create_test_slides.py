#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.core.models import SliderSlide

# Create test slides
slides_data = [
    {
        'title': 'WORSHIP',
        'heading': 'Experience the presence of God through spirit-filled music',
        'highlighted_text': 'WE WORSHIP',
        'description': 'Encounter God through worship and experience His transforming presence.',
        'order': 1
    },
    {
        'title': 'EVANGELIZATION',
        'heading': 'Reaching the world with the gospel message',
        'highlighted_text': 'WE EVANGELIZE',
        'description': 'Reaching souls with the message of Christ and making disciples.',
        'order': 2
    },
    {
        'title': 'LIVE CONCERT',
        'heading': 'An evening of powerful music and ministry',
        'highlighted_text': 'WE TRANSFORM LIVES',
        'description': 'Experience the power of live worship as we transform lives together.',
        'order': 3
    },
    {
        'title': 'OUR STORY',
        'heading': 'A legacy of worship and ministry since 1998',
        'highlighted_text': 'FAITHFUL THROUGH GENERATIONS',
        'description': 'Discover the journey of Jehovah Jireh Choir and the mission that continues to inspire lives.',
        'order': 4
    }
]

for slide_data in slides_data:
    title = slide_data.pop('title')
    slide, created = SliderSlide.objects.get_or_create(
        title=title,
        defaults={**slide_data, 'is_active': True}
    )
    status = 'CREATED' if created else 'EXISTS'
    print(f"Slide '{slide.title}': {status}")

print(f"\nTotal active slides: {SliderSlide.objects.filter(is_active=True).count()}")
print("Test slides created successfully!")

