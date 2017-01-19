# Docker file for a running postgres instance with the dosrec DB
#
# build from root dir of this repo with e.g.
# `docker build --force-rm=true -t bfs/elan_pgsql -f ../Docker/ubuntu14pgsql/Dockerfile.pgsql ./Docker/ubuntu14pgsql/ ',
# then run with e.g.
# `docker run --name elan_db -dp 2345:5432 bfs/elan_pgsql:latest'
#

FROM debian:jessie
MAINTAINER mlechner@bfs.de

#
# Use utf-8
#
RUN echo \
    "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | \
    debconf-set-selections && \
    echo "locales locales/default_environment_locale select en_US.UTF-8" | \
    debconf-set-selections

RUN apt-get update -y && apt-get install -y locales

ENV LC_ALL en_US.UTF-8

#
# Install postgres 9.4 + postgis 2.1
#
RUN apt-get update && apt-get install -y postgresql-9.4-postgis-2.1 postgis \
    postgresql-plpython-9.4

#
# Use user postgres to run the next commands
#
USER postgres

#
# Add superuser for remote access
#
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER zodbuser WITH SUPERUSER PASSWORD 'zodbuser';" &&\
    psql --command "CREATE USER elan WITH SUPERUSER PASSWORD 'elan';"

#
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
#
RUN echo "host all  all    0.0.0.0/0  md5" \
    >> /etc/postgresql/9.4/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/9.4/main/postgresql.conf

#
# Expose the PostgreSQL port
#
EXPOSE 5432

#
# Create dosrec database
#
# Don't mind scary messages like
# 'FATAL: the database system is starting up'.
# It's because of the -w
#
ADD pgsql elan_pgsql/
RUN /usr/lib/postgresql/9.4/bin/pg_ctl start -wD /etc/postgresql/9.4/main/ && \
    createdb -E UTF-8 -O zodbuser zodb && \
    createdb -E UTF-8 -O elan elan 

#
# Start Postgres-Server
#
CMD ["/usr/lib/postgresql/9.4/bin/postgres", "-D", \
     "/var/lib/postgresql/9.4/main", "-c", \
     "config_file=/etc/postgresql/9.4/main/postgresql.conf"]
