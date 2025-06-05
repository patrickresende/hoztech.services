#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Installing Node.js dependencies..."
npm install

echo "Building Tailwind CSS..."
if [ -f "tailwind.config.js" ]; then
    echo "Tailwind config exists, building CSS..."
    npm run build
else
    echo "No Tailwind config found, skipping CSS build"
fi

echo "Cleaning up old static files..."
rm -rf staticfiles/*

echo "Checking static files integrity..."
for file in static/css/*.css static/js/*.js static/images/*; do
    if [ -f "$file" ]; then
        echo "File exists: $file"
        file "$file"
        ls -l "$file"
    else
        echo "WARNING: File not found: $file"
    fi
done

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Verifying collected files..."
for file in staticfiles/css/*.css staticfiles/js/*.js staticfiles/images/*; do
    if [ -f "$file" ]; then
        echo "Collected file exists: $file"
        file "$file"
        ls -l "$file"
    else
        echo "ERROR: Collected file not found: $file"
        exit 1
    fi
done

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