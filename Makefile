include Makefile.defs

run: .penv .nginx migrated stop
	$(call gunicorn,3)

run_dev_server: .penv migrated 
	$(call exenv,manage.py runserver 0.0.0.0:8000)

stop: 
	kill -INT $$(cat pleromanna/gunicorn.pid) || true

pyshell:
	$(call exenv,manage.py shell)

collected:
	$(call collectstatic)

migrated:
	echo "First make migrations..."
	$(call exenv,manage.py makemigrations pleromanna)
	echo "then migrate..."
	$(call exenv,manage.py migrate)

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

.certbot:
	$(call certbot_install)

.nginx: 
	# My dev machine is named 'spade' and I don't use certs on it
	[[ $(hostname) -ne "spade" ]] && $(MAKE) .certbot
	sudo cp nginx.conf /etc/nginx/nginx.conf
	which nginx || sudo apt install nginx
	which nginx && echo "Nginx installation detected."
	test -f /usr/local/nginx/logs/nginx.pid || sudo nginx&
	test -f /usr/local/nginx/logs/nginx.pid || sleep 3
	test -f /usr/local/nginx/logs/nginx.pid && echo "Nginx process detected."


.penv: pleromanna/requirements.txt
	virtualenv --python=python3 .penv
	$(call exenv,pip install -r pleromanna/requirements.txt)
	touch .penv

syncdb:
	$(call dumpdb)

dbshell:
	$(call exenv,manage.py dbshell)

deploy:
	sudo (apt install -y postgres)
	echo "TODO: configure a database called pleromadb"
	sudo (apt install -y nginx && cp nginx.conf /etc/nginx/)
	echo "TODO: install letsencrypt cryptbot and run it to create certs"

.ONESHELL:

