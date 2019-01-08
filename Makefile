local_dev: 
	RDS_HOSTNAME=localhost RDS_USERNAME=dbsync RDS_DB_NAME=pleromadb $(MAKE) ldev

local_collected:
	RDS_HOSTNAME=localhost RDS_USERNAME=dbsync RDS_DB_NAME=pleromadb $(MAKE) collected

ldev: .penv migrated 
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py runserver 0.0.0.0:8000'

run: .penv migrated 
	bash -c 'source .penv/bin/activate && cd pleromanna && gunicorn -w3 -b unix:/tmp/gunicorn.sock pleromanna.wsgi'

collected:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py collectstatic --no-input'

migrated:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py makemigrations'
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py migrate'

.penv: pleromanna/requirements.txt
	virtualenv --python=python3 .penv
	bash -c 'source .penv/bin/activate && pip install -r pleromanna/requirements.txt'
	touch .penv

dumpdb:
	(test -f pdb.dump && mv pdb.dump pdb.dump.old) && pg_dump pleromadb > pdb.dump

shell:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py shell'

dbshell:
	bash -c 'source .penv/bin/activate && cd pleromanna && python3 manage.py dbshell'

deploy:
	sudo (apt install -y postgres)
	echo "TODO: configure a database called pleromadb"
	sudo (apt install -y nginx && cp nginx.conf /etc/nginx/)
	echo "TODO: install letsencrypt cryptbot and run it to create certs"
