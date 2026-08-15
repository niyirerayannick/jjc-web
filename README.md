# Jehovah Jireh Choir Website

Django website and content-management system for Jehovah Jireh Choir – ULK.

## Run locally with Docker

Local development uses SQLite. PostgreSQL is used only by the production
configuration.

### Requirements

- Docker Desktop
- Docker Compose (included with Docker Desktop)

### First-time setup

Open PowerShell in the project directory:

```powershell
cd C:\Users\User\Desktop\jjc-web
```

Build the application image:

```powershell
docker compose build
```

Apply database migrations:

```powershell
docker compose run --rm web python manage.py migrate
```

Populate or update the CMS content:

```powershell
docker compose run --rm web python manage.py seed_choir_data
```

Start the development server:

```powershell
docker compose up
```

Open the website at [http://localhost:8000/](http://localhost:8000/).

### Common Docker commands

Run the website in the background:

```powershell
docker compose up -d
```

Follow the Django logs:

```powershell
docker compose logs -f web
```

Stop and remove the local containers:

```powershell
docker compose down
```

Rebuild and restart after changing dependencies or the Docker configuration:

```powershell
docker compose up --build
```

Run Django checks inside the container:

```powershell
docker compose run --rm web python manage.py check
```

The local SQLite database is stored in `db.sqlite3` within the project directory,
so its data remains available when the container is stopped or recreated.

## Production media persistence

Dashboard uploads are stored under `/app/media`. When deploying the Dockerfile
directly in Coolify, configure a persistent volume whose destination is exactly:

```text
/app/media
```

Without this mount, uploaded logos and photographs are deleted whenever Coolify
replaces the application container. If deploying with `docker-compose.prod.yml`,
the `media_data` volume is already declared. See `COOLIFY_DEPLOYMENT.md` for the
complete production setup.
