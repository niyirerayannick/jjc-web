"""Link known uploaded seed media files to records without copying files."""
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from apps.core.models import SiteSettings, SliderSlide


class Command(BaseCommand):
    help = 'Link uploaded Coolify media files to blank site settings and hero slide image fields.'

    def handle(self, *args, **options):
        linked = 0
        missing = []

        settings = SiteSettings.get_settings()
        site_images = {
            'logo': 'site/JJC_Logos_.PNG',
            'logo_white': 'site/JJC_Logos__3zAyQLJ.PNG',
            'favicon': 'site/JJC_Logos__mzNkhV3.PNG',
        }
        settings_changed = False
        for field, path in site_images.items():
            if not getattr(settings, field) and default_storage.exists(path):
                getattr(settings, field).name = path
                settings_changed = True
                linked += 1
            elif not default_storage.exists(path):
                missing.append(path)
        if settings_changed:
            settings.save()

        slide_images = {
            1: ('slider/choir-hero-01-desktop.jpg', 'slider/choir-hero-01-mobile.jpg'),
            2: ('slider/choir-hero-02-desktop.jpg', 'slider/choir-hero-02-mobile.jpg'),
            3: ('slider/choir-hero-03-desktop.jpg', 'slider/choir-hero-03-mobile.jpg'),
            4: ('slider/choir-hero-01-desktop.jpg', 'slider/choir-hero-01-mobile.jpg'),
        }
        for order, (desktop, mobile) in slide_images.items():
            slide = SliderSlide.objects.filter(order=order).first()
            if not slide:
                continue
            changed = False
            for field, path in (('desktop_image', desktop), ('mobile_image', mobile)):
                if not getattr(slide, field) and default_storage.exists(path):
                    getattr(slide, field).name = path
                    changed = True
                    linked += 1
                elif not default_storage.exists(path):
                    missing.append(path)
            if changed:
                slide.save(update_fields=['desktop_image', 'mobile_image', 'updated_at'])

        self.stdout.write(self.style.SUCCESS(f'Linked {linked} media field(s).'))
        if missing:
            self.stdout.write(self.style.WARNING(
                'Missing media paths: ' + ', '.join(sorted(set(missing)))
            ))
