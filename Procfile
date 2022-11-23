web: newrelic-admin run-program uwsgi uwsgi.ini
worker: celery -A portcast worker -l info --concurrency=2 -B
