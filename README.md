# Dragrace Results Aggregation Service

![GitHub](https://img.shields.io/github/license/PlummersSoftwareLLC/primes-aggregator)

This service, written using FastAPI, is responsible for coordinating benchmarks
across many machines.

Because this service is developed using FastAPI, it automatically provides an OpenAPI
specification, and API documentation on `<HOST>/docs`.

## Setting up

1. Copy `alembic.ini.template` to `alembic.ini`
2. Adjust `sqlalchemy.url` in `alembic.ini` to the path to your database of choice
3. Run `pipenv install -d`
4. Run `pipenv run alembic upgrade head`

## Running the dev-server

1. Run `pipenv run uvicorn main:app --reload`

## Creating an admin account

In the `administrators` table, create a new row with your preferred username, and the
password set to `{<your_preferred_password>`, so, that is a curly open brace, and then
your preferred password.
The first time you log in, this password will be hashed.
