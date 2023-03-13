convert:
	cd docker/ && docker-compose --env-file ../.env convert

build:
	cd docker/ && docker-compose --env-file ../.env build

up:
	cd docker/ && docker-compose --env-file ../.env up

up-d:
	cd docker/ && docker-compose --env-file ../.env up -d

up--build-d:
	cd docker/ && docker-compose --env-file ../.env up --build -d

logs:
	cd docker/ && docker-compose --env-file ../.env logs -f

logs-api:
	cd docker/ && docker-compose --env-file ../.env logs -f api

run-api-bash:
	cd docker/ && docker-compose --env-file ../.env run --rm api /bin/bash

down:
	cd docker/ && docker-compose --env-file ../.env down

down rmi-local-v:
	cd docker/ && docker-compose --env-file ../.env down --rmi local -v