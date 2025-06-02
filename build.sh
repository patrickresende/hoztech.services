#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Checking static files integrity..."
if [ -f "static/images/logo.png" ]; then
    echo "Logo file exists"
    file static/images/logo.png
    ls -l static/images/logo.png
else
    echo "ERROR: Logo file not found!"
    exit 1
fi

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Verifying collected files..."
if [ -f "staticfiles/images/logo.png" ]; then
    echo "Collected logo file exists"
    file staticfiles/images/logo.png
    ls -l staticfiles/images/logo.png
else
    echo "ERROR: Collected logo file not found!"
    exit 1
fi

echo "Running migrations..."
python manage.py migrate

# Create superuser if ADMIN_PASSWORD is set
if [[ -n "${ADMIN_PASSWORD}" ]]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput --username admin \
    --email admin@example.com
fi 