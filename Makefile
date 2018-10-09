dev: .penv
	bash -c 'source .penv/bin/activate && cd pleroma && python manage.py runserver 0.0.0.0:8000'

.penv: requirements.txt
	virtualenv --python=python3 .penv
	bash -c 'source .penv/bin/activate && pip install -r requirements.txt'

prod: 
	cd pleroma && gunicorn -b 0.0.0.0:80 pleroma.wsgi

migrated:
	bash -c 'source .penv/bin/activate && cd pleroma && python manage.py makemigrations'
	bash -c 'source .penv/bin/activate && cd pleroma && python manage.py migrate'
   
dbshell:
	bash -c 'source .penv/bin/activate && cd pleroma && python manage.py dbshell'
