PYTHONPATH := src
HTTP_SERVER := granian
HTTP_SERVER_HOST ?= 127.0.0.1
HTTP_SERVER_PORT ?= 8080

ENVIRONMENT ?= dev

export PYTHONPATH
export ENVIRONMENT

.PHONY: run-dev-serve
run-dev-serve:
	$(HTTP_SERVER) \
	    interface.http.asgi:create_asgi_application \
		--host=$(HTTP_SERVER_HOST) \
		--port=$(HTTP_SERVER_PORT) \
		--interface=asgi \
		--factory \
		--reload

.PHONY: format
format:
	@echo "Applying formatting..."
	ruff format --preview src tests migrations

.PHONY: lint
lint:
	@echo "Run linting"
	ruff check
	mypy

.PHONY: test
test:
	@echo "Run tests"
	pytest tests
