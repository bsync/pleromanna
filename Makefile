include Makefile.defs

run: .penv .nginx migrated stop
	$(call gunicorn,3)

run_dev_server: .penv migrated 
	$(call exenv,python manage.py runserver 0.0.0.0:8000)

stop: 
	kill -INT $$(cat gunicorn.pid) || true

pyshell:
	$(call exenv,python manage.py shell)

collected:
	$(call collectstatic)

migrated:
	echo "First make migrations..."
	$(call exenv,python manage.py makemigrations pleromanna)
	echo "then migrate..."
	$(call exenv,python manage.py migrate)

bash:
	@echo "PS1='django> '" > /tmp/rc
	bash --rcfile /tmp/rc -i

#Dev wrapped targets 
devserve: 
	$(call devmake,run_dev_server)

devcollected:
	$(call devmake,collected)

devbash:
	$(call devmake,bash)

devpyshell:
	$(call devmake,pyshell)

devmigrated:
	$(call devmake,migrated)


# Under the hood targets
.nginx: 
	$(call nginx_install)
	$(call certbot_install)

.penv: pleromanna/requirements.txt
	virtualenv --python=python3 .penv
	$(call exenv,pip install -r pleromanna/requirements.txt)
	touch .penv

syncdb:
	$(call dumpdb)

dbshell:
	$(call exenv,python manage.py dbshell)

deploy:
	sudo (apt install -y postgres)
	echo "TODO: configure a database called pleromadb"
	sudo (apt install -y nginx && cp nginx.conf /etc/nginx/)
	echo "TODO: install letsencrypt cryptbot and run it to create certs"

.ONESHELL:

