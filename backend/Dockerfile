# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13

# Stage to only build the theme
FROM node:23-slim AS node

WORKDIR /app

# Add only files required to build theme (for better caching)
COPY src/docpool.base/docpool/base/resources src/docpool.base/docpool/base/resources
COPY src/docpool.config/docpool/config/resources src/docpool.config/docpool/config/resources
COPY src/docpool.elan/docpool/elan/resources src/docpool.elan/docpool/elan/resources
COPY src/docpool.rei/docpool/rei/resources src/docpool.rei/docpool/rei/resources
COPY src/docpool.ui/docpool/ui/resources src/docpool.ui/docpool/ui/resources
COPY src/elan.journal/elan/journal/resources src/elan.journal/elan/journal/resources

COPY src/docpool.rei/docpool/rei/browser/static src/docpool.rei/docpool/rei/browser/static
COPY src/docpool.ui/docpool/ui/static src/docpool.ui/docpool/ui/static
# TODO Remove as soon as ui is the main pkg
COPY src/docpool.theme/docpool/theme/resources src/docpool.theme/docpool/theme/resources
COPY src/docpool.theme/docpool/theme/static src/docpool.theme/docpool/theme/static

COPY package.json package.json
COPY package-lock.json package-lock.json
COPY webpack.config.js webpack.config.js

# Build theme
RUN set -e
RUN npm ci
RUN npm run build

# Stage to build dokpool
FROM plone/server-builder:uv-${PYTHON_VERSION} AS builder
ARG GIT_COMMIT='Not detected'

WORKDIR /app

# Add local code
COPY . /src
WORKDIR /src

# Install project dependencies based on uv.lock and pyproject.toml
# We expect pyproject.toml to have an entry cointainer inside [dependency-groups]
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=mx.ini,target=mx.ini \
    uv tool run mxdev[uv] -c mx.ini && \
    uv sync \
        --locked \
        --no-dev \
        --no-group test \
        --group container \
        --no-install-project

WORKDIR /
RUN mv /src /app/src
WORKDIR /app/src

# Install local packages as editable sources under /app/src/src.
RUN --mount=type=cache,target=/root/.cache \
    uv tool run mxdev[uv] -c mx.ini && \
    uv sync \
        --no-dev \
        --no-group test \
        --group container

# Move skeleton files to /app
RUN <<EOT
    mv /app_skeleton/* /app
    rm -Rf /app_skeleton
    chmod +x /app/docker-entrypoint.sh
    mv scripts/* /app/scripts/
    rm -Rf scripts
    echo ${GIT_COMMIT} > ../GIT_COMMIT
EOT

# Compile translation files
# RUN <<EOT
#     /app/bin/python /compile_mo.py
# EOT

FROM plone/server-prod-config:uv-${PYTHON_VERSION}
ENV TZ="Europe/Berlin"

LABEL maintainer="Starzel.de for Bundesamt für Strahlenschutz <info@starzel.de>" \
    org.label-schema.name="dokpool-backend" \
    org.label-schema.description="Dokpool backend image." \
    org.label-schema.vendor="Starzel.de for Bundesamt für Strahlenschutz"

# Copy /app from builder
COPY --from=builder --chown=500:500 /app /app
# Add compiled theme from node
COPY --from=node --chown=500:500 /app/src/docpool.ui/docpool/ui/static /app/src/src/docpool.ui/docpool/ui/static
# TODO Remove as soon as ui is the main pkg
COPY --from=node --chown=500:500 /app/src/docpool.theme/docpool/theme/static /app/src/src/docpool.theme/docpool/theme/static
# Experimental: Use pyruvate
COPY --chown=500:500 templates/zope.ini /app/etc/zope.ini
# Make sure we load our translation first - see #4514
COPY --chown=500:500 templates/i18n-plone-configure.zcml /app/etc/package-includes/i18n-plone-configure.zcml
# Adds the session temp storage to the zope conf
COPY --chown=500:500 templates/temp_storage.conf /app/etc/zope.conf.d/temp_storage.conf
# Install ghostscript into prod container
RUN <<EOT
    set -e
    apt update
    apt install -y --no-install-recommends ghostscript poppler-utils
EOT

# Compile our mo files
ENV zope_i18n_compile_mo_files=true

RUN <<EOT
    set -e
    ln -s /data /app/var
    chown -R 500:500 /data
EOT
