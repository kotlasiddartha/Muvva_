Railway deployment notes for Muvva Django app

1. Connect repo to Railway and create a new Project.
2. Add the Postgres plugin in Railway (this will create a DATABASE_URL env var).
3. Set the following environment variables in Railway (Project -> Variables):
   - SECRET_KEY: a secure random string
   - DEBUG: False
   - ALLOWED_HOSTS: the railway app domain(s), comma-separated
   - (DATABASE_URL is set automatically by the Postgres plugin)
4. Ensure a Procfile is present (this repo includes one):
   web: gunicorn Muvva_.wsgi --bind 0.0.0.0:$PORT
5. Trigger a deploy. After the deploy completes, run the following in Railway's console:
   python manage.py migrate
   python manage.py collectstatic --noinput
6. Optionally add S3 for media storage in production; Railway filesystem is ephemeral.

Local testing:
1. Copy `.env.example` to `.env` and fill values for local testing.
2. Create a virtualenv and install requirements:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r Muvva_\requirements.txt
3. Run locally:
   python manage.py migrate
   python manage.py runserver

Notes:
- Keep SECRET_KEY secret and do not commit `.env` to git.
- Use the Railway web console to run one-off management commands.
