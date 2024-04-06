FROM python:3.12 as base

ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

FROM base
EXPOSE 8000

WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

