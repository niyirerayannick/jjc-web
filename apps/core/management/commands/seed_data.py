"""Management command to seed initial data for development."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the database with initial development data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # ── Site Settings ──
        from apps.core.models import SiteSettings
        settings = SiteSettings.get_settings()
        settings.site_name = 'Jehovah Jireh Choir – ULK'
        settings.tagline = 'We Worship. We Evangelize. We Transform Lives.'
        settings.email = 'info@jjculk.rw'
        settings.phone = '+250 788 000 000'
        settings.address = 'University of Lay Catholics of Kigali'
        settings.city = 'Kigali'
        settings.country = 'Rwanda'
        settings.facebook = 'https://facebook.com/jjcoulk'
        settings.instagram = 'https://instagram.com/jjcoulk'
        settings.youtube = 'https://youtube.com/@jjcoulk'
        settings.footer_text = (
            'Jehovah Jireh Choir – ULK is a spirit-filled gospel choir from the '
            'University of Lay Catholics of Kigali, dedicated to worship, evangelization, '
            'and transforming lives through the power of music.'
        )
        settings.copyright_text = f'© {timezone.now().year} Jehovah Jireh Choir – ULK. All rights reserved.'
        settings.sponsor_cta_text = 'Become a Sponsor'
        settings.default_seo_description = (
            'Jehovah Jireh Choir – ULK is a gospel choir from Kigali, Rwanda. '
            'We worship, evangelize, and transform lives through music ministry.'
        )
        settings.save()
        self.stdout.write(self.style.SUCCESS('✓ Site settings created'))

        # ── Superuser ──
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@jjculk.rw',
                password='JJCAdmin2024!',
                first_name='JJC',
                last_name='Administrator'
            )
            from apps.accounts.models import UserProfile, Role
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = Role.SUPER_ADMIN
            profile.save()
            self.stdout.write(self.style.SUCCESS('✓ Superuser created: admin / JJCAdmin2024!'))

        # ── CMS Categories ──
        from apps.cms.models import Category
        cats = [
            ('Latest News', 'news', '#123F78'),
            ('Testimonies', 'testimonies', '#DCA928'),
            ('Evangelization', 'evangelization', '#1F5DA8'),
            ('Concerts', 'concert', '#061B38'),
            ('Ministry', 'ministry', '#123F78'),
            ('Announcements', 'announcements', '#DCA928'),
        ]
        for name, slug, color in cats:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'color': color})
        self.stdout.write(self.style.SUCCESS('✓ Categories created'))

        # ── Event Types ──
        from apps.events.models import EventType
        event_types = [
            ('Concert', 'concert', '🎵'),
            ('Evangelization Outreach', 'evangelization-outreach', '🌍'),
            ('Worship Night', 'worship-night', '🙏'),
            ('Prayer Meeting', 'prayer-meeting', '⛪'),
            ('Album Launch', 'album-launch', '💿'),
            ('Community Outreach', 'community-outreach', '🤝'),
            ('Thanksgiving Event', 'thanksgiving', '🎉'),
        ]
        for name, slug, icon in event_types:
            EventType.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
        self.stdout.write(self.style.SUCCESS('✓ Event types created'))

        # ── Sponsor Groups ──
        from apps.sponsor.models import SponsorGroup
        groups = [
            ('Individual', 'individual', 'Personal sponsor supporting our ministry'),
            ('Inkoramutima', 'inkoramutima', 'Heart-level partner committed to our mission'),
            ('Inkingi z\'Iterambere', 'inkingi-ziterambere', 'Pillar of development — our highest-tier partnership'),
        ]
        for i, (name, slug, desc) in enumerate(groups):
            SponsorGroup.objects.get_or_create(slug=slug, defaults={
                'name': name, 'description': desc, 'order': i
            })
        self.stdout.write(self.style.SUCCESS('✓ Sponsor groups created'))

        # ── Ad Positions ──
        from apps.advertising.models import AdPosition
        positions = [
            ('Homepage Hero Secondary Banner', 'homepage-hero-secondary'),
            ('Homepage Mid-page Banner', 'homepage-mid-banner'),
            ('Homepage Ministry Sidebar', 'homepage-ministry-sidebar'),
            ('News Sidebar', 'news-sidebar'),
            ('Article Inline Ad', 'article-inline'),
            ('Article Bottom Ad', 'article-bottom'),
            ('Events Page', 'events-page'),
            ('Gallery Page', 'gallery-page'),
            ('Footer Banner', 'footer-banner'),
        ]
        for name, slug in positions:
            AdPosition.objects.get_or_create(slug=slug, defaults={'name': name})
        self.stdout.write(self.style.SUCCESS('✓ Ad positions created'))

        # ── Hero Slider sample ──
        from apps.core.models import SliderSlide
        if not SliderSlide.objects.exists():
            SliderSlide.objects.create(
                title='Welcome Slide',
                heading='WE WORSHIP.\nWE EVANGELIZE.',
                highlighted_text='WE TRANSFORM LIVES.',
                description='A spirit-filled gospel choir bringing hope, healing, and the presence of God through music and ministry.',
                desktop_image='',  # Will need actual image
                button_1_text='Listen to Our Music',
                button_1_url='/music/albums/',
                button_2_text='Upcoming Events',
                button_2_url='/events/',
                text_align='left',
                overlay_opacity=0.6,
                order=0,
                is_active=True,
            )
        self.stdout.write(self.style.SUCCESS('✓ Sample slider created'))

        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete!'))
        self.stdout.write('Admin credentials: username=admin, password=JJCAdmin2024!')
