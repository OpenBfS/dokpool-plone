# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.10.1

# Stage to only build the theme
FROM node:20-slim as node

WORKDIR /app

# Add only files required to build theme (for better caching)
COPY src/docpool.base/docpool/base/resources src/docpool.base/docpool/base/resources
COPY src/docpool.config/docpool/config/resources src/docpool.config/docpool/config/resources
COPY src/docpool.elan/docpool/elan/resources src/docpool.elan/docpool/elan/resources
COPY src/docpool.rei/docpool/rei/resources src/docpool.rei/docpool/rei/resources
COPY src/docpool.theme/docpool/theme/resources src/docpool.theme/docpool/theme/resources
COPY src/elan.journal/elan/journal/resources src/elan.journal/elan/journal/resources

COPY src/docpool.rei/docpool/rei/browser/static src/docpool.rei/docpool/rei/browser/static
COPY src/docpool.theme/docpool/theme/static/images src/docpool.theme/docpool/theme/static/images

COPY package.json package.json
COPY package-lock.json package-lock.json
COPY webpack.config.js webpack.config.js

# Build theme
RUN <<EOT
    set -e
    npm ci
    npm run build
EOT

# Stage to build dokpool
FROM plone/server-builder:${PLONE_VERSION} as builder

WORKDIR /app

# Add local code
COPY . .

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    bin/pip install mxdev
    mv requirements-docker.txt requirements.txt
    # remove all test-extras from mx.ini
    sed -i'' -e '/extras \= test/d' mx.ini
    bin/mxdev -c mx.ini
    bin/pip install -r requirements-mxdev.txt
    bin/python /compile_mo.py
EOT

# New layer that has all code so the site can run
FROM plone/server-prod-config:${PLONE_VERSION}

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

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT

# Trigger shell-script to add site, create demo-content and start the site
CMD ["/app/scripts/build_demo_site.sh"]
