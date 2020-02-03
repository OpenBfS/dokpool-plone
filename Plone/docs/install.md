# Development install 

# Install & Setup

```
$ mkvirtualenv dokpool-plone
$ cd dokpool-plone/Plone
$ pip installl -r requirements.txt
$ sudo apt install libpq-dev
$ sudo apt install postgresql
$ bin/buildout -c local-develop.cfg
```

## Start with filestorage and demo content

```
$ bin/instance fg
```

Create a new vanilla Plone-Site (without any addons activated). Access http://localhost:8080/Plone/@@docpool_setup and start the demo creation process.

## With a production backup database

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

## Convert production backup database to filestorage

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

# Development

## Branches

### master

The branch with the code that is released on production. We release tags that exists on this branch, e.g. 2.1.0

### develop

The branch which is currently developed. Used for demos or test-deployments.

### tag (ex. 1.5.0)

The branch in which a certain version is being prepared before deployment.

### ticket_xxxx_some_task

A feature-branch, cut from develop which will be merged back to develop as soon as a feature is done.

Example:

.. code-block:: bash
    
    # Update develop
    $ git checkout develop
    $ git pull origin develop
    # Create new branch
    $ git checkout -b ticket_123_fix_was 
    # Do changes and commit if needed
    $ git commit -a -m 'Fix something (#123)'
    # Push the branch to gitlab
    $ git push origin ticket_123_fix_was 
    # Gitlab reports back with a merge request url
    # Visit the url and create a new merge request
    # Wait for a successful CI run and assign to reviewer
    
dual-use branches
-----------------

When a feature is meant to be used in develop and in release/xxx we need to first create a branch from develop and later create another from release/xxx. The changes in the first branch will be cherry-picked into the second branch.

Example:

.. code-block:: bash

    git checkout develop
    git checkout -b ticket_123_fix_was

make some changes

.. code-block:: bash

    git commit -a -m 'Fix something (#123)'
    git push

create pull-request

.. code-block:: bash

    git checkout release/2.1.0
    git checkout -b ticket_123_fix_was_for_release210
    git cherry-pick --no-commit xxxxxxx (the hash of the commit with 'Fix something (#123)')

maybe make more changes to make the original changes compatible with the release-branch

.. code-block:: bash

    git commit -a -m 'Fix something (#123) for release/2.1.0'
    git push

create pull-request
