cov := coverage run -m pytest
cov_port := 5500
url := http://localhost:$(cov_port)

env:
	rm -rf .venv/
	uv venv -p 3.12

deps:
	uv sync

dev:
	uvicorn src.presentation.api.http.asgi:app --reload --port 8000

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
	python -c "import webbrowser; webbrowser.open_new_tab('$(url)')"
	python -m http.server -d .coverage/html-report $(cov_port)
