# ELAN 5
Description

## License
ELAN5 and most of its components are licensed under the [GPL](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

## Using
Where to find the user guide?

## Building
If you want to run ELAN5 there are several ways. Run ELAN5 in a production environment using PostgreSQL as  Backend or run it as simple Testinstallation using ZODB/SQLite Backend. Using Varnish/Supervisor ELAN can be configured to run in a multi.instance mode as well. See several *.cfg files in ./Plone to be used with buildout.

For rapid simple testing/demonstrations we provide Dockerfiles as well. See Docker (https://www.docker.com) for further information on this Container technology.

### Build your own standalone ELAN5 using Docker
To build ELAN5 running in a Dockercontainer we provide a Version based on latest Ubuntu (Dockerfile.standalone) and a Version build on top of latest Oracle Linux (Dockerfile.oel7).

#### Requirements:
Place an zodb-Backup (created with plonebackup) next to this Dockerfile and name it initialELAN-backup.tgz (or get one from the ELAN5 Repository)
This Containers run standalone using sqlite- and zope-Databases as backend only. No need for PostgreSQL, but not recommended for production use!

#### Build:
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
Your running ELAN5 is available on port 18081 on your host machine (http://localhost:18081).

In case you want to interact with the running container, use e.g.
```sh
$ docker exec -it elan5_standalone "/bin/bash"
```

### Build your own standalone ELAN5 on a current Linux Distribution
To build ELAN5 on a current Linux Distribution you simply have to clone the repository run three commands from CLI and got it running 

#### Requirements:
ELAN5 refuses to run as root. Add a system account (e.g. elan) which can be used to run ELAN5.
Python2.7 and Mercurial (to clone the Repo).
```sh
$ apt-get install mercurial python-dev libffi-dev libssl-dev libxml2-dev libxslt-dev postgresql-server-dev 
```

#### Build:

```sh
$ hg clone https://redmine-koala.bfs.de/hg/elan
$ cd elan/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ python ./bootstrap.py
$ ./bin/buildout -Nvc buildout.cfg
$ ./bin/instance fg
```

#### Run:

```sh
$ cd elan/Plone
$ export ELANENGINE=sqlite:////tmp/elan5db
$ ./bin/instance fg
```

#### Backup and Restore standalone Instances

```sh
$ cd elan/Plone
$ ./bin/plonebackup-full
# backups will be stored in
# elan/Plone/var/plonebackups
$ ./bin/plonebackup-restore
```

### ELAN 5 with PostgreSQL
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

