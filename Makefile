VENV := .venv-aenir_web

_:
	echo -ne "make _frontend\nmake _backend\nmake _browser\n";

_frontend:
	make terminal_ &
	# frontend
	printf '\033]0;%s\007' "react-server";
	cd frontend/ && npm run dev -- --port 3000;

_backend: $(VENV)
	make terminal_ &
	# backend
	printf '\033]0;%s\007' "django-server";
	. ${VENV}/bin/activate;
	./backend/manage.py runserver;

_browser:
	# open browser for backend
	firefox http://127.0.0.1:8000/ http://localhost:3000;

terminal_:
	xfce4-terminal --working-directory=/home/eclair/Documents/coding/_web-dev/aenir_web/ &

$(VENV):
	python3 -m venv $(VENV)/;
