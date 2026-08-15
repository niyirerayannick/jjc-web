from django.db import migrations


CONTENT_MODELS = (
    'ContentPage',
    'MinistryArea',
    'SiteStatistic',
    'TimelineMilestone',
)


def create_missing_content_tables(apps, schema_editor):
    """Repair databases whose migration history exists without CMS tables."""
    existing_tables = set(schema_editor.connection.introspection.table_names())
    for model_name in CONTENT_MODELS:
        model = apps.get_model('core', model_name)
        if model._meta.db_table not in existing_tables:
            schema_editor.create_model(model)
            existing_tables.add(model._meta.db_table)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_contentpage_featured_image_and_more'),
    ]

    operations = [
        migrations.RunPython(create_missing_content_tables, migrations.RunPython.noop),
    ]
