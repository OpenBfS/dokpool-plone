# Dockerfile for running instance of ELAN as Standalone Container
#
# Requirements:
# Place an zodb-Backup (created with plonebackup) next to this Dockerfile and name it initialELAN-backup.tgz
#
# Info:
# This Container runs standalone using sqlite- and zope-Databses as backend.
# No need for PostgreSQL, but not recommended for production use
#
# If you want to restore a transfer-Db (based on sqlite) just place a elan_transfer.sqlite file next to this
# Dockerfile. See ./Plone/buildout_docker.cfg where elan_transfer.sqlite is expected to be in running container
#
# build with e.g. `docker build --force-rm=true -t bfs/elan5standalone -f ./Docker/ubuntu16pgsql/Dockerfile .',
# then run with e.g.
# `docker run --name bfs_elan5_standalone -dp 18081:8081 bfs/elan5standalone:latest'
#
# In case you want to interact with the container, use e.g.
# `docker exec -it bfs_elan5_standalone "/bin/bash"'
#
FROM ubuntu:xenial
MAINTAINER Marco Lechner<mlechner@bfs.de>

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y upgrade && apt-get -y install python postgresql-server-dev-9.5 libxml2-dev libxslt-dev libssl-dev libffi-dev python-virtualenv tar libjpeg-turbo8-dev python-dev gcc make g++ ghostscript libav-tools && apt-get autoclean
RUN adduser --system --disabled-password --shell /bin/bash --group --home /home/zope --gecos "Zope/Plone system user" zope
#
# install ELAN
#
RUN mkdir -p /opt/bfs/elan
ADD . /opt/bfs/elan/
WORKDIR /opt/bfs/elan/Plone
RUN cd /opt/bfs/elan/Plone && python bootstrap.py
RUN cd /opt/bfs/elan/Plone && ./bin/buildout -Nvc buildout_docker.cfg

RUN chown -R zope.zope /opt/bfs
USER zope
ENV HOME /home/zope
# try to use sqlite instead of postgreSQL as DB backend for transfer
WORKDIR /opt/bfs/elan/Plone
EXPOSE 8081
CMD [ "/opt/bfs/elan/Plone/bin/instance", "fg"]

