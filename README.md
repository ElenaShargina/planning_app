# My great planning app

docker compose up -d

docker compose restart

# Run migrations for the new models
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Restart to pick up code changes
docker compose restart web

user
admin nopassword