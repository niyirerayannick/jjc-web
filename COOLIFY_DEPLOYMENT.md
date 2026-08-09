# Coolify production deployment

This project deploys as a Docker Compose application containing Django/Gunicorn and Nginx. PostgreSQL is created as a separate Coolify database resource; uploaded media uses a persistent Docker volume.

## 1. Prepare the repository

Commit and push the application source, but never commit `.env`, `db.sqlite3`, `media/`, `deployment/data/`, or `deployment/site-transfer.tar.gz`.

Generate a strong Django key locally:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 2. Create the Coolify resource

1. In Coolify, create a new resource from the Git repository.
2. Select Docker Compose and use `docker-compose.prod.yml`.
3. Assign the public domain to the `nginx` service on port `80`.
4. Keep the `media_data` and `static_data` volumes persistent.
5. Create a PostgreSQL database resource in the same Coolify project and environment. Use its internal connection URL, not its public URL.

Set these runtime environment variables in Coolify:

```dotenv
SECRET_KEY=<generated-secret>
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
SITE_URL=https://example.com
DATABASE_URL=postgresql://USER:PASSWORD@POSTGRES_INTERNAL_HOST:5432/DATABASE
DEFAULT_FROM_EMAIL=Jehovah Jireh Choir <noreply@example.com>
```

To seed a brand-new database directly during the first Coolify deployment, also set:

```dotenv
RUN_SEED_ON_DEPLOY=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=<strong-unique-admin-password>
```

After the first successful deployment, change `RUN_SEED_ON_DEPLOY` to `false`. The guarded command refuses to overwrite a database that already contains articles, albums, events, or slides.

Add SMTP variables when email delivery is ready. Sensitive values should be runtime-only variables. The compose file marks required variables so Coolify stops before an incomplete deployment.

Deploy once. The web entrypoint automatically runs migrations and collects static files on every release.

## 3. Export local SQLite content and media

From the repository root on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File deployment/export-local-data.ps1
```

This creates the private, Git-ignored file `deployment/site-transfer.tar.gz`. It contains:

- the application fixture, including users and hashed passwords;
- CMS articles, slides, albums, events, settings, and related site data;
- uploaded media files.

Generated Django permissions, sessions, login-attempt logs, thumbnails, admin logs, and advertising analytics are intentionally excluded.

## 4. Back up production before any later re-import

For the first import the database is normally empty. Before repeating an import, create a PostgreSQL backup from the Coolify server:

```bash
docker exec <postgres-container> pg_dump -U <database-user> -d <database-name> -Fc > jjc-before-import.dump
```

Also back up the media volume. Never import over an active production site without this backup.

## 5. Transfer and import

Upload the private archive to the server, for example:

```powershell
scp deployment/site-transfer.tar.gz root@SERVER_IP:/tmp/site-transfer.tar.gz
```

On the server, identify the running web container and transfer archive:

```bash
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}'
mkdir -p /tmp/jjc-transfer
tar -xzf /tmp/site-transfer.tar.gz -C /tmp/jjc-transfer
docker cp /tmp/jjc-transfer/. <web-container>:/tmp/site-transfer/
docker exec <web-container> python /app/seed_production.py
```

The Python seeder imports the fixture and copies media into the persistent `/app/media` volume. It refuses to run when application data already exists unless `--force` is supplied. Always create backups before using `--force`.

## 6. Verify before going public

Check all of the following:

- `/` loads over HTTPS without a redirect loop;
- `/admin/` and `/dashboard/` accept the imported administrator account;
- hero, article, album, event, gallery, sponsor, and advertisement images load;
- category filters and HTMX pagination work;
- form submissions pass CSRF validation;
- new media uploads remain after a redeploy;
- emails work once SMTP is configured;
- PostgreSQL and media backups are scheduled.

After verification, remove `/tmp/site-transfer.tar.gz` and `/tmp/jjc-transfer` from the server because the archive contains private site data.

## Rollback

If validation fails, stop writes to the site, restore the PostgreSQL dump and media backup, then redeploy the previous working commit. Do not repeatedly run `loaddata` against a database that has received new production content.
