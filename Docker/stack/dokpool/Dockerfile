# Dockerfile for running instance of Dokpool/ELAN as Container
#
# Requirements:
# A running Postgres-Service on (linked) machine having (empty) dokpool and dokpool_transfer DBs.
#
FROM ubuntu:bionic
LABEL maintainer="Marco Lechner<mlechner@bfs.de>"

ARG IMIS3_PACKAGE_REPO
ARG DOKPOOL_VERSION

# set timezone ME(S)Z
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# install packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade && DEBIAN_FRONTEND=noninteractive apt-get -y install git python postgresql-server-dev-10 libxml2-dev libxslt-dev libssl-dev libsasl2-dev libldap2-dev libffi-dev python-virtualenv tar libjpeg-turbo8-dev python-dev gcc make g++ ghostscript ffmpeg apt-utils tzdata locales libncurses-dev libedit-dev autoconf automake libjemalloc-dev libtool libpcre3-dev pkg-config graphviz python-pip && apt-get autoclean
#RUN DEBIAN_FRONTEND=noninteractive apt-get -y remove python-yaml python3-yaml
RUN adduser --system --disabled-password --shell /bin/bash --group --home /home/zope --gecos "Zope/Plone system user" zope
#
# install ELAN
#
RUN mkdir -p /opt/bfs/
RUN mkdir -p /opt/bfs/dokpool/blobs
RUN mkdir -p /opt/bfs/dokpool/Plone/var/log

# CHOWN is here and not further down so it runs before docker-compose volume. It is so, so the folders belong to the user zope
RUN chown -R zope.zope /opt/bfs/dokpool/blobs
RUN chown -R zope.zope /opt/bfs/dokpool/Plone/var/log

WORKDIR /opt/bfs/
COPY . .

WORKDIR /opt/bfs/dokpool/Plone
#ADD ./docker-compose-buildout.cfg ./
ADD ./dokpool/Docker/stack/dokpool/docker-entrypoint.sh /usr/local/bin
RUN cd /opt/bfs/dokpool/Plone && pip install --upgrade pip setuptools && pip install docutils && pip install -r requirements.txt
RUN cp config-template.cfg.tmpl config.cfg
# TODO: REMOVE THE -N FLAG WHEN GOING PRODUCTIVE!
RUN buildout bootstrap && ./bin/buildout -Nvc config.cfg

RUN chown -R zope.zope /opt/bfs

USER zope
ENV HOME /home/zope
WORKDIR /opt/bfs/dokpool/Plone


ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
