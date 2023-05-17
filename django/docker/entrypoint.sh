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

echo 'Loading data...'
python manage.py loaddata **/fixtures/*.json

python manage.py runserver 0.0.0.0:8000
