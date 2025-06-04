web: newrelic-admin run-program gunicorn hoztechsite.wsgi:application --workers 2 --threads 2 --timeout 60
worker: python manage.py rqworker default
release: python manage.py migrate 