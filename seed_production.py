#!/usr/bin/env python
"""Import an exported local site fixture and media into production.

Run inside the deployed web container after extracting site-transfer.tar.gz:
    python seed_production.py
"""
import argparse
import os
import shutil
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='Seed production from exported local data.')
    parser.add_argument(
        '--fixture',
        default='/tmp/site-transfer/deployment/data/site-data.json',
        help='Path to the Django JSON fixture.',
    )
    parser.add_argument(
        '--media-source',
        default='/tmp/site-transfer/media',
        help='Path to the exported media directory.',
    )
    parser.add_argument(
        '--skip-media',
        action='store_true',
        help='Import database records without copying media files.',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Allow importing when production application data already exists.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    fixture = Path(args.fixture).resolve()
    media_source = Path(args.media_source).resolve()

    if not fixture.is_file():
        raise SystemExit(f'Fixture not found: {fixture}')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    import django

    django.setup()

    from django.conf import settings
    from django.core.management import call_command
    from django.db import transaction
    from apps.cms.models import Article
    from apps.core.models import SliderSlide
    from apps.events.models import Event
    from apps.music.models import Album

    existing = {
        'articles': Article.objects.count(),
        'slides': SliderSlide.objects.count(),
        'events': Event.objects.count(),
        'albums': Album.objects.count(),
    }
    if any(existing.values()) and not args.force:
        summary = ', '.join(f'{name}={count}' for name, count in existing.items())
        raise SystemExit(
            f'Production already contains application data ({summary}). '
            'Import stopped. Back up production and pass --force only if intentional.'
        )

    print('Applying migrations...')
    call_command('migrate', interactive=False, verbosity=1)

    print(f'Loading fixture: {fixture}')
    with transaction.atomic():
        call_command('loaddata', str(fixture), verbosity=1)

    if not args.skip_media:
        if not media_source.is_dir():
            raise SystemExit(
                f'Database imported, but media source was not found: {media_source}'
            )
        media_root = Path(settings.MEDIA_ROOT).resolve()
        media_root.mkdir(parents=True, exist_ok=True)
        print(f'Copying media into persistent storage: {media_root}')
        shutil.copytree(media_source, media_root, dirs_exist_ok=True)

    print('Collecting static files...')
    call_command('collectstatic', interactive=False, verbosity=0)
    print('Production seed completed successfully.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('Seed cancelled.')
