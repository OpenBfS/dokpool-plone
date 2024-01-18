# Docker file for a running postgres instance with the dosrec DB
#
# build from root dir of this repo with e.g.
# `docker build --force-rm=true -t bfs/elan_pgsql -f ../Docker/ubuntu14pgsql/Dockerfile.pgsql ./Docker/ubuntu14pgsql/ ',
# then run with e.g.
# `docker run --name elan_db -dp 2345:5432 bfs/elan_pgsql:latest'
#

FROM ubuntu:latest
MAINTAINER mlechner@bfs.de

#
# Use utf-8
#
RUN apt-get update && apt-get install -y apt-utils tzdata locales
RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

#
# Install postgres 14 + postgis 3
#
RUN apt-get update
RUN apt-get install -y postgresql-14-postgis-3 postgis \
    postgresql-plpython3-14

#
# Use user postgres to run the next commands
#
USER postgres

#
# Add superuser for remote access
#
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER zodbuser WITH SUPERUSER PASSWORD 'zodbuser';" && \
    psql --command "CREATE USER elan WITH SUPERUSER PASSWORD 'elan';"

#
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
#
RUN echo "host all  all    0.0.0.0/0  md5" \
    >> /etc/postgresql/14/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

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
# ADD pgsql elan_pgsql/
RUN /usr/lib/postgresql/14/bin/pg_ctl start -wD /etc/postgresql/14/main/ && \
    createdb -E UTF-8 -O zodbuser zodb && \
    createdb -E UTF-8 -O elan elan 

#
# Start Postgres-Server

CMD ["/usr/lib/postgresql/14/bin/postgres", "-D", \
     "/var/lib/postgresql/14/main", "-c", \
     "config_file=/etc/postgresql/14/main/postgresql.conf"]
