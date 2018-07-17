dev: stop
	docker-compose build 
	docker-compose up 

migration:
	docker-compose run migration

stop:
	docker-compose down
