"""
Django management command to seed Jehovah Jireh Choir website with real content.
Populates all models with authentic data from the official website and Flickr account.

Usage:
    python manage.py seed_choir_data [--clear]

Options:
    --clear: Delete all existing content before seeding (use with caution in production)
"""

import os
import sys
import django
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from decimal import Decimal

# Import all models
from apps.core.models import (
    SiteSettings, SliderSlide, Partner, ContentPage, SiteStatistic,
    TimelineMilestone, MinistryArea,
)
from apps.music.models import Album, Song
from apps.cms.models import Category, Article
from apps.events.models import EventType, Event
from apps.sponsors.models import SponsorGroup
from apps.gallery.models import GalleryAlbum, GalleryMedia
from apps.ministry.models import EvangelizationReport


class Command(BaseCommand):
    help = 'Seed Jehovah Jireh Choir website with real content from official sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing content before seeding (WARNING: irreversible)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('JEHOVAH JIREH CHOIR WEBSITE SEEDING'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        if options['clear']:
            self.clear_all_data()

        try:
            # Get or create admin user for content creation
            admin_user = self.get_admin_user()
            
            # Seed in logical order
            self.seed_site_settings()
            self.seed_categories()
            self.seed_albums()
            self.seed_songs()
            self.seed_articles(admin_user)
            self.seed_event_types()
            self.seed_events()
            self.seed_evangelization_reports()
            self.seed_gallery()
            self.seed_sponsor_groups()
            self.seed_hero_slides()
            self.seed_partners()
            self.seed_authoritative_content()

            self.stdout.write(self.style.SUCCESS('\n' + '='*70))
            self.stdout.write(self.style.SUCCESS('Seeding completed successfully!'))
            self.stdout.write(self.style.SUCCESS('='*70 + '\n'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nError during seeding: {str(e)}'))
            raise CommandError(str(e))

    def clear_all_data(self):
        """Clear all seedable data"""
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        SliderSlide.objects.all().delete()
        Song.objects.all().delete()
        Album.objects.all().delete()
        Article.objects.all().delete()
        Category.objects.all().delete()
        Event.objects.all().delete()
        EventType.objects.all().delete()
        EvangelizationReport.objects.all().delete()
        GalleryMedia.objects.all().delete()
        GalleryAlbum.objects.all().delete()
        SponsorGroup.objects.all().delete()
        Partner.objects.all().delete()
        ContentPage.objects.all().delete()
        SiteStatistic.objects.all().delete()
        TimelineMilestone.objects.all().delete()
        MinistryArea.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('Data cleared'))

    def get_admin_user(self):
        """Get or create admin user"""
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jehovahjirehchoir.rw',
                'first_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        return user

    def seed_site_settings(self):
        """Seed global website settings"""
        self.stdout.write('Seeding Site Settings...')
        
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        
        settings.site_name = 'Jehovah Jireh Choir – ULK'
        settings.tagline = 'Where Gospel Music Transforms Hearts'
        settings.email = 'info@jehovahjirehchoir.rw'
        settings.phone = '+250 788 000 000'
        settings.city = 'Kigali'
        settings.country = 'Rwanda'
        settings.facebook = 'https://www.facebook.com/JehovahJirehChoir'
        settings.youtube = 'https://www.youtube.com/channel/JehovahJirehChoir'
        
        settings.footer_text = (
            'Jehovah Jireh Choir is a faith-based music ministry dedicated to spreading '
            'the gospel message through spirit-filled worship, evangelization, and community '
            'outreach since 1998.'
        )
        settings.copyright_text = '© 2024 Jehovah Jireh Choir. All rights reserved.'
        settings.sponsor_cta_text = 'Become a Sponsor'
        settings.sponsor_cta_url = '/sponsors/become-a-sponsor/'
        settings.default_seo_description = (
            'Jehovah Jireh Choir – Gospel music ministry dedicated to worship, evangelization, '
            'and spiritual transformation through spirit-filled music and community ministry.'
        )
        
        # Mission Statement
        settings.mission = (
            '<p>Jehovah Jireh Choir seeks to use Gospel music to lead people toward '
            '<strong>transformation, repentance, and becoming born-again believers</strong>.</p>'
            '<p>Through spirit-filled worship, evangelization, and community ministry, '
            'we proclaim the life-changing message of Jesus Christ and encourage believers '
            'in their spiritual journey.</p>'
        )
        
        # Vision Statement
        settings.vision = (
            '<p>To be <strong>faithful servants of the Lord</strong>, serving diligently '
            'and seeking the reward of God\'s Kingdom.</p>'
            '<p>We envision a Rwanda and world transformed by the gospel message, where '
            'communities are healed through music, faith is strengthened through worship, '
            'and the Kingdom of God advances through our witness and service.</p>'
        )
        
        # About / History
        settings.about = '''<h2>Our Story: A Legacy of Worship Since 1998</h2>

<h3>The Beginning</h3>
<p>Jehovah Jireh Choir began its worship ministry at Kigali Independent University (ULK) in 1998 
when the university was located at Saint Paul. The choir originated from a small group of 
born-again ULK students associated with CEP (Pentecostal students' congregation).</p>

<h3>The Foundation</h3>
<p>What started with six evening-program students gathering to pray and praise God 
soon became a growing music ministry within the university community. These young 
believers shared a passion for worshipping God and spreading the gospel through music.</p>

<h3>The Name Jehovah Jireh: 2005</h3>
<p>The worship team adopted the name "Jehovah Jireh Choir" in 2005. 
The name is rooted in <strong>Genesis 22:5–15</strong>, meaning 
<strong>"The Lord Will Provide"</strong> – a testament to God's provision and faithfulness 
in all circumstances.</p>

<h3>Growth and Expansion</h3>
<p>Over the years, Jehovah Jireh Choir expanded significantly beyond ULK, serving churches, 
communities, and districts across Rwanda. The choir's ministry grew to include multiple albums, 
tours, evangelization campaigns, and community outreach programs.</p>

<h3>Our Albums</h3>
<ul>
<li><strong>2010:</strong> "INGOMA YA KRISTO NTIZAHANGUKA" (The Throne of Jesus Will Never End)</li>
<li><strong>2014:</strong> "UWITEKA NIWE MANA" (He Is The Only God)</li>
<li><strong>2016:</strong> "UMUKWE ARAJE" (The Bridegroom Is Coming)</li>
<li><strong>2019:</strong> "URUGAMBA NI YESU URUYOBOYE" (The Battle Is Led By Jesus)</li>
</ul>

<h3>Our Ministry Today</h3>
<p>Today, Jehovah Jireh Choir continues its sacred calling to use Gospel music for spiritual 
transformation. Through worship events, evangelization campaigns, concert performances, and 
community ministry, the choir remains committed to:</p>

<ul>
<li>Leading people to faith in Jesus Christ</li>
<li>Encouraging believers in their spiritual growth</li>
<li>Addressing social issues through ministry and awareness</li>
<li>Serving churches and communities across Rwanda</li>
<li>Preserving and promoting Gospel music in Kinyarwanda and English</li>
</ul>

<p><em>Jehovah Jireh – The Lord Provides. He provides vision, voice, and victory to those who believe.</em></p>'''
        
        settings.save()
        self.stdout.write(self.style.SUCCESS('  Site settings updated with mission, vision, and about'))

    def seed_categories(self):
        """Seed article categories"""
        self.stdout.write('Seeding Article Categories...')
        
        categories_data = [
            {'name': 'News', 'icon': 'newspaper', 'color': '#123F78'},
            {'name': 'Evangelization', 'icon': 'campaign', 'color': '#DCA928'},
            {'name': 'Outreach', 'icon': 'handshake', 'color': '#061B38'},
            {'name': 'Concerts', 'icon': 'music_note', 'color': '#C41E3A'},
            {'name': 'Testimonies', 'icon': 'favorite', 'color': '#F6F8FC'},
            {'name': 'Events', 'icon': 'event', 'color': '#123F78'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.update_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                }
            )
            if created:
                self.stdout.write(f"    Created: {category.name}")

        self.stdout.write(self.style.SUCCESS(f'  {len(categories_data)} categories ready'))

    def seed_albums(self):
        """Seed historical albums"""
        self.stdout.write('Seeding Albums...')
        
        albums_data = [
            {
                'title': 'INGOMA YA KRISTO NTIZAHANGUKA',
                'slug': 'ingoma-ya-kristo-ntizahanguka',
                'description': '<p><strong>English: The Throne of Jesus Will Never End</strong></p><p>This album features powerful gospel music celebrating the eternal Kingdom of Christ. Released in 2010, it showcases the choir\'s commitment to spirit-filled worship and proclamation of Christ\'s return.</p>',
                'year': 2010,
                'release_date': date(2010, 1, 1),
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'UWITEKA NIWE MANA',
                'slug': 'uwiteka-niwe-mana',
                'description': '<p><strong>English: He Is The Only God</strong></p><p>Released in 2014, this album emphasizes the monotheistic faith and devotion to the one true God. The collection features songs of praise and worship celebrating God\'s sovereignty and faithfulness.</p>',
                'year': 2014,
                'release_date': date(2014, 1, 1),
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'UMUKWE ARAJE',
                'slug': 'umukwe-araje',
                'description': '<p><strong>English: The Bridegroom Is Coming</strong></p><p>Released in 2016, this album focuses on the eschatological message of the church. Songs prepare believers for Christ\'s second coming with themes of readiness, watchfulness, and eternal hope.</p>',
                'year': 2016,
                'release_date': date(2016, 1, 1),
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'URUGAMBA NI YESU URUYOBOYE',
                'slug': 'urugamba-ni-yesu-uruyoboye',
                'description': '<p><strong>English: The Battle Is Led By Jesus</strong></p><p>Released in 2019, this album features spiritual warfare themes and victory in Christ. The songs emphasize God\'s power over all opposition and the triumph of believers through faith in Jesus.</p>',
                'year': 2019,
                'release_date': date(2019, 1, 1),
                'status': 'published',
                'is_featured': True,
            },
        ]
        
        for album_data in albums_data:
            album, created = Album.objects.update_or_create(
                slug=album_data['slug'],
                defaults={k: v for k, v in album_data.items() if k != 'slug'}
            )
            if created:
                self.stdout.write(f"    Created: {album.title} ({album.year})")

        self.stdout.write(self.style.SUCCESS(f'  {len(albums_data)} albums ready'))

    def seed_songs(self):
        """Seed known songs"""
        self.stdout.write('Seeding Songs...')
        
        songs_data = [
            {
                'title': 'YESU ARIHO',
                'slug': 'yesu-ariho',
                'album_slug': 'ingoma-ya-kristo-ntizahanguka',
                'track_number': 1,
            },
            {
                'title': 'YARANGURANIYE',
                'slug': 'yaranguraniye',
                'album_slug': 'uwiteka-niwe-mana',
                'track_number': 1,
            },
            {
                'title': 'NIBWO BUMANA BWAYO',
                'slug': 'nibwo-bumana-bwayo',
                'album_slug': 'umukwe-araje',
                'track_number': 1,
            },
            {
                'title': 'Ngihanura',
                'slug': 'ngihanura',
                'album_slug': None,
                'track_number': None,
            },
            {
                'title': "Iw'abandi",
                'slug': "iw-abandi",
                'album_slug': None,
                'track_number': None,
            },
        ]
        
        song_count = 0
        for song_data in songs_data:
            album = None
            if song_data['album_slug']:
                try:
                    album = Album.objects.get(slug=song_data['album_slug'])
                except Album.DoesNotExist:
                    album = None
            
            song, created = Song.objects.update_or_create(
                slug=song_data['slug'],
                defaults={
                    'title': song_data['title'],
                    'album': album,
                    'track_number': song_data['track_number'],
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f"    Created: {song.title}")
                song_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {song_count} new songs created'))

    def seed_articles(self, author):
        """Seed news and articles"""
        self.stdout.write('Seeding Articles & News...')
        
        news_category = Category.objects.filter(name='News').first()
        evangelization_category = Category.objects.filter(name='Evangelization').first()
        outreach_category = Category.objects.filter(name='Outreach').first()
        
        articles_data = [
            {
                'title': 'Jehovah Jireh Choir Evangelization Visit to ADEPR Rutagara',
                'slug': 'adepr-rutagara-evangelization-2025',
                'category': evangelization_category,
                'excerpt': 'The choir conducted a spiritual outreach at ADEPR Rutagara in Kabarondo-Kayonza bringing the gospel message through worship and testimony.',
                'content': '<p>Jehovah Jireh Choir visited ADEPR Rutagara in Kabarondo-Kayonza for a special evangelization ministry. The event featured spirit-filled worship, gospel songs, and personal testimonies of faith.</p><p>The visit was part of the choir\'s ongoing commitment to spread the gospel message and encourage believers in their spiritual journey.</p>',
                'published_date': timezone.make_aware(datetime(2025, 5, 18, 10, 0)),
                'status': 'published',
            },
            {
                'title': 'Jehovah Jireh Choir and EFATA Choir at ADEPR Munini-Nyamirambo',
                'slug': 'adepr-munini-nyamirambo-concert',
                'category': evangelization_category,
                'excerpt': 'A joint worship event bringing together Jehovah Jireh Choir and EFATA Choir for a special ministry at ADEPR Munini-Nyamirambo.',
                'content': '<p>Jehovah Jireh Choir joined with EFATA Choir for a united worship event at ADEPR Munini-Nyamirambo. The combined voices created a powerful ministry of praise and intercession.</p><p>This partnership demonstrated the power of unity in the body of Christ through music and shared faith.</p>',
                'published_date': timezone.make_aware(datetime(2025, 3, 15, 14, 0)),
                'status': 'published',
            },
            {
                'title': 'Ministry at ADEPR Kiyanza in Rulindo',
                'slug': 'adepr-kiyanza-rulindo-ministry',
                'category': outreach_category,
                'excerpt': 'Jehovah Jireh Choir conducted spiritual ministry at ADEPR Kiyanza, bringing worship and encouragement to the congregation in Rulindo.',
                'content': '<p>The choir ministered at ADEPR Kiyanza in Rulindo, sharing songs of faith and pastoral encouragement. The service included worship, testimonies, and prayer for the community.</p><p>This outreach reinforced the choir\'s mission to strengthen faith communities through gospel music.</p>',
                'published_date': timezone.make_aware(datetime(2025, 2, 10, 11, 0)),
                'status': 'published',
            },
            {
                'title': 'Jehovah Jireh Choir Addresses Social Issues Through Music Ministry',
                'slug': 'social-outreach-musanze-2024',
                'category': outreach_category,
                'excerpt': 'The choir worked with Musanze District addressing critical social issues including drug abuse, teenage pregnancy, school dropout, and malnutrition through awareness and ministry.',
                'content': '<p>Jehovah Jireh Choir partnered with Musanze District authorities to address pressing social challenges in the community. Through music, testimonies, and community dialogue, the choir contributed to awareness campaigns on:</p><ul><li>Drug abuse prevention</li><li>Teenage pregnancy awareness</li><li>Importance of school attendance</li><li>Nutrition and health</li></ul><p>This multi-faceted ministry demonstrated the choir\'s commitment to holistic community development rooted in Gospel values.</p>',
                'published_date': timezone.make_aware(datetime(2024, 9, 20, 9, 0)),
                'status': 'published',
            },
            {
                'title': 'The History and Mission of Jehovah Jireh Choir',
                'slug': 'about-jehovah-jireh-choir-history',
                'category': news_category,
                'excerpt': 'Learn about Jehovah Jireh Choir\'s rich history beginning at Kigali Independent University (ULK) in 1998 and its evolution as a gospel music ministry.',
                'content': '''<p><strong>Beginning: 1998</strong></p>
<p>Jehovah Jireh Choir began its worship ministry at Kigali Independent University (ULK) when the university was operating at Saint Paul. The choir originated from a small group of born-again ULK students associated with CEP (Pentecostal students' congregation).</p>

<p><strong>The Foundation: A Small Group</strong></p>
<p>The group started with six evening-program students who gathered to pray, worship, and serve God. What began as a very small gathering grew into a music ministry within the university community.</p>

<p><strong>The Name Jehovah Jireh: 2005</strong></p>
<p>The group adopted the name "Jehovah Jireh Choir" in 2005. The name is rooted in Genesis 22:5–15 and expresses faith in God's provision and direction.</p>

<p><strong>Growth and Development</strong></p>
<p>Over the years, the choir expanded significantly, moving beyond the university to serve churches, communities, and districts across Rwanda. The ministry recorded and released multiple albums featuring songs in Kinyarwanda and English, each carrying spiritual themes and messages of faith transformation.</p>

<p><strong>Albums Released</strong></p>
<ul>
<li>2010: "INGOMA YA KRISTO NTIZAHANGUKA" (The Throne of Jesus Will Never End)</li>
<li>2014: "UWITEKA NIWE MANA" (He Is The Only God)</li>
<li>2016: "UMUKWE ARAJE" (The Bridegroom Is Coming)</li>
<li>2019: "URUGAMBA NI YESU URUYOBOYE" (The Battle Is Led By Jesus)</li>
</ul>

<p><strong>Mission and Impact</strong></p>
<p>Jehovah Jireh Choir seeks to use Gospel music to lead people toward transformation, repentance, and becoming born-again believers. Through worship, evangelization, and community ministry, the choir continues its commitment to spreading the gospel message and encouraging spiritual growth.</p>''',
                'published_date': timezone.make_aware(datetime(2024, 8, 9, 12, 0)),
                'status': 'published',
                'is_featured': True,
            },
        ]

        # A complete sample newsroom makes the homepage editorial layout useful
        # immediately after a fresh deployment. These records remain editable in admin.
        category_map = {category.name: category for category in Category.objects.all()}
        sample_news = [
            ('Choir Begins Preparations for the Next Imana Iratsinze Gathering', 'imana-iratsinze-preparations', 'Events', 'Rehearsals and ministry planning have begun for the choir’s next annual worship gathering.'),
            ('Young Singers Join Jehovah Jireh Junior Mentorship Programme', 'junior-mentorship-programme', 'News', 'A new group of young singers has started a season of musical and spiritual mentorship.'),
            ('A Night of Worship, Testimony and Prayer in Kigali', 'night-of-worship-kigali', 'Concerts', 'Believers gathered in Kigali for an evening centred on worship, testimony and prayer.'),
            ('Community Outreach Brings Encouragement to Vulnerable Families', 'community-outreach-vulnerable-families', 'Outreach', 'Choir members visited families and shared practical support, prayer and encouragement.'),
            ('Jehovah Jireh Academy Opens a New Training Season', 'academy-new-training-season', 'News', 'Children are learning worship, choir discipline, music and the history of the ministry.'),
            ('Behind the Music: How the Choir Prepares a New Song', 'behind-the-music-new-song', 'News', 'A look inside the prayer, writing, arrangement and rehearsal process behind every release.'),
            ('Gospel Ministry Visit Strengthens the Church in Musanze', 'gospel-ministry-visit-musanze', 'Evangelization', 'Songs, scripture and testimonies brought a message of hope to believers in Musanze.'),
            ('Post Cepiens Members Share Lessons with University Singers', 'post-cepiens-mentorship-ulk', 'Testimonies', 'Senior members returned to mentor ULK singers and share lessons from their ministry journey.'),
            ('Choir Marks Another Year of God’s Faithfulness', 'another-year-gods-faithfulness', 'Testimonies', 'Members reflected on the provision, growth and transformed lives witnessed through the ministry.'),
            ('Worship Team Completes Weekend Vocal Workshop', 'weekend-vocal-workshop', 'News', 'The workshop focused on vocal health, harmony, stage discipline and serving through excellence.'),
            ('Evangelization Team Announces Community Prayer Visits', 'community-prayer-visits', 'Evangelization', 'Teams will visit communities to pray with families and share the message of Jesus Christ.'),
            ('Four Albums, One Continuing Story of Gospel Music', 'four-albums-gospel-story', 'News', 'The choir looks back at four albums and the messages that continue to encourage listeners.'),
            ('Members Serve Through Hospital Visitation Ministry', 'hospital-visitation-ministry', 'Outreach', 'The ministry shared prayer and encouragement with patients, families and healthcare workers.'),
            ('New Rehearsal Calendar Supports Every Choir Generation', 'new-rehearsal-calendar', 'Events', 'A coordinated rehearsal calendar will bring Academy, Junior, ULK and Post Cepiens together.'),
            ('Testimony: A Song That Restored Hope During a Difficult Season', 'song-restored-hope-testimony', 'Testimonies', 'One listener shares how a Jehovah Jireh song became a source of courage and renewed faith.'),
        ]
        sample_images = [
            'slider/choir-hero-01-desktop.jpg',
            'slider/choir-hero-02-desktop.jpg',
            'slider/choir-hero-03-desktop.jpg',
        ]
        for index, (title, slug, category_name, excerpt) in enumerate(sample_news):
            articles_data.append({
                'title': title,
                'slug': slug,
                'category': category_map.get(category_name, news_category),
                'excerpt': excerpt,
                'content': (
                    f'<p>{excerpt}</p>'
                    '<p>Jehovah Jireh Choir continues to serve God and people through '
                    'worship, evangelization, discipleship and compassionate community ministry.</p>'
                    '<p>Members thanked partners, churches and friends of the ministry for '
                    'their prayers and continued support.</p>'
                ),
                'featured_image': sample_images[index % len(sample_images)],
                'published_date': timezone.now() - timedelta(days=index + 1),
                'status': 'published',
                'is_featured': index == 0,
            })

        # Give the original seed stories imagery as well, without requiring uploads.
        for index, article_data in enumerate(articles_data):
            article_data.setdefault('featured_image', sample_images[index % len(sample_images)])
        
        article_count = 0
        for article_data in articles_data:
            article, created = Article.objects.update_or_create(
                slug=article_data['slug'],
                defaults={
                    'title': article_data['title'],
                    'category': article_data.get('category'),
                    'author': author,
                    'excerpt': article_data.get('excerpt', ''),
                    'content': article_data['content'],
                    'published_date': article_data['published_date'],
                    'status': article_data['status'],
                    'is_featured': article_data.get('is_featured', False),
                    'featured_image': article_data.get('featured_image', ''),
                    'featured_image_alt': article_data['title'],
                }
            )
            if created:
                self.stdout.write(f"    Created: {article.title[:60]}...")
                article_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {article_count} new articles created'))

    def seed_event_types(self):
        """Seed event types"""
        self.stdout.write('Seeding Event Types...')
        
        types_data = [
            {'name': 'Concert', 'icon': 'music_note', 'color': '#C41E3A'},
            {'name': 'Evangelization Outreach', 'icon': 'campaign', 'color': '#DCA928'},
            {'name': 'Worship Service', 'icon': 'favorite', 'color': '#123F78'},
            {'name': 'Album Launch', 'icon': 'album', 'color': '#061B38'},
        ]
        
        for type_data in types_data:
            event_type, created = EventType.objects.update_or_create(
                name=type_data['name'],
                defaults={'icon': type_data['icon'], 'color': type_data['color']}
            )
            if created:
                self.stdout.write(f"    Created: {event_type.name}")

        self.stdout.write(self.style.SUCCESS(f'  {len(types_data)} event types ready'))

    def seed_events(self):
        """Seed historical and upcoming events"""
        self.stdout.write('Seeding Events...')
        
        concert_type = EventType.objects.filter(name='Concert').first()
        evangelization_type = EventType.objects.filter(name='Evangelization Outreach').first()
        worship_type = EventType.objects.filter(name='Worship Service').first()
        
        # Use timezone-aware dates
        from django.utils import timezone
        today = timezone.now().date()
        
        events_data = [
            {
                'title': 'ADEPR Gihundwe',
                'slug': 'adepr-gihundwe-2023',
                'event_type': evangelization_type,
                'location': 'Rusizi',
                'start_date': date(2023, 12, 2),
                'status': 'completed',
                'description': 'Jehovah Jireh Choir ministered at ADEPR Gihundwe in Rusizi.',
                'youtube_livestream_url': '',
            },
            {
                'title': 'IMANA IRATSINZE / Jehovah Jireh Choir Concert',
                'slug': 'imana-iratsinze-concert-2023',
                'event_type': concert_type,
                'location': 'Musanze District',
                'start_date': date(2023, 8, 19),
                'status': 'completed',
                'description': 'A special concert celebrating the goodness and faithfulness of God through spirit-filled worship.',
                'youtube_livestream_url': '',
            },
            {
                'title': 'ADEPR Bukane Ministry',
                'slug': 'adepr-bukane-musanze',
                'event_type': evangelization_type,
                'location': 'Musanze',
                'start_date': date(2023, 6, 15),
                'status': 'completed',
                'description': 'Choir ministry at ADEPR Bukane in Musanze.',
                'youtube_livestream_url': '',
            },
        ]

        event_count = 0
        for event_data in events_data:
            event, created = Event.objects.update_or_create(
                slug=event_data['slug'],
                defaults={
                    'title': event_data['title'],
                    'event_type': event_data['event_type'],
                    'location': event_data.get('location', ''),
                    'venue': event_data.get('venue', ''),
                    'start_date': event_data['start_date'],
                    'start_time': event_data.get('start_time'),
                    'status': event_data['status'],
                    'description': event_data.get('description', ''),
                    'short_description': event_data.get('short_description', ''),
                    'youtube_livestream_url': event_data.get('youtube_livestream_url', ''),
                    'registration_url': event_data.get('registration_url', ''),
                    'ticket_price': event_data.get('ticket_price', ''),
                }
            )
            if created:
                self.stdout.write(f"    Created: {event.title}")
                event_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {event_count} new events created'))

    def seed_evangelization_reports(self):
        """Seed evangelization reports"""
        self.stdout.write('Seeding Evangelization Reports...')
        
        reports_data = [
            {
                'title': 'Evangelization at Kabarondo-Kayonza',
                'slug': 'evangelization-kabarondo-kayonza',
                'location': 'Kabarondo-Kayonza',
                'event_date': date(2025, 5, 18),
                'content': '<p>Jehovah Jireh Choir visited ADEPR Rutagara in Kabarondo-Kayonza for a special evangelization ministry. Through songs, testimonies, and prayer, the choir shared the gospel message of transformation and hope in Christ.</p>',
                'is_published': True,
            },
            {
                'title': 'Ministry at Kiyanza, Rulindo',
                'slug': 'ministry-kiyanza-rulindo',
                'location': 'Rulindo',
                'event_date': date(2025, 2, 10),
                'content': '<p>The choir conducted spiritual ministry at ADEPR Kiyanza in Rulindo, bringing worship, encouragement, and pastoral care to the congregation. The service emphasized faith, perseverance, and God\'s faithfulness.</p>',
                'is_published': True,
            },
            {
                'title': 'Community Outreach in Musanze',
                'slug': 'community-outreach-musanze',
                'location': 'Musanze',
                'event_date': date(2024, 9, 20),
                'content': '<p>In partnership with Musanze District authorities, Jehovah Jireh Choir addressed critical social issues including drug abuse prevention, teenage pregnancy awareness, school dropout rates, and malnutrition. The choir used music and testimonies to raise community consciousness and promote positive change.</p>',
                'is_published': True,
            },
        ]
        
        report_count = 0
        for report_data in reports_data:
            report, created = EvangelizationReport.objects.update_or_create(
                slug=report_data['slug'],
                defaults={
                    'title': report_data['title'],
                    'location': report_data['location'],
                    'event_date': report_data['event_date'],
                    'content': report_data['content'],
                    'is_published': report_data['is_published'],
                }
            )
            if created:
                self.stdout.write(f"    Created: {report.title}")
                report_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {report_count} new evangelization reports created'))

    def seed_gallery(self):
        """Seed gallery albums (without media for now - media requires file uploads)"""
        self.stdout.write('Seeding Gallery Albums...')
        
        albums_data = [
            {
                'name': 'Worship Celebrations',
                'slug': 'worship-celebrations',
                'description': 'Photos from choir worship and celebration events.',
            },
            {
                'name': 'Concert Performances',
                'slug': 'concert-performances',
                'description': 'Live concert performances and stage events.',
            },
            {
                'name': 'Community Ministry',
                'slug': 'community-ministry',
                'description': 'Evangelization and outreach activities in communities.',
            },
        ]
        
        album_count = 0
        
        for album_data in albums_data:
            album, created = GalleryAlbum.objects.update_or_create(
                slug=album_data['slug'],
                defaults={
                    'name': album_data['name'],
                    'description': album_data['description'],
                }
            )
            if created:
                self.stdout.write(f"    Created album: {album.name}")
                album_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {album_count} gallery albums created (media can be added via admin dashboard)'))

    def seed_sponsor_groups(self):
        """Seed sponsor group tiers"""
        self.stdout.write('Seeding Sponsor Groups...')
        
        groups_data = [
            {
                'name': 'Individual',
                'slug': 'individual',
                'description': '<p>Support Jehovah Jireh Choir as an individual believer or contributor.</p>',
                'benefits': '<ul><li>Recognition as a supporter</li><li>Updates on choir ministry</li><li>Invitations to special events</li></ul>',
                'color': '#123F78',
            },
            {
                'name': 'Inkoramutima',
                'slug': 'inkoramutima',
                'description': '<p>Inkoramutima is a group of committed friends and supporters dedicated to the advancement of Jehovah Jireh Choir ministry. This supporter group works collaboratively to strengthen the choir\'s mission and expand its gospel outreach.</p>',
                'benefits': '<ul><li>Dedicated supporter status</li><li>Regular updates and exclusive news</li><li>Special acknowledgment in materials</li><li>Priority invitations to events</li></ul>',
                'color': '#DCA928',
            },
            {
                'name': 'Inkingi z\'Iterambere',
                'slug': 'inkingi-z-iterambere',
                'description': '<p>Strategic partners in the choir\'s growth and development. Together we work toward expanding the kingdom of God through music ministry.</p>',
                'benefits': '<ul><li>Featured sponsor recognition</li><li>Co-branding opportunities</li><li>Regular partnership communication</li><li>Invitation to planning meetings</li><li>Event sponsorship options</li></ul>',
                'color': '#061B38',
            },
        ]
        
        for group_data in groups_data:
            group, created = SponsorGroup.objects.update_or_create(
                slug=group_data['slug'],
                defaults={
                    'name': group_data['name'],
                    'description': group_data['description'],
                    'benefits': group_data['benefits'],
                    'color': group_data['color'],
                }
            )
            if created:
                self.stdout.write(f"    Created: {group.name}")

        self.stdout.write(self.style.SUCCESS(f'  {len(groups_data)} sponsor groups ready'))

    def seed_hero_slides(self):
        """Seed homepage hero slider"""
        self.stdout.write('Seeding Hero Slider Slides...')
        
        slides_data = [
            {
                'title': 'Worship',
                'order': 1,
                'heading': 'WE WORSHIP.\nWE EVANGELIZE.\nWE TRANSFORM LIVES.',
                'highlighted_text': 'WE TRANSFORM LIVES.',
                'description': 'Encounter God through worship and experience His transforming presence in spirit-filled music.',
                'button_1_text': 'LISTEN TO OUR MUSIC',
                'button_1_url': '/music/albums/',
                'button_2_text': 'OUR MINISTRY',
                'button_2_url': '/ministry/',
                'text_align': 'left',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Our Story',
                'order': 2,
                'heading': 'A LEGACY OF WORSHIP\nSince 1998',
                'highlighted_text': 'Since 1998',
                'description': 'From a small group of students at ULK to a thriving gospel music ministry serving Rwanda and beyond.',
                'button_1_text': 'OUR STORY',
                'button_1_url': '/about/',
                'button_2_text': 'MEET THE CHOIR',
                'button_2_url': '/about/#committee',
                'text_align': 'left',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Our Music',
                'order': 3,
                'heading': 'GOSPEL MUSIC\nWITH A MESSAGE',
                'highlighted_text': 'WITH A MESSAGE',
                'description': 'More than 80 original songs, four completed albums, and a fifth album in development.',
                'button_1_text': 'EXPLORE OUR SONGS',
                'button_1_url': '/music/albums/',
                'button_2_text': 'LATEST ALBUM',
                'button_2_url': '/music/albums/urugamba-ni-yesu-uruyoboye/',
                'text_align': 'left',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Evangelization',
                'order': 4,
                'heading': 'REACHING HEARTS\nTHROUGH MINISTRY',
                'highlighted_text': 'THROUGH MINISTRY',
                'description': 'Spreading the gospel message through evangelization, outreach, and community service across Rwanda.',
                'button_1_text': 'OUR MINISTRY',
                'button_1_url': '/ministry/',
                'button_2_text': 'READ MORE',
                'button_2_url': '/news/',
                'text_align': 'left',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Support',
                'order': 5,
                'heading': 'BE PART OF\nOUR MISSION',
                'highlighted_text': 'OUR MISSION',
                'description': 'Join us in spreading the gospel and transforming lives through music and community ministry.',
                'button_1_text': 'BECOME A SPONSOR',
                'button_1_url': '/sponsors/become-a-sponsor/',
                'button_2_text': 'CONTACT US',
                'button_2_url': '/contact/',
                'text_align': 'left',
                'is_active': True,
                'is_featured': True,
            },
        ]
        
        slide_count = 0
        for slide_data in slides_data:
            slide, created = SliderSlide.objects.update_or_create(
                order=slide_data['order'],
                defaults={k: v for k, v in slide_data.items() if k != 'order'}
            )
            if created:
                self.stdout.write(f"    Created: Slide {slide.order} - {slide.title}")
                slide_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {slide_count} new hero slides created'))

    def seed_authoritative_content(self):
        """Apply the supplied choir-history facts over older generated copy."""
        self.stdout.write('Seeding authoritative history and ministry content...')

        pages = {
            'home': {
                'title': 'Jehovah Jireh Choir', 'eyebrow': 'Who We Are',
                'summary': 'Jehovah Jireh began at ULK in 1998 as a small student worship ministry and has grown into a multigenerational Gospel ministry focused on worship, evangelization, music, service, and preparing future generations.',
                'featured_image': 'slider/choir-hero-01-desktop.jpg',
                'featured_image_alt': 'Jehovah Jireh Choir singing together during worship',
                'body': '<p>For Jehovah Jireh, singing is not simply performance. It is a means of serving God, proclaiming the Gospel, and serving people.</p>',
            },
            'about': {
                'title': 'About Jehovah Jireh Choir', 'eyebrow': 'Who We Are',
                'summary': 'A multigenerational Gospel ministry born at Kigali Independent University (ULK) in 1998.',
                'body': '''<h2>Worship, Gospel and Service</h2><p>Jehovah Jireh began with six evening-program students who belonged to Groupe de Prière des Étudiants Pentecôtistes Universitaires (GPEPU), later known as CEP — Communautés des Étudiants Pentecôtistes. They were committed to prayer, worship, and service to God despite very limited resources.</p><p>For Jehovah Jireh, singing is not simply performance. It is a way to serve God, proclaim the Gospel, and serve people. Today the ministry brings together more than 160 singers across generations, has composed more than 80 original songs, completed four albums, and is preparing a fifth.</p><h2>Jehovah Jireh Today</h2><p>The choir remains focused on worship, evangelization, composing and singing Gospel music, helping vulnerable people, developing young people in ministry, and pursuing spiritual, musical, administrative, and organizational growth.</p><h2>Generational Pathway</h2><p><strong>Jehovah Jireh Academy → Jehovah Jireh Junior → Jehovah Jireh ULK → Jehovah Jireh ULK Post Cepiens</strong></p><p>This pathway supports continuity, mentorship, and the passing on of the ministry from one generation to another.</p>''',
            },
            'history': {
                'title': 'Our History', 'eyebrow': 'A Journey of Faith Since 1998',
                'summary': 'From six ULK students committed to prayer and worship to a ministry serving across generations.',
                'body': '''<h2>Our Beginnings — 1998</h2><p>Jehovah Jireh began its ministry at Kigali Independent University (ULK) in 1998. Six students in the evening program, members of Groupe de Prière des Étudiants Pentecôtistes Universitaires (GPEPU), gathered for prayer, worship, and service to God. GPEPU later became CEP — Communautés des Étudiants Pentecôtistes.</p><p>Professeur DUSHIMIRIMANA Jean de Dieu was the first leader of the singers, while GPEPU was led at the time by KAREMERA Fiston.</p><h2>The Early Years</h2><p>The group faced very few singers, limited musical capacity, a lack of confidence, and the departure of members after university. At one point only four members remained. They persevered in prayer, asking God to grow and sustain the ministry.</p><h2>The “Ibyihare / Ikihare” Period</h2><p>During this difficult period the group informally called itself Ibyihare or Ikihare, reflecting its perseverance and persistence.</p><h2>The Kimicanga Story</h2><p>Kimicanga holds an important place in the choir’s early journey and is remembered as part of the setting in which the young ministry continued to develop.</p><h2>Beginning to Compose Original Songs</h2><p>At first the group sang songs by other artists and choirs. Later, Jacques NTAKIRA began composing songs for the group, opening a new chapter in its musical identity.</p><h2>How Our Name Was Born</h2><p>In 2005, CEP ULK Soir leadership—including Pastor BUDIGIRI Herman and KAMPAYANA Jean de Dieu—considered giving the growing group a distinct choir name. Several names were written and discussed, including JEHOVAH JIREH. Senior members were consulted, and Prof. DUSHIMIRIMANA Jean de Dieu selected the name JEHOVAH JIREH.</p><h2>What Jehovah Jireh Means</h2><p>Rooted in Genesis 22:5–15, Jehovah Jireh proclaims that God provides and makes provision. The name became a testimony, an expression of faith, and confidence that God would provide direction and everything needed for the ministry.</p><blockquote><p>“Uwiteka ni we uzatanga icyerekezo cyiza.”</p></blockquote><h2>Passing the Ministry to Future Generations</h2><p>Graduates remain connected, sharing mentorship, testimonies, knowledge, and support. This structured approach to continuity helps preserve the ministry and pass it faithfully to future generations.</p>''',
            },
            'mission-vision': {
                'title': 'Mission & Vision', 'eyebrow': 'Serving God and People',
                'summary': 'Singing is a means of serving God, proclaiming the Gospel, and serving people.',
                'body': '<h2>Our Mission</h2><p>To worship and serve God, proclaim the Gospel through music and evangelization, and serve people through compassionate ministry.</p><h2>Our Vision</h2><p>To nurture a spiritually grounded and musically growing ministry that carries Jehovah Jireh’s faith, history, and values faithfully from one generation to the next.</p><h2>Our Commitment</h2><p>We pursue spiritual growth, musical growth, responsible administration and management, development, and evangelization in Rwanda and beyond.</p>',
                'closing_statement': 'JEHOVAH JIREH — UWITEKA AZITANGIRA.',
            },
            'academy': {
                'title': 'Jehovah Jireh Academy', 'eyebrow': 'Preparing Future Generations',
                'summary': 'A pillar for preserving the ministry by forming children in worship, music, service, values, history, and heritage.',
                'body': '<h2>Learning the Ministry from an Early Age</h2><p>Jehovah Jireh Academy prepares future generations, particularly children of parents who have been part of Jehovah Jireh. Children are introduced to singing, music, worship, serving God, Jehovah Jireh values, the choir’s history, and its ministry heritage.</p><p>The Academy helps ensure that faith, knowledge, values, and service are passed forward with care.</p>',
            },
            'legacy': {
                'title': 'Our Legacy', 'eyebrow': 'Faith Across Generations',
                'summary': 'A journey from six founding students—and once only four remaining—to more than 160 singers today.',
                'body': '<p>Jehovah Jireh’s legacy includes more than 80 original songs, four completed albums, a fifth album in development, evangelization in Rwanda and abroad, more than seven leadership committees, and the recurring Imana Iratsinze event.</p><p>The Academy, Junior, ULK, and Post Cepiens structures help graduates and younger members remain connected through mentorship, testimony, knowledge, support, and service.</p>',
            },
            'future': {
                'title': 'Our Future', 'eyebrow': 'Passing the Ministry Forward',
                'summary': 'Preparing children and young people to carry the ministry’s faith, history, values, and service into the future.',
                'body': '<p>The future vision emphasizes Jehovah Jireh Academy, teaching children from an early age, preserving the choir’s history and values, and transferring the ministry responsibly from one generation to another.</p><p>Through worship, training, mentorship, and service, Jehovah Jireh seeks to ensure that the ministry continues long into the future.</p>',
                'closing_statement': 'JEHOVAH JIREH — UWITEKA AZITANGIRA.',
            },
            'evangelization': {
                'title': 'Evangelization & Community Ministry', 'eyebrow': 'The Gospel Beyond the Stage',
                'summary': 'Serving through evangelization, hospital visits, prison ministry, and compassionate community outreach.',
                'body': '<p>Jehovah Jireh has carried out evangelization in Rwanda and outside Rwanda, including a documented ministry trip to Ngozi, Burundi.</p><p>The ministry has also included visiting patients in hospitals, taking the Gospel to prisons and correctional facilities, helping people facing different difficulties, supporting community and social-welfare activities, and walking with people through different life situations.</p><p>Singing is not simply performance; it is a means of serving God, proclaiming the Gospel, and serving people.</p>',
            },
            'imana-iratsinze': {
                'title': 'IMANA IRATSINZE', 'eyebrow': 'Annual Worship Gathering',
                'summary': 'A recurring Jehovah Jireh event centered on worship, praise, testimonies, and Gospel proclamation.',
                'body': '<p>IMANA IRATSINZE brings together Christians, artists, choirs, friends, and supporters of God’s ministry for worship, praise, testimonies, and proclamation of the Gospel.</p><p>Future and previous editions may include confirmed photos, videos, livestreams, and guest artists or choirs as those records become available.</p>',
            },
        }
        for slug, defaults in pages.items():
            ContentPage.objects.update_or_create(slug=slug, defaults={**defaults, 'is_published': True})

        statistics = [
            ('founded', '1998', 'Ministry Began', 'At ULK with six evening-program students'),
            ('members', '160+', 'Choir Members', 'Singers across generations'),
            ('songs', '80+', 'Original Songs', 'Composed by the ministry'),
            ('albums', '4', 'Released Albums', 'Completed albums'),
            ('leadership-generations', '7+', 'Leadership Generations', 'Committees over the years'),
        ]
        SiteStatistic.objects.filter(key='album-production').delete()
        for order, (key, value, label, detail) in enumerate(statistics, 1):
            SiteStatistic.objects.update_or_create(key=key, defaults={
                'value': value, 'label': label, 'detail': detail, 'order': order,
                'show_on_homepage': key != 'leadership-generations', 'is_active': True,
            })

        milestones = [
            ('1998', 'Ministry begins at ULK', 'Six evening-program students begin gathering for prayer, worship, and service through GPEPU.'),
            ('2000', 'GPEPU becomes CEP', 'The university Pentecostal student prayer community becomes known as CEP.'),
            ('2005', 'The name Jehovah Jireh is adopted', 'After considering several names and consulting senior members, the group adopts Jehovah Jireh.'),
            ('2010', 'Umucyo Gospel Award', 'At Mbambino Super City in Kabuga, the choir places fourth and receives a certificate in the Radio Umucyo-organized award.'),
            ('2012', 'Post Cepiens continuity strengthened', 'More than 30 choir members graduate from ULK and continue through Jehovah Jireh ULK Post Cepiens while the school-based group continues.'),
            ('Today', 'A multigenerational ministry', 'More than 160 singers, 80+ original songs, four completed albums, and a fifth album in development.'),
        ]
        for order, (year, title, description) in enumerate(milestones, 1):
            TimelineMilestone.objects.update_or_create(year=year, defaults={
                'title': title, 'description': description, 'order': order, 'is_active': True,
            })

        ministry_areas = [
            ('worship-music', 'Worship & Music', 'Serving God and proclaiming the Gospel through worship, singing, and original Gospel music.', '/music/albums/'),
            ('evangelization', 'Evangelization', 'Sharing the Gospel in Rwanda and abroad, including the documented ministry journey to Ngozi, Burundi.', '/ministry/evangelization/'),
            ('community-service', 'Community Service', 'Hospital ministry, prison and correctional outreach, and help for people facing difficult circumstances.', '/ministry/evangelization/'),
            ('events', 'Events', 'Gatherings for worship, praise, testimony, fellowship, and Gospel proclamation.', '/events/'),
            ('generational-ministry', 'Generational Ministry', 'Academy, Junior, ULK, and Post Cepiens carrying the ministry forward through mentorship and service.', '/about/academy/'),
            ('support', 'Support Our Mission', 'Partner with worship, evangelization, community service, and formation of future generations.', '/sponsors/become-a-sponsor/'),
        ]
        for order, (slug, title, summary, link_url) in enumerate(ministry_areas, 1):
            MinistryArea.objects.update_or_create(slug=slug, defaults={
                'title': title, 'summary': summary, 'link_url': link_url,
                'order': order, 'show_on_homepage': True, 'is_active': True,
            })

        slides = [
            ('Worship & Mission', 'WE WORSHIP. WE EVANGELIZE.', 'WE SERVE GOD AND PEOPLE.', 'For Jehovah Jireh, singing is a means of serving God, proclaiming the Gospel, and serving people.', 'DISCOVER OUR MINISTRY', '/ministry/evangelization/'),
            ('Our Story', 'A JOURNEY OF FAITH', 'SINCE 1998', 'From six ULK students committed to prayer and worship to a ministry serving across generations.', 'READ OUR STORY', '/history/'),
            ('Music', 'MORE THAN 80 SONGS', 'OF FAITH', 'A growing Gospel music legacy with four completed albums and a fifth in development.', 'EXPLORE OUR MUSIC', '/music/albums/'),
            ('Evangelization', 'THE GOSPEL', 'BEYOND THE STAGE', 'Serving through evangelization, hospital visits, prison ministry, and community outreach.', 'OUR MINISTRY', '/ministry/evangelization/'),
            ('Legacy', 'BUILDING THE', 'NEXT GENERATION', 'From Jehovah Jireh Academy to Junior, ULK and Post Cepiens, the ministry is being passed forward.', 'DISCOVER OUR LEGACY', '/about/legacy/'),
        ]
        for order, (title, heading, highlighted, description, button, url) in enumerate(slides, 1):
            SliderSlide.objects.update_or_create(order=order, defaults={
                'title': title, 'heading': heading, 'highlighted_text': highlighted,
                'description': description, 'button_1_text': button, 'button_1_url': url,
                'button_2_text': '', 'button_2_url': '', 'text_align': 'left',
                'is_active': True, 'is_featured': True,
            })

        imana_type, _ = EventType.objects.update_or_create(
            slug='imana-iratsinze', defaults={
                'name': 'Imana Iratsinze', 'icon': 'celebration',
                'color': '#DCA928', 'is_active': True,
            }
        )
        Event.objects.filter(slug__icontains='imana-iratsinze').update(event_type=imana_type)

        Event.objects.filter(slug__in=[
            'worship-service-september-2026', 'kigali-worship-celebration-2026',
            'mountain-top-evangelization-2026',
        ]).delete()

        history_article = Article.objects.filter(slug='about-jehovah-jireh-choir-history').first()
        if history_article:
            history_article.excerpt = 'The documented journey from six ULK students in 1998 to a multigenerational Gospel ministry.'
            history_article.content = ContentPage.objects.get(slug='history').body
            history_article.save()

        settings = SiteSettings.get_settings()
        settings.about = ContentPage.objects.get(slug='about').body
        settings.mission = ContentPage.objects.get(slug='mission-vision').body
        settings.vision = '<p>To preserve and pass on Jehovah Jireh’s ministry, faith, history, and values from one generation to another.</p>'
        settings.tagline = 'We Worship. We Evangelize. We Serve God and People.'
        settings.footer_text = 'Jehovah Jireh is a multigenerational Gospel ministry serving God and people through worship, evangelization, music, and compassionate outreach since 1998.'
        settings.save()

        self.stdout.write(self.style.SUCCESS('  Authoritative content updated'))

    def seed_partners(self):
        """Seed ministry partners"""
        self.stdout.write('Seeding Partners...')
        
        # Note: Only adding verified partners from official sources
        # Not creating fictional corporate partners
        partners_data = [
            {
                'name': 'Kigali Independent University (ULK)',
                'description': 'The birthplace of Jehovah Jireh Choir in 1998, where the ministry began as a small group of born-again students.',
                'partner_type': 'educational',
            },
            {
                'name': 'ADEPR Churches Network',
                'description': 'Partnership in evangelization and ministry with various ADEPR congregations across Rwanda.',
                'partner_type': 'ministry',
            },
        ]
        
        partner_count = 0
        for partner_data in partners_data:
            partner, created = Partner.objects.update_or_create(
                name=partner_data['name'],
                defaults={
                    'description': partner_data['description'],
                    'partner_type': partner_data['partner_type'],
                }
            )
            if created:
                self.stdout.write(f"    Created: {partner.name}")
                partner_count += 1

        self.stdout.write(self.style.SUCCESS(f'  {partner_count} new partners created'))
