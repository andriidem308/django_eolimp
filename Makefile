MANAGE = python3 manage.py

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) makemigrations && $(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

requirements:
	pip install -r requirements.txt
