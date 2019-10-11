# Development install 

Use this development buildout file https://git.starzel.de/snippets/18

## Linux dependency's

```
$ mkvirtualenv dokpool-plone
$ cd dokpool-plone/Plone
$ pip installl -r requirements.txt
$ sudo apt install libpq-dev
$ sudo apt install postgresql
$ bin/buildout -c dev_local.cfg
```

### Start with filestorage and demo content

```
$ bin/instance_filestorage fg
```

Create a new vanilla Plone-Site (without any addons activated). Access http://localhost:8080/Plone/@docpool_setup and start the demo creation process.

### With a production backup database

On Debian you maybe need "sudo -u postgres" in front of all commands. 

```
DB und user löschen:
$ dropdb zodb
$ dropuser zodbuser

User und DB anlegen:
$ createuser --createdb zodbuser
# On Mac OS ($ createdb zodb -U zodbuser)
$ createdb -O zodbuser zodb
$ sudo -u postgres psql
$ alter user zodbuser with encrypted password 'zodbuser';

DB restore:
$ pg_restore -d zodb dokpool_20190920-1210.backup
```

```
$ bin/instance_filestorage fg
```
