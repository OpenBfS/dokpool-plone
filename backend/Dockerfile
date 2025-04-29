# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.1.1

# Stage to only build the theme
FROM node:20-slim AS node

WORKDIR /app

# Add only files required to build theme (for better caching)
COPY src/docpool.base/docpool/base/resources src/docpool.base/docpool/base/resources
COPY src/docpool.config/docpool/config/resources src/docpool.config/docpool/config/resources
COPY src/docpool.elan/docpool/elan/resources src/docpool.elan/docpool/elan/resources
COPY src/docpool.rei/docpool/rei/resources src/docpool.rei/docpool/rei/resources
COPY src/docpool.theme/docpool/theme/resources src/docpool.theme/docpool/theme/resources
COPY src/elan.journal/elan/journal/resources src/elan.journal/elan/journal/resources

COPY src/docpool.rei/docpool/rei/browser/static src/docpool.rei/docpool/rei/browser/static
COPY src/docpool.theme/docpool/theme/static src/docpool.theme/docpool/theme/static

COPY package.json package.json
COPY package-lock.json package-lock.json
COPY webpack.config.js webpack.config.js

# Build theme
RUN set -e
RUN npm ci
RUN npm run build

# Stage to build dokpool
FROM plone/server-builder:${PLONE_VERSION} AS builder
ARG GIT_COMMIT='Not detected'

WORKDIR /app

# Add local code
COPY . .

# Install local requirements and pre-compile mo files
RUN set -e
RUN apt install -y --no-install-recommends openssh-client ca-certificates
RUN bin/pip install uv==0.4.18
RUN bin/uv pip install mxdev
RUN mv requirements-docker.txt requirements.txt
RUN # remove all test-extras from mx.ini
RUN sed -i'' -e '/extras \= test/d' mx.ini
RUN bin/mxdev -c mx.ini
RUN bin/uv pip install -r requirements-mxdev.txt
RUN bin/python /compile_mo.py
RUN echo ${GIT_COMMIT} > GIT_COMMIT

# New layer that has all code so the site can run
FROM plone/server-prod-config:${PLONE_VERSION}
ENV TZ="Europe/Berlin"

LABEL maintainer="Philip Bauer <bauer@starzel.de>" \
    org.label-schema.name="dokpool" \
    org.label-schema.description="dokpool image" \
    org.label-schema.vendor="Philip Bauer"

# Copy /app from builder
COPY --from=builder --chown=500:500 /app /app
# Add compiled theme from node
COPY --from=node --chown=500:500 /app/src/docpool.theme/docpool/theme/static /app/src/docpool.theme/docpool/theme/static

# Compile our mo files
ENV zope_i18n_compile_mo_files=true

RUN set -e
RUN ln -s /data /app/var
