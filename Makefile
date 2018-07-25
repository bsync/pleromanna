dev: stop
	docker-compose up 

build:
	docker-compose build 

prod: stop
	docker-compose up -d
	
migration:
	docker-compose run docksync/pleromanna:latest \
    bash -c "python manage.py makemigrations && python manage.py migration"

stop:
	docker-compose down
