#!/bin/bash
set -e
export VENVBIN=/app/bin

# CLIENT HOME
CLIENT_HOME="/data/$(hostname)/$(hostid)"
export CLIENT_HOME=$CLIENT_HOME

USER="$(id -u)"

# Create directories to be used by Plone
mkdir -p /data/filestorage /data/blobstorage /data/cache /data/log $CLIENT_HOME
if [ "$USER" = '0' ]; then
  find /data -not -user plone -exec chown plone:plone {} \+
  sudo="gosu plone"
else
  sudo=""
fi

CONF=zope.conf


export DELETE_EXISTING=1
echo "Creating site with demo content"
$sudo $VENVBIN/zconsole run etc/${CONF} /app/scripts/create_site.py
echo "Starting site..."
$sudo $VENVBIN/runwsgi -v etc/zope.ini config_file=${CONF}
