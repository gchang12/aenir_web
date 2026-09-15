PROJECT_NAME := aenir_web
VENV_NAME := .venv-$(PROJECT_NAME)

$(VENV_NAME)/: requirements.txt
	bash -c 'python3 -m venv $(VENV_NAME)/ && . $(VENV_NAME)/bin/activate && pip install -r requirements.txt;'

backend/: $(VENV_NAME)/
	bash -c '. $(VENV_NAME)/bin/activate && pip install django && django-admin startproject $(PROJECT_NAME)';
	mv $(PROJECT_NAME)/ backend/;
	# create .env file
	cat backend/$(PROJECT_NAME)/settings.py | grep SECRET_KEY > backend/.env;
	sed -i s/' '//g backend/.env;
	sed -i s/\'//g backend/.env;
	sed -i s/'^SECRET_KEY = .*'/'from decouple import config; SECRET_KEY = config("SECRET_KEY")'/g backend/$(PROJECT_NAME)/settings.py;
