# Dokpool
Description

Contact
-------
Bundesamt für Strahlenschutz / General Office for Radiation Protection
SW2 Notfallschutz, Zentralstelle des Bundes (ZdB)
Willy-Brandt-Strasse 5
38226 Salzgitter
info@bfs.de

License
------
Dokpool including ELAN5 and most of its components are published using the [GNU GPL v>=3](http://www.gnu.org/licenses/gpl-3.0) license.
See `LICENSE` for more details.

Sources
---------
Publicly available repo:
```
git clone https://github.com/OpenBfS/dokpool-plone
```

## Building
If you want to run Dokpool there are several ways. Run Dokpool in a production environment using PostgreSQL as Backend or run it as simple Testinstallation using ZODB/SQLite Backend. Using Varnish/Supervisor `Dokpool` can be configured to run in a multi.instance mode as well. See several *.cfg files in ./Plone to be used with buildout.

For rapid simple testing/demonstrations we provide Dockerfiles in ./Docker as well. See Docker (https://www.docker.com) for further information on this Container technology.

#### Requirements:
If you want to start from scratch, just go on. If you want to use a preconfigured Dokpool, you need a zodb-Backup (created with plonebackup) of a zodb. See various Dockerfiles in ./Docker that take care of this. Usually the zodb Backup has to be named initialELAN-backup.tgz. Containers using zodb/sqlite as backend run standalone using sqlite- and zope-Databases but are not recommended for production use! For production using a PostgreSQL-DB backend is recommended.

#### Build:
FIXME
```sh
$ docker build --force-rm=true -t elan5/standalone -f Dockerfile.standalone .
```
or for Oracle Linux
```sh
$ docker build --force-rm=true -t elan5/standalone -f Dockerfile.oel7 .
```
#### Run:
```sh
$ docker run --name elan5_standalone -dp 18081:8081 elan5/standalone:latest
```
Your running Dokpool is available on port 18081 on your host machine (http://localhost:18081).

In case you want to interact with the running container, use e.g.
```sh
$ docker exec -it elan5_standalone "/bin/bash"
```

### Build your own standalone ELAN5 on a current Linux Distribution
To build Dokpool on a current Linux Distribution you simply have to clone the repository run three commands from CLI and got it running 

#### Requirements:
Dokpool refuses to run as root. Add a system account (e.g. elan) which can be used to run Dokpool.
Python2.7 and Git (to clone the Repo).
```sh
$ apt-get install git python-dev libffi-dev libssl-dev libxml2-dev libxslt-dev postgresql-server-dev libjpeg-turbo8-dev gcc
```

#### Build:

```sh
$ git clone https://github.com/OpenBfS/dokpool-plone
$ cd dokpool-plone/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ python ./bootstrap.py
$ ./bin/buildout -Nvc buildout.cfg
$ ./bin/instance fg
```

#### Run:

```sh
$ cd dokpool-plone/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ ./bin/instance fg
```

#### Backup and Restore standalone Instances

```sh
$ cd dokpool-plone/Plone
$ ./bin/plonebackup-full
# backups will be stored in
# dokpool-plone/Plone/var/plonebackups
$ ./bin/plonebackup-restore
```

### Dokpool with PostgreSQL
```sh
buildout -Nc relstorage.cfg
```


## Known issues
coming soon

## Mailing Lists
coming soon

## Contributing
coming soon

## More Information
coming soon

