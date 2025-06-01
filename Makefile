# Project config
COMPOSE_FILE=docker/compose.yaml
PROFILE_DEV=--profile=dev
PROFILE_PROD=--profile=prod
PROFILE_MIGRATIONS=--profile=migrations
ENGINE=$(shell command -v docker 2> /dev/null || echo podman)
COMPOSE = $(ENGINE)-compose -f $(COMPOSE_FILE) # Compose wrapper

PYTHONPATH := src
ENVIRONMENT ?= dev

EXPORT_ENV := PYTHONPATH=$(PYTHONPATH) ENVIRONMENT=$(ENVIRONMENT)

# --- BUILD ---
compose-build-dev:
	$(EXPORT_ENV) $(COMPOSE) $(PROFILE_DEV) build

compose-build-prod:
	$(EXPORT_ENV) $(COMPOSE) $(PROFILE_PROD) build

# --- MIGRATIONS RUNNER ---
compose-up-migration:
	$(EXPORT_ENV) $(COMPOSE) $(PROFILE_MIGRATIONS) up

# --- UP SERVICES ---
compose-up-dev:
	$(EXPORT_ENV) $(COMPOSE) $(PROFILE_DEV) up --build

compose-up-prod:
	$(EXPORT_ENV) $(COMPOSE) $(PROFILE_PROD) up --build

# --- DOWN & CLEANUP ---
compose-down:
	$(COMPOSE) down

compose-clean:
	$(ENGINE) container prune -f
	$(ENGINE) image prune -f

# --- TESTING ---
test:
	$(EXPORT_ENV) uv run --extra test pytest

# --- LINTING ---
lint:
	$(EXPORT_ENV) uv run --extra lint ruff check
	$(EXPORT_ENV) uv run --extra lint mypy

# --- FORMATTING ---
fmt:
	PYTHONPATH=$(PYTHONPATH) uv run --extra fmt ruff format
