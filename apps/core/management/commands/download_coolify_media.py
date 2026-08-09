"""Download approved public choir images into persistent Coolify media storage."""
from pathlib import Path

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


MEDIA_FILES = {
    'slider/choir-hero-01-desktop.jpg': 'https://live.staticflickr.com/65535/55317900765_4785ffc819_c.jpg',
    'slider/choir-hero-01-mobile.jpg': 'https://live.staticflickr.com/65535/55317900765_4785ffc819_w.jpg',
    'slider/choir-hero-02-desktop.jpg': 'https://live.staticflickr.com/65535/54784120160_fd46fed347_z.jpg',
    'slider/choir-hero-02-mobile.jpg': 'https://live.staticflickr.com/65535/54784120160_fd46fed347_w.jpg',
    'slider/choir-hero-03-desktop.jpg': 'https://live.staticflickr.com/65535/55317715224_bcb61cbb63_z.jpg',
    'slider/choir-hero-03-mobile.jpg': 'https://live.staticflickr.com/65535/55317715224_bcb61cbb63_w.jpg',
}


class Command(BaseCommand):
    help = 'Download approved slider photos into Coolify media storage and link them to slides.'

    def add_arguments(self, parser):
        parser.add_argument('--replace', action='store_true', help='Replace existing files.')

    def handle(self, *args, **options):
        downloaded = 0
        for storage_path, url in MEDIA_FILES.items():
            if default_storage.exists(storage_path) and not options['replace']:
                self.stdout.write(f'Exists: {storage_path}')
                continue
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    raise CommandError(f'Unexpected content type for {url}: {content_type}')
                if options['replace'] and default_storage.exists(storage_path):
                    default_storage.delete(storage_path)
                saved_path = default_storage.save(
                    storage_path,
                    ContentFile(response.content, name=Path(storage_path).name),
                )
                self.stdout.write(self.style.SUCCESS(f'Downloaded: {saved_path}'))
                downloaded += 1
            except requests.RequestException as exc:
                raise CommandError(f'Could not download {url}: {exc}') from exc

        call_command('link_coolify_media')
        self.stdout.write(self.style.SUCCESS(f'Downloaded {downloaded} media file(s).'))
