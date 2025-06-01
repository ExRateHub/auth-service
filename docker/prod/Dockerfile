# Use the official slim Python 3.13 image as base
FROM python:3.13-slim AS development

# Set working directory inside the container
WORKDIR /app

# Ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Install curl and uv
RUN apt-get update && apt-get install -y curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Copy dependency configuration files
COPY pyproject.toml ./

# Install all dependencies including dev dependencies into the system environment
RUN uv sync --no-cache

# Copy the rest of the application code into the container
COPY . .

# Make the entrypoint script executable
COPY docker/prod/entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh

# Start the application using the entrypoint script
CMD ["./entrypoint.sh"]
