APP_NAME := aenir_web
VENV_NAME := .venv-aenir_web
NVM_VERSION := 24.13.0

.backend: _terminal backend/$(VENV_NAME)/
	#firefox http://127.0.0.1:8000/api/ &
	printf '\033]0;%s\007' "backend-server";
	bash -c 'cd backend/ && . $(VENV_NAME)/bin/activate && ./manage.py runserver;'

.frontend: _terminal frontend/node_modules/
	printf '\033]0;%s\007' "frontend-server";
	bash -c 'cd frontend/ && . ~/.nvm/nvm.sh && nvm install $(NVM_VERSION) && npm run dev -- --port 3000 --open;'

_terminal:
	xfce4-terminal --tab --working-directory=/home/eclair/Documents/coding/_web-dev/$(APP_NAME)/;

backend/$(VENV_NAME)/:
	bash -c 'python3 -m venv $(VENV_NAME)/ && . $(VENV_NAME)/bin/activate && pip install -r requirements.txt;'

frontend/node_modules/:
	bash -c 'cd frontend/ && . ~/.nvm/nvm.sh && nvm install $(NVM_VERSION) && npm install;'
