PROJECT_NAME := aenir_web
VENV_NAME := .venv-$(PROJECT_NAME)
NVM_VERSION := 24.13.0

_backend: _terminal
	printf '\033]0;%s\007' "backend-server";
	bash -c 'cd backend/ && ./manage.py runserver;'

_frontend: _terminal frontend/node_modules/
	printf '\033]0;%s\007' "frontend-server";
	bash -c 'cd frontend/ && . ~/.nvm/nvm.sh && nvm install $(NVM_VERSION) && npm run dev -- --port 3000 --open;'

_terminal:
	xfce4-terminal --tab --working-directory=/home/eclair/Documents/coding/_web-dev/$(PROJECT_NAME)/;

$(VENV_NAME)/: requirements.txt
	bash -c 'python3 -m venv $(VENV_NAME)/ && . $(VENV_NAME)/bin/activate && pip install -r requirements.txt;'

backend/:
	# ceremony to make Django project.
	python3 -m venv .TEMP_VENV/;
	bash -c '. .TEMP_VENV/bin/activate && pip install django && django-admin startproject $(PROJECT_NAME)';
	# cleanup
	rm -r .TEMP_VENV/;
	mv $(PROJECT_NAME) backend/;
	# create .env file
	cat backend/$(PROJECT_NAME)/settings.py | grep SECRET_KEY > backend/.env;
	sed -i s/' '//g backend/.env;
	sed -i s/\'//g backend/.env;
	sed -i s/'^SECRET_KEY = .*'/'from decouple import config; SECRET_KEY = config("SECRET_KEY")'/g backend/$(PROJECT_NAME)/settings.py;

frontend/:
	npx create-react-router@latest $(PROJECT_NAME) --install --no-git-init;
	mv $(PROJECT_NAME) frontend/;

frontend/node_modules/: frontend/
	bash -c 'cd frontend/ && . ~/.nvm/nvm.sh && nvm install $(NVM_VERSION) && npm install;'

