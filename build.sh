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

echo "Building Tailwind CSS..."
if [ -f "tailwind.config.js" ]; then
    echo "Tailwind config exists, building CSS..."
    npm run build
else
    echo "No Tailwind config found, skipping CSS build"
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

echo "Verifying admin templates..."
if [ -d "staticfiles/admin" ]; then
    echo "Admin static files collected successfully"
    ls -la staticfiles/admin/
else
    echo "ERROR: Admin static files not found!"
    exit 1
fi

if [ -d "core/templates/admin" ]; then
    echo "Admin templates exist"
    ls -la core/templates/admin/
else
    echo "ERROR: Admin templates not found!"
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

echo "Checking WSGI configuration..."
if [ -f "hoztechsite/wsgi.py" ]; then
    echo "WSGI file exists"
    cat hoztechsite/wsgi.py
else
    echo "ERROR: WSGI file not found!"
    exit 1
fi 