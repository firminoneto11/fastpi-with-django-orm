cov := rm -rf .coverage/; coverage run -m pytest

dev:
	uvicorn conf.asgi:app --reload --port 8001

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
