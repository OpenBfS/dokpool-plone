# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.9
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

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Philip Bauer <bauer@starzel.de>" \
    org.label-schema.name="dokpool" \
    org.label-schema.description="dokpool image" \
    org.label-schema.vendor="Philip Bauer"

# Copy /app from builder
COPY --from=builder /app /app

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT
