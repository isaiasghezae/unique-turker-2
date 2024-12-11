FROM docker.io/library/python:3.12-alpine
LABEL org.opencontainers.image.source="https://github.com/isaiasghezae/unique-turker-2"

ARG TARGETPLATFORM
ARG VERSION
ARG CHANNEL

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_BREAK_SYSTEM_PACKAGES=1 \
  CRYPTOGRAPHY_DONT_BUILD_RUST=1

ENV UMASK="0002" \
  TZ="Etc/UTC" \
  EXPOSED_URL="REPLACE_ME" \
  EXPOSED_PROTO="HTTPS" \
  CONFIG_DB="/config/database.db"

USER root

WORKDIR /config
VOLUME /config

WORKDIR /app

RUN apk add --no-cache \
  bash \
  catatonit \
  coreutils \
  curl \
  jq \
  nano \
  tzdata \
  git \
  && git clone https://github.com/isaiasghezae/unique-turker-2.git . \
  && pip install uv \
  && uv pip install --system \
  flask \
  flask-cors \
  Flask-SQLAlchemy \
  gunicorn \
  && chown -R root:root /app && chmod -R 755 /app \
  && if [ -f /config/database.db ]; then \
  rm -f /app/instance/database.db; \
  ln -s /config/database.db /app/instance/database.db; \
  else \
  cp /app/instance/database.db /config/database.db && \
  rm -f /app/instance/database.db && \
  ln -s /config/database.db /app/instance/database.db; \
  fi \
  && chown -R root:root /app && chmod -R 755 /app \
  && chown -R nobody:nogroup /app && chmod -R 755 /config/database.db \
  && rm -rf /root/.cache /root/.cargo /tmp/*

COPY ./dockerfiles/entrypoint.sh /entrypoint.sh

USER nobody:nogroup

EXPOSE 8080

ENTRYPOINT ["/usr/bin/catatonit", "--", "/entrypoint.sh"]

