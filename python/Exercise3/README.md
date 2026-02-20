   In this folder you'll now find a `Dockerfile` and `docker-compose.yml` that
   launch a Django development server on port 8000 and a PostgreSQL 15 database.
   The compose file mounts the source so you can make code changes without rebuilding
   the image. A `requirements.txt` is included with `Django` and `psycopg2-binary`.

   **Quick usage:**
   ```sh
   docker-compose up --build
   ```
   Then browse to `http://localhost:8000`. Adjust `DATABASE_URL` or settings as needed.



   A minimal Django project has been scaffolded in this folder (see
   `manage.py` and the `project/` package). Starting the compose stack will
   allow the development server to start without errors. You can extend the
   project or replace it with your own; just ensure a `manage.py` exists at
   the repository root.

   Once the containers are running you can run migrations and create a superuser:
   ```sh
   docker-compose run app python manage.py migrate
   docker-compose run app python manage.py createsuperuser
   ```
