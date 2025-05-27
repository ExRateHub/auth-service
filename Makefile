PYTHONPATH := src
HTTP_SERVER := granian
MIGRATION := alembic

export PYTHONPATH

.PHONY: run-dev-serve
run-dev-serve:
	uv run $(HTTP_SERVER) \
	    --host $(SERVER_HOST) \
	    --port $(SERVER_PORT) \
	    interface.http.asgi:create_asgi_application \
		--interface=asgi \
		--factory \
		--reload

.PHONY: migrate
migrate:
	uv run $(MIGRATION) upgrade head