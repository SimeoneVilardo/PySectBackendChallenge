docker compose exec web-local python manage.py migrate
docker compose exec web-local python manage.py collectstatic
docker compose exec web-local python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')"
foo