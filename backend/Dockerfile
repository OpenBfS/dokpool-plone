# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.10.1
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

# Install current node/npm and build frontend files
RUN <<EOT
    set -e
    apt install -y --no-install-recommends gpg
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
    apt-get update
    apt-get install nodejs -yq
    npm ci
    npm run build
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Philip Bauer <bauer@starzel.de>" \
    org.label-schema.name="dokpool" \
    org.label-schema.description="dokpool image" \
    org.label-schema.vendor="Philip Bauer"

# Copy /app from builder
COPY --from=builder --chown=500:500 /app /app

# Compile our mo files
ENV zope_i18n_compile_mo_files=true

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT
