cov := coverage run -m pytest

env:
	rm -rf venv
	python3.12 -m venv venv

deps:
	poetry install --no-root

dev:
	uvicorn conf.gateways.fastapi:application --reload --port 8001

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -m http.server -d .coverage/html-report 5500
