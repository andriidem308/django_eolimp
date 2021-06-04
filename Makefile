MANAGE = python3 manage.py
PROJECT_DIR = $(shell pwd)

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE)  makemigrations

migrate:
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

lint:
	flake8 .