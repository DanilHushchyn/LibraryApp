MANAGE = python3 manage.py

run:
	$(MANAGE) runserver

m1:
	$(MANAGE) makemigrations

m2:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

init:
	$(MANAGE) migrate
	$(MANAGE) init_script


fix:
	sudo service postgresql restart
	$(MANAGE) reset_db --noinput
	$(MANAGE) migrate
	$(MANAGE) init_script
