dev:
	docker-compose build 
	docker-compose up -d

migration:
	docker-compose run migration

stop:
	docker-compose down
