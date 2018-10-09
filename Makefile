dev: .penv
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py runserver 0.0.0.0:8000'

.penv: pleromanna/requirements.txt
	virtualenv --python=python3 .penv
	bash -c 'source .penv/bin/activate && pip install -r pleromanna/requirements.txt'

prod: 
	cd pleromanna && gunicorn -b 0.0.0.0:80 pleroma.wsgi

migrated:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py makemigrations'
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py migrate'
   
dbshell:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py dbshell'

devdeploy:
	bash -c 'source .penv/bin/activate && cd pleromanna && zappa update dev'
