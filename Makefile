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
	@docker-compose run --rm test /bin/bash

front fe frontend ui:
	@docker-compose run --rm front /bin/bash

back be backend api:
	@docker-compose run --rm back /bin/bash

shell:
	@docker-compose run --rm back django-admin shell

dbshell:
	@docker-compose run --rm back django-admin dbshell

dbinit:
	@docker-compose run --rm back django-admin makemigrations --noinput
	@docker-compose run --rm back django-admin migrate
	@docker-compose run --rm back django-admin init_superuser

dbtest: dbclean
	@docker-compose run --rm back psql -f /code/gasistafelice/fixtures/test.sql

dbdump:
	@docker-compose run --rm back pg_dump -f /code/gasistafelice/fixtures/test.sql app

dbclean:
	@docker-compose run --rm back dropdb app
	@docker-compose run --rm back createdb app -O app

rm:
	@docker-compose stop
	@docker-compose rm -f

rmall: rm
	@docker rmi -f befair/gasistafelice-{front,back}

rmc:
	@docker rm -f $(docker ps -aq)

rmi: rmc
	@docker rmi -f $(docker images -aq)

test: test-info test-unit test-integration test-e2e
	@echo 'All tests passed!'

test-info:
	@echo 'To prepare the test db (this will clear your data):'
	@echo '    $$ make dbtest'
	@echo

test-unit:
	@echo 'Unit test: not implemented yet'

test-integration:
	@echo 'Integration test: not implemented yet'

test-e2e:
	@echo 'End-to-end test: running protractor'
	@docker-compose run --rm e2e
