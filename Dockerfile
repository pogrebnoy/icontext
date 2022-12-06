FROM python:3.9-alpine

ENV PYTHONPATH=/app/icontext

ENV PYTHONUNBUFFERED=1

RUN addgroup -S icontext && adduser -h /app/icontext -S icontext -G icontext

COPY --chown=icontext:icontext requirements.txt /app/requirements.txt

RUN apk update --no-cache \
 && apk add --no-cache postgresql-dev \
 && apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
 && pip install --no-cache-dir --disable-pip-version-check -r /app/requirements.txt \
 && apk del .build-deps \
 && rm -rf /app/requirements.txt

COPY --chown=icontext:icontext . /app/icontext

WORKDIR /app/icontext

EXPOSE 8000