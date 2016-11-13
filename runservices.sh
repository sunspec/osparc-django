cd server
python manage.py runserver 0.0.0.0:8001 >> ~/osparc_services.log 2>&1
disown
