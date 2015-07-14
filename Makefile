help:
	@echo 'make            Print this help'
	@echo
	@echo 'Whole app commands:'
	@echo 'make up         Download and start all'
	@echo 'make ps         Container status'
	@echo 'make logs       See all logs'
	@echo 'make stop       Stop all containers'
	@echo 'make restart    Restart all containers'
	@echo 'make rm         Delete containers'
	@echo 'make test       Run all tests'
	@echo
	@echo 'Container commands:'
	@echo 'make logs-back  See only backend logs'
	@echo 'make back       Debug in backend via iPython'

up:
	@docker-compose up -d
	@docker-compose ps

logs log:
	@docker-compose logs

logs-back log-back:
	@docker-compose logs back

start:
	@docker-compose start
	@docker-compose ps

stop:
	@docker-compose stop
	@docker-compose ps

restart:
	@docker-compose restart
	@docker-compose ps

ps:
	@docker-compose ps

t:
	@docker-compose run test /bin/bash

front fe frontend ui:
	@docker-compose run front /bin/bash

back be backend api:
	@docker-compose run back /bin/bash

shell:
	@docker-compose run back django-admin shell

dbshell:
	@docker-compose run back django-admin dbshell

initdb:
	@docker-compose run back django-admin makemigrations --noinput
	@docker-compose run back django-admin migrate
	@docker-compose run back django-admin init_superuser

testdb:
	@docker-compose run back psql -f /code/gasistafelice/fixtures/test.sql

rm:
	@docker-compose stop
	@docker-compose rm -f

rmall: rm
	@docker rmi -f befair/gasistafelice-{front,back}

rmc:
	@docker rm -f $(docker ps -aq)

rmi: rmc
	@docker rmi -f $(docker images -aq)

test: test-unit test-integration test-e2e
	@echo 'All tests passed!'

test-unit:
	@echo 'TODO: unit test'

test-integration:
	@echo 'TODO: integration test'

test-e2e:
	@docker-compose run --rm e2e
