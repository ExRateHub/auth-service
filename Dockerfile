ARG PYTHON_IMG=python:3.12-slim

FROM ${PYTHON_IMG} AS build

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip \
    && pip install uv
RUN uv sync --locked

COPY . .


FROM ${PYTHON_IMG} AS run

WORKDIR /app

RUN apt-get update && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["make", "run-dev-serve"]
