# ELAN 5
Description

## License
ELAN5 and most of its components are licensed under the [GPL](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

## Using
Where to find the user guide?

## Building
If you want to run ELAN5 there are several ways. Run ELAN5 in a production environment using PostgreSQL as  Backend or running it as simple Testinstallation on a simple ZODB/SQLite Backend. Using Varnish/Supervisor ELAN can be configured to run in a multi.instance mode as well. See several *.cfg files in ./Plone to be used with buildout.

For rapid simple testing/demonstrations we provide Dockerfiles as well. See Docker (https://www.docker.com) for further information on this Container technology.

### Build your own standalone ELAN5 using Docker
To build ELAN5 running in a Dockercontainer we provide a Version based on latest Ubuntu (Dockerfile.standalone) and a Version build on top of latest Oraclelinux.

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

### Build your own standalone ELAN5 using Docker
More details coming soon
```sh
$ ELANENGINE="sqlite:////tmp/elan5db"
$ buildout -Nc buildout.cfg
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

