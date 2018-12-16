ldev: .penv
	bash -c 'export RDS_HOSTNAME=localhost RDS_USERNAME=travis RDS_DB_NAME=pleromadb && source .penv/bin/activate && cd pleromanna && python3 manage.py makemigrations'
	bash -c 'export RDS_HOSTNAME=localhost RDS_USERNAME=travis RDS_DB_NAME=pleromadb && source .penv/bin/activate && cd pleromanna && python3 manage.py migrate'
	bash -c 'export RDS_HOSTNAME=localhost RDS_USERNAME=travis RDS_DB_NAME=pleromadb && source .penv/bin/activate && cd pleromanna && python3 manage.py collectstatic --no-input'
	bash -c 'export RDS_HOSTNAME=localhost RDS_USERNAME=travis RDS_DB_NAME=pleromadb && source .penv/bin/activate && cd pleromanna && python3 manage.py runserver 0.0.0.0:8000'

dev: .penv
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py runserver 0.0.0.0:8000'

devdb:
	dropdb pleromadb; createdb pleromadb
	pg_dump -C -h pleromadb.cqxcmysb4mot.us-east-2.rds.amazonaws.com -U dbsync pleromadb | psql -h localhost -U travis pleromadb

.penv: 
	virtualenv --python=python3 .penv
	bash -c 'source .penv/bin/activate && pip install -r pleromanna/requirements.txt'

prod: 
	cd pleromanna && gunicorn -b 0.0.0.0:80 pleroma.wsgi

migrated:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py makemigrations'
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py migrate'
   
dbshell:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py dbshell'

zappadev: migrated
	bash -c 'source .penv/bin/activate && find . -name "*.pyc" -delete'
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py collectstatic -v2 --no-input && zappa update dev'

zaptail:
	bash -c 'source .penv/bin/activate && cd pleromanna && zappa tail dev --since 10m'
