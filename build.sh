#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

# Create superuser if ADMIN_PASSWORD is set
if [[ -n "${ADMIN_PASSWORD}" ]]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput --username admin \
    --email admin@example.com
fi 