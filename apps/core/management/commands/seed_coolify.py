"""Safely seed a new Coolify PostgreSQL database once."""
import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.cms.models import Article
from apps.core.models import SliderSlide
from apps.events.models import Event
from apps.music.models import Album


class Command(BaseCommand):
    help = 'Seed an empty Coolify production database without overwriting live content.'

    def handle(self, *args, **options):
        if not os.environ.get('DATABASE_URL'):
            raise CommandError('DATABASE_URL is required for the Coolify seed command.')

        if any((Article.objects.exists(), Album.objects.exists(), Event.objects.exists(), SliderSlide.objects.exists())):
            self.stdout.write(self.style.WARNING('Database already contains site content; Coolify seed skipped.'))
            return

        with transaction.atomic():
            call_command('seed_choir_data')
            self._configure_superuser()

        self.stdout.write(self.style.SUCCESS('Coolify production seed completed successfully.'))

    def _configure_superuser(self):
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@jehovahjirehchoir.rw')
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            self.stdout.write(self.style.WARNING(
                'DJANGO_SUPERUSER_PASSWORD was not set. Run createsuperuser before dashboard login.'
            ))
        user.save()
