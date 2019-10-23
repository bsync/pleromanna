DYML=docker-compose.yml

upd: 
	docker-compose -f $(DYML) up -d

int_up: 
	$(MAKE) DYML=docker-compose.int.yml

prod_up: 
	$(MAKE) DYML=docker-compose.prod.yml

down: 
	docker-compose down

build:
	docker-compose build

showmigs: upd
	docker-compose exec pleroma python3 manage.py showmigrations

pygrate: upd
	docker-compose exec pleroma python3 manage.py makemigrations pleromanna
	docker-compose exec pleroma python3 manage.py migrate

superuser: upd
	docker-compose exec pleroma python3 manage.py createsuperuser

pshell: upd
	docker-compose exec pleroma bash

pyshell: upd
	docker-compose exec pleroma python3 manage.py shell

ipyshell: upd
	docker-compose exec pleroma ipython

dbshell: upd
	docker-compose exec pleroma python3 manage.py dbshell

collected: upd
	docker-compose exec pleroma python3 manage.py collectstatic -i wagtail* -i common* -i admin* --no-input

attached: upd
	docker attach pleroma

dumpdb:
	pg_dump -U dbsync -h dev.pleromabiblechurch.org -d pleromadb > dev.dump

syncdbs: upd
	@docker exec pleroma_postgres dropdb -U postgres postgres || true
	@sleep 3
	@docker exec pleroma_postgres createdb -U postgres -O postgres postgres
	#TODO: User should be postgres instead of dbsync eventually
	@sed -s 's/dbsync/postgres/g' dev.dump | docker exec -i pleroma_postgres psql -U postgres postgres 
	@docker-compose down 

docker_volume_backups:
	sudo tar czvf plerodata.backup.tar.gz /var/lib/docker/volumes/plerodata
	sudo tar czvf pleromedia.backup.tar.gz /var/lib/docker/volumes/pleromedia

docker_volume_restore:
	sudo tar xzvf plerodata.backup.tar.gz -C / 
	sudo tar xzvf pleromedia.backup.tar.gz -C / 
.ONESHELL:
