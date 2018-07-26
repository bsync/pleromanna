dev: 
	cd pleroma && gunicorn -b 0.0.0.0:8000 pleroma.wsgi
prod: 
	cd pleroma && gunicorn -b 0.0.0.0:80 pleroma.wsgi
