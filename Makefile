DYML=docker-compose.yml

up: 
	docker-compose -f $(DYML) up -d

down: 
	docker-compose down

build:
	docker-compose build

showmigs: up
	docker-compose exec pleroma python manage.py showmigrations

pygrate: up
	docker-compose exec pleroma python manage.py makemigrations pleromanna
	docker-compose exec pleroma python manage.py migrate

superuser: up
	docker-compose exec pleroma python manage.py createsuperuser

pshell: up
	docker-compose exec pleroma bash

pyshell: up
	docker-compose exec pleroma python manage.py shell

dbshell: up
	docker-compose exec pleroma python manage.py dbshell

collected: up
	docker-compose exec pleroma python manage.py collectstatic -i wagtail* -i common* -i admin* --no-input

attached: up
	docker attach plerodock_pleroma_1

dumpdb:
	pg_dump -U dbsync -h dev.pleromabiblechurch.org -d pleromadb > dev.dump

syncdbs: up
	@docker exec plerodock_postgres_1 dropdb -U postgres postgres || true
	@sleep 3
	@docker exec plerodock_postgres_1 createdb -U postgres -O postgres postgres
	#TODO: User should be postgres instead of dbsync eventually
	@sed -s 's/dbsync/postgres/g' dev.dump | docker exec -i plerodock_postgres_1 psql -U postgres postgres 
	@docker-compose down 

.ONESHELL:
