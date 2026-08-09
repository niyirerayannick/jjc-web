#!/bin/sh
set -eu

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ "${RUN_SEED_ON_DEPLOY:-false}" = "true" ]; then
    echo "Running the guarded Coolify seed..."
    python manage.py seed_coolify
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
