#!/bin/ash
echo "Creating Migrations..."
echo "Creating Migrations for admin"
python manage.py makemigrations admin 

echo "Creating Migrations for auth"
python manage.py makemigrations auth

echo "Creating Migrations for loan"
python manage.py makemigrations loan 

python manage.py makemigrations

echo ====================================

echo "Starting Migrations..."
python manage.py migrate admin
python manage.py migrate auth
python manage.py migrate loan
python manage.py migrate

echo ====================================

  python ingest.py
#  python manage.py runserver

# Execute the command passed as arguments
exec "$@"