#!/bin/sh
set -eu

fixture="${1:-/tmp/site-transfer/deployment/data/site-data.json}"

if [ ! -f "$fixture" ]; then
    echo "Fixture not found: $fixture" >&2
    exit 1
fi

echo "Applying migrations before import..."
python manage.py migrate --noinput

echo "Importing site content into PostgreSQL..."
python manage.py loaddata "$fixture"

echo "Rebuilding static files..."
python manage.py collectstatic --noinput

echo "Import complete. Verify the homepage and dashboard before removing the transfer archive."
