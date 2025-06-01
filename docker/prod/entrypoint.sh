#!/bin/bash

set -e

# Set defaults if not defined
: "${HTTP_SERVER_HOST:=0.0.0.0}"
: "${HTTP_SERVER_PORT:=8000}"


# Start the service
uv run granian interface.http.asgi:create_asgi_application \
		--host="${HTTP_SERVER_HOST}" \
    --port="${HTTP_SERVER_PORT}" \
		--interface="asgi" \
		--factory
