FROM python:3.11-slim AS base

FROM base AS builder
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  PATH="$PATH:/usr/local/bin" \
  PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.11/site-packages" \
  POETRY_VERSION=1.7.0
WORKDIR /src/
RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --no-root --without dev

FROM base AS runtime
ARG APP_RELEASE=not-set
ENV APP_RELEASE=$APP_RELEASE \
  PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.11/site-packages"
RUN apt-get update && apt-get install -y curl && apt-get clean
COPY --from=builder /usr/local /usr/local
WORKDIR /app/
COPY . .
ENTRYPOINT ["poe", "start-prod"]
