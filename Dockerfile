FROM python:3.12-slim

LABEL maintainer="https://suk.kr"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH="/:$PYTHONPATH"

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && apt-get remove -y curl \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY pyproject.toml poetry.lock /api/

RUN poetry install --no-root

COPY . /api

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]