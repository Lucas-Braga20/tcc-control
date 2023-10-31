#!/bin/bash

echo "Waiting for database creation..."
until mysql --user=$MYSQL_USER --password=$MYSQL_PASSWORD --host=$MYSQL_HOST $MYSQL_DATABASE; do
  sleep 1
done
echo "Database successfully created!"

echo 'Generate migrations...'
python manage.py makemigrations

echo 'Migrating...'
python manage.py migrate

if [[ "$DJANGO_SETTINGS_MODULE" == "tcc_control.settings.development" ]]; then
  echo 'Loading data...'
  python manage.py loaddata **/fixtures/*.json
fi

echo 'Collecting static...'
python manage.py collectstatic --noinput

echo 'Compressing static files...'
python manage.py compress

celery -A tcc_control worker --autoscale=3,1 --loglevel=INFO &
celery -A tcc_control beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

if [[ "$DJANGO_SETTINGS_MODULE" == "tcc_control.settings.production" ]]; then
  gunicorn tcc_control.wsgi:application --bind 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000
fi
