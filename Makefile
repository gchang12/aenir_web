_:
	echo -ne "make .frontend\nmake .backend\nmake .browser\n";

.frontend:
	make terminal_ &
	# frontend
	cd frontend/ && npm run dev -- --port 3000;

.backend:
	make terminal_ &
	# backend
	printf '\033]0;%s\007' "django-server"; "django-server" 2>/dev/null; . .venv-aenir_web/bin/activate; ./backend/manage.py runserver;

.browser:
	# open browser for backend
	firefox http://127.0.0.1:8000/ http://localhost:3000 &

terminal_:
	xfce4-terminal --working-directory=/home/eclair/Documents/coding/_web-dev/aenir_web/ &
