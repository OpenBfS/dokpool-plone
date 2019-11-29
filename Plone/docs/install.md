# Development install 

## Linux dependency's

```
$ mkvirtualenv dokpool-plone
$ cd dokpool-plone/Plone
$ pip installl -r requirements.txt
$ sudo apt install libpq-dev
$ sudo apt install postgresql
$ bin/buildout -c local-develop.cfg
```

### Start with filestorage and demo content

```
$ bin/instance fg
```

Create a new vanilla Plone-Site (without any addons activated). Access http://localhost:8080/Plone/@@docpool_setup and start the demo creation process.

### With a production backup database

On Debian you maybe need "sudo -u postgres" in front of all commands. 

```
DB und user löschen (z.B. beim Einspielen von prod backup - siehe unten):
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

Start with Postgres DB und Relstorage
```
$ bin/instance_relstorage fg
```

### Convert production backup database to filestorage

Diesen Code als convert_to_zodb.conf im var Verzeichnis speichern und die Pfade anpassen:

```
<relstorage source>
    shared-blob-dir false
    blob-dir ./blobs
    <postgresql>
        dsn dbname=zodb user=zodbuser host=localhost password=zodbuser port=5432
    </postgresql>
</relstorage>

<blobstorage destination>
  blob-dir /Users/pbauer/workspace/dokpool-plone/Plone/var/blobstorage
  # FileStorage database
  <filestorage>
    path /Users/pbauer/workspace/dokpool-plone/Plone/var/filestorage/Data.fs
  </filestorage>
</blobstorage>
```

Die Postgres DB kann danach mit diesem Befehl in eine Data.fs mit blobstorage 
umgewandelt werden:

```
$ bin/zodbconvert var/convert_to_zodb.conf
```
