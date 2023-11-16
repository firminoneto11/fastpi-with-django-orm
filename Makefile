dev:
	uvicorn conf.asgi:app --reload --port 8001

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
