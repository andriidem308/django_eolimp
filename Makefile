MANAGE = python3 manage.py

run:
	$(MANAGE) runserver

run_8080:
	$(MANAGE) runserver 0:8080

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

migrate_acc:
	$(MANAGE) makemigrations accounts

migrate_tst:
	$(MANAGE) makemigrations testing

createsuperuser:
	$(MANAGE) createsuperuser

requirements:
	pip install -r requirements.txt

startapp:
	$(MANAGE) startapp $(app)