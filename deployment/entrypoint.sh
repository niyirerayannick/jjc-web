#!/bin/sh
set -eu

# manage.py defaults to development/SQLite for local use. A production image
# must set this before running migrations so startup and Gunicorn use the same
# PostgreSQL database even when the platform only builds the Dockerfile.
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

echo "Using Django settings: ${DJANGO_SETTINGS_MODULE}"
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Verifying CMS database tables..."
python manage.py shell -c "from django.db import connection; required={'core_contentpage','core_ministryarea','core_sitestatistic','core_timelinemilestone'}; missing=required-set(connection.introspection.table_names()); assert not missing, 'Missing database tables after migration: ' + ', '.join(sorted(missing)); print('CMS database schema verified.')"

if [ "${RUN_SEED_ON_DEPLOY:-false}" = "true" ]; then
    echo "Running the guarded Coolify seed..."
    python manage.py seed_coolify
fi

echo "Linking available persistent media to seeded records..."
python manage.py link_coolify_media

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
