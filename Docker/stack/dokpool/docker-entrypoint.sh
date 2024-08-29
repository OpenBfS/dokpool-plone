#!/bin/bash
set -e

zope_conf="/opt/bfs/dokpool/Plone/parts/instance1/etc/zope.conf"

sed -i "s/address 8081/address $DOKPOOL_INSTANCE_PORT/g" "$zope_conf"
sed -i "/ELANENGINE/c\ELANENGINE postgres://${TRANSFER_DB_USER}:${TRANSFER_DB_PASS}@${TRANSFER_DB_HOST}:${TRANSFER_DB_PORT}/${TRANSFER_DB_NAME}" "$zope_conf"
sed -i "/dsn/c\dsn dbname=${DB_NAME} user=${DB_USER} host=${DB_HOST} password=${DB_PASS} port=${DB_PORT}" "$zope_conf" &
if [ -n "${RELSTORAGE_SKIP_CREATE_SCHEMA}" ]; then
  if ! grep -q "create-schema" "$zope_conf"; then
      sed -i "/shared-blob-dir/a\create-schema false" "$zope_conf" &
  fi
fi

exec /opt/bfs/dokpool/Plone/bin/instance1 console

