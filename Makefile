VENV := .venv-aenir_web
PROJECT_DIR := /home/eclair/Documents/coding/_web-dev/aenir_web/

.frontend:
	make .backend_terminal &
	# frontend
	printf '\033]0;%s\007' "react-server";
	cd frontend/ && npm run dev -- --port 3000;

.backend: $(VENV)
	make .main_terminal &
	# backend
	printf '\033]0;%s\007' "django-server";
	. $(VENV)/bin/activate;
	./backend/manage.py runserver;

.browser:
	firefox http://127.0.0.1:8000/ http://localhost:3000;

.backend_terminal:
	xfce4-terminal --tab --title=django-server --working-directory=${PROJECT_DIR} &

.main_terminal:
	xfce4-terminal --tab --working-directory=${PROJECT_DIR} &

#$(VENV): python3 -m venv $(VENV)/;
#f_terminal: xfce4-terminal --tab --title=react-server --working-directory=${PROJECT_DIR} &
