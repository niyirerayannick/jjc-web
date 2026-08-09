#!/bin/sh
set -eu

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ "${RUN_SEED_ON_DEPLOY:-false}" = "true" ]; then
    echo "Running the guarded Coolify seed..."
    python manage.py seed_coolify
fi

echo "Linking available persistent media to seeded records..."
python manage.py link_coolify_media

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
