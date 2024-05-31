local_path = --settings=config.django.local_settings

run:
	python manage.py runserver $(local_path)

makemigrations:
	python manage.py makemigrations $(local_path)

migrate:
	python manage.py migrate $(local_path)

superuser:
	python manage.py createsuperuser $(local_path)

startapp:
	python manage.py startapp $(app) $(local_path)

test:
	python manage.py test $(local_path) --keepdb --verbosity=2

mkfreeze:
	pip freeze > requirements.txt