from django.db import migrations


def create_ministry_sidebar_position(apps, schema_editor):
    AdPosition = apps.get_model('advertising', 'AdPosition')
    AdPosition.objects.get_or_create(
        slug='homepage-ministry-sidebar',
        defaults={
            'name': 'Homepage Ministry Sidebar',
            'description': 'Vertical or stacked advertisements beside the homepage ministry newsroom.',
            'recommended_width': 300,
            'recommended_height': 600,
            'is_active': True,
        },
    )


def remove_ministry_sidebar_position(apps, schema_editor):
    AdPosition = apps.get_model('advertising', 'AdPosition')
    AdPosition.objects.filter(slug='homepage-ministry-sidebar').delete()


class Migration(migrations.Migration):
    dependencies = [('advertising', '0001_initial')]
    operations = [migrations.RunPython(create_ministry_sidebar_position, remove_ministry_sidebar_position)]
