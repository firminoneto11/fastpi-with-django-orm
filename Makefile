dev:
	uvicorn conf.asgi:app --reload

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate