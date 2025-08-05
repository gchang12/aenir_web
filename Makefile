servers:
	# open client
	# work from this branch
	xfce4-terminal --working-directory=/home/eclair/Documents/coding/_web-dev/aenir_web/;
	#firefox http://127.0.0.1:8000/ http://localhost:3000 &
	firefox http://127.0.0.1:8000/ &
	# frontend
	xfce4-terminal --title='react-server' --working-directory=/home/eclair/Documents/coding/_web-dev/aenir_web/frontend/ --command='npm start';
	# backend
	printf '\033]0;%s\007' "django-server"; "django-server" 2>/dev/null; . .venv-aenir_web/bin/activate; ./backend/manage.py runserver;
	
