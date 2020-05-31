release: python app/manage.py migrate
web: gunicorn --chdir /app/app app.wsgi --log-file -