web: gunicorn hoztechsite.wsgi:application --config gunicorn.conf.py
worker: python manage.py rqworker default
release: python manage.py migrate 