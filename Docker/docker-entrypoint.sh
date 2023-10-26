#!/bin/bash
set -e
# Create directories to be used by Plone
mkdir -p /data/filestorage /data/blobstorage /data/cache /data/log /data/instance
exec /opt/bfs/dokpool/Plone/bin/instance fg
