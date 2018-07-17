dev: stop
	docker-compose up 

build:
	docker-compose build 

prod: stop
	docker-compose up -d
	
migration:
	docker-compose run migration

stop:
	docker-compose down
