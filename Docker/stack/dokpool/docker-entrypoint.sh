#!/bin/bash
sed -i "s/address 8081/address $DOKPOOL_INSTANCE_PORT/g" /opt/bfs/dokpool/Plone/parts/instance1/etc/zope.conf
sed -i "/ELANENGINE/c\ELANENGINE postgres://${TRANSFER_DB_USER}:${TRANSFER_DB_PASS}@${TRANSFER_DB_HOST}:${TRANSFER_DB_PORT}/${TRANSFER_DB_NAME}" /opt/bfs/dokpool/Plone/parts/instance1/etc/zope.conf
sed -i "/dsn/c\dsn dbname=${DB_NAME} user=${DB_USER} host=${DB_HOST} password=${DB_PASS} port=${DB_PORT}" /opt/bfs/dokpool/Plone/parts/instance1/etc/zope.conf &

exec /opt/bfs/dokpool/Plone/bin/instance1 console

