#!/bin/bash

set -e

# Start the service
uv run alembic upgrade head
